#!/usr/bin/env python3
"""
claudedocs-check-task-page — check one Claude Docs page against the Task style-guide excerpt.

Usage:
  check_task_page.py URL [--out DIR] [--save-snapshot]
  check_task_page.py --input FILE.md --url URL [--out DIR]
  check_task_page.py ... --judgment-file FILE.json   # merge judgment results produced out-of-band

Fetches <URL>.md (Mintlify serves raw MDX at that path), normalizes MDX, and runs three classes of check:
  deterministic — exact structural rules, verified in code, zero tolerance (front matter keys, lengths, column names, H2 counts)
  heuristic     — pattern rules that approximate a judgment (imperative verb, one action per step, conditional content)
  judgment      — rubric questions for Claude (one observable job, outcome-first, examples subordinate)

Judgment checks call the Messages API when ANTHROPIC_API_KEY is set. Otherwise the script writes the rubric prompt to
<out>/judgment-prompt.md and marks those checks "pending"; run the prompt and pass the JSON back with --judgment-file.

Exit code 1 when any mandatory check fails (so the script can gate a publish pipeline). Stdlib only.
"""
import argparse, json, os, re, sys, datetime, urllib.request, urllib.error

VERSION = "0.1.0"
STANDARD = "TeresaTalbot_Phase2_01StyleGuideExcerpt.md"
FRONT_MATTER_KEYS = ["content_type", "object_type", "owner_team", "supported_surfaces", "status",
                     "last_reviewed", "canonical_url", "next_action"]
AT_A_GLANCE_FIELDS = ["Audience", "Prerequisites", "Outcome"]
TROUBLESHOOTING_COLUMNS = ["Symptom", "Check", "Fix"]
IMPERATIVE_VERBS = set("""open create select click run copy enter choose add remove revoke install edit read configure
set write start stop delete record archive increment review render fetch deploy verify check turn go sign return prepare
provision monitor rotate restart follow call paste export repeat register apply notify use confirm decide connect replace
keep list leave save upload download navigate find type press name generate build test publish update pin request
grant disable enable close launch move pick view search""".split())
NON_IMPERATIVE_STARTERS = set("the a an this that these those you your it its if when in on at members each both there".split())
SECURITY_TRIGGERS = re.compile(r"\b(install|deploy|permission|credential|token|api key|oauth|secret|execute|external data|sign in)\b", re.I)
CONDITIONAL_MARKERS = re.compile(r"\b(Enterprise|Team|Pro|Max|Free) plan\b|\bon (desktop|mobile|web)\b|\borganization settings\b", re.I)


# ---------- input ----------

def fetch(url):
    md_url = url.rstrip("/") + ".md"
    for candidate in (md_url, url):
        req = urllib.request.Request(candidate, headers={"User-Agent": "claudedocs-check-task-page/" + VERSION})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read().decode("utf-8", "replace")
                return candidate, body
        except urllib.error.URLError as e:
            last = e
    raise SystemExit(f"fetch failed for {url}: {last}")


def split_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]


# ---------- MDX normalization ----------

def normalize(body):
    """Return (prose_lines, steps, headings, callouts, tabs, code_blocks_removed)."""
    body = re.sub(r"^> ## Documentation Index.*?(?:\n\n|\Z)", "", body, flags=re.S | re.M)
    code_blocks = re.findall(r"```.*?```", body, re.S)
    body = re.sub(r"```.*?```", "[code]", body, flags=re.S)
    callouts = re.findall(r"<(Note|Warning|Tip|Info)>(.*?)</\1>", body, re.S)
    body = re.sub(r"<(Note|Warning|Tip|Info)>.*?</\1>", "", body, flags=re.S)
    tabs = re.findall(r'<Tab title="([^"]+)">', body)

    steps, headings, prose = [], [], []
    current_h, current_tab, step_n = "(intro)", None, 0
    for i, raw in enumerate(body.splitlines(), 1):
        line = raw.strip()
        mt = re.match(r'<Tab title="([^"]+)">', line)
        if mt:
            current_tab = mt.group(1); continue
        if line == "</Tab>":
            current_tab = None; continue
        mh = re.match(r"^(#{1,6})\s+(.*)", line)
        if mh:
            headings.append({"level": len(mh.group(1)), "text": mh.group(2).strip(), "line": i})
            current_h = mh.group(2).strip(); step_n = 0
            prose.append(line); continue
        ms = re.match(r'<Step title="([^"]+)">', line)
        if ms:
            step_n += 1
            steps.append({"n": step_n, "text": ms.group(1), "section": current_h, "tab": current_tab, "line": i, "form": "Steps"})
            continue
        mo = re.match(r"^(\d+)\.\s+(.*)", line)
        if mo:
            steps.append({"n": int(mo.group(1)), "text": mo.group(2), "section": current_h, "tab": current_tab, "line": i, "form": "ordered-list"})
            prose.append(line); continue
        if re.match(r"^</?(Tabs|Steps|Step|CodeGroup|Tab)\b", line):
            continue
        prose.append(line)
    return prose, steps, headings, callouts, tabs, len(code_blocks)


def first_paragraph(prose):
    """First non-empty prose paragraph after the H1, skipping blockquotes (Mintlify description) and code."""
    seen_h1, buf = False, []
    for line in prose + [""]:
        if not seen_h1:
            seen_h1 = line.startswith("# "); continue
        if line.startswith(">") or line == "[code]":
            continue
        if line == "" and buf:
            return " ".join(buf)
        if line and not line.startswith("#"):
            buf.append(line)
    return " ".join(buf)


def words(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return [w for w in re.split(r"\s+", s.strip()) if w]


def first_word(s):
    s = re.sub(r"^[*_`]+", "", s.strip())
    m = re.match(r"([A-Za-z-]+)", s)
    return m.group(1).lower() if m else ""


def links_in(text):
    return re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)


# ---------- findings ----------

class Findings:
    def __init__(self):
        self.items = []

    def add(self, rule_id, rule, cls, severity, status, location, evidence, fix=""):
        self.items.append({"id": rule_id, "rule": rule, "class": cls, "severity": severity, "status": status,
                           "location": location, "evidence": evidence, "fix": fix})


def run_checks(fm, prose, steps, headings, callouts, tabs):
    F = Findings()
    h1s = [h for h in headings if h["level"] == 1]
    h2s = [h for h in headings if h["level"] == 2]

    # T1 Name the job in the H1
    if len(h1s) != 1:
        F.add("T1", "Name the job in the H1", "deterministic", "mandatory", "fail", "document",
              f"{len(h1s)} H1 headings found", "Use exactly one H1.")
    else:
        h1 = h1s[0]["text"]
        status = "pass" if len(h1) <= 70 else "fail"
        F.add("T1a", "H1 is 70 characters or fewer", "deterministic", "mandatory", status, f"line {h1s[0]['line']}",
              f"{len(h1)} chars: {h1!r}", "Shorten the H1 to one imperative verb and one object.")
        fw = first_word(h1)
        status = "pass" if fw in IMPERATIVE_VERBS else ("fail" if fw in NON_IMPERATIVE_STARTERS else "needs-review")
        F.add("T1b", "H1 begins with an imperative verb", "heuristic", "mandatory", status, f"line {h1s[0]['line']}",
              f"first word {fw!r}", "Start the H1 with the verb that names the job.")

    # T2 State the outcome first
    para = first_paragraph(prose)
    n = len(words(para))
    F.add("T2a", "First paragraph is 45 words or fewer", "deterministic", "mandatory", "pass" if n <= 45 else "fail",
          "first paragraph after H1", f"{n} words: {para[:160]!r}…" if n else "no opening paragraph found",
          "Open with one paragraph of 45 words or fewer that states the observable result.")
    F.add("T2b", "First paragraph describes the observable result", "judgment", "mandatory", "pending",
          "first paragraph after H1", para[:400], "Rewrite the opening around the result the reader will see.")

    # T3 Machine-readable identity
    missing = [k for k in FRONT_MATTER_KEYS if k not in fm]
    extra_note = "" if fm else " (no YAML front matter at all)"
    F.add("T3", "Front matter contains exactly one value for each required key", "deterministic", "mandatory",
          "pass" if not missing else "fail", "front matter", f"missing: {missing}{extra_note}",
          "Add typed front matter: " + ", ".join(FRONT_MATTER_KEYS) + ".")
    if fm.get("content_type") not in (None, "task"):
        F.add("T3b", "content_type is task", "deterministic", "mandatory", "fail", "front matter",
              f"content_type={fm.get('content_type')!r}", "Use the Task template only for task pages.")

    # T4 Orient before action — At a glance before first H2
    first_h2_line = h2s[0]["line"] if h2s else 10**9
    glance_lines = [i for i, l in enumerate(prose) if re.search(r"\*\*At a glance\*\*", l)]
    if not glance_lines:
        F.add("T4", "At a glance block appears before the first H2 with exactly Audience, Prerequisites, Outcome",
              "deterministic", "mandatory", "fail", "before first H2", "no 'At a glance' block found",
              "Add a blockquote 'At a glance' with exactly Audience, Prerequisites, and Outcome.")
    else:
        block = []
        for l in prose[glance_lines[0] + 1:]:
            if not l.startswith(">"): break
            m = re.match(r">\s*-\s*([A-Za-z ]+):", l)
            if m: block.append(m.group(1).strip())
        ok = block == AT_A_GLANCE_FIELDS
        F.add("T4", "At a glance block has exactly Audience, Prerequisites, Outcome", "deterministic", "mandatory",
              "pass" if ok else "fail", "At a glance block", f"fields: {block}", "Use exactly the three fields, in order.")

    # T5 Prerequisites before procedure
    byb = [h for h in h2s if h["text"].lower() == "before you begin"]
    first_step_line = steps[0]["line"] if steps else None
    if not steps:
        F.add("T5", "Before you begin appears before the first numbered procedure", "deterministic", "mandatory",
              "fail", "document", "no numbered procedure found — is this a task page?", "Confirm content type.")
    elif not byb:
        F.add("T5", "Before you begin appears before the first numbered procedure", "deterministic", "mandatory",
              "fail", f"first step at line {first_step_line}", "no 'Before you begin' H2",
              "Add a Before you begin section listing roles, access, and inputs the reader needs.")
    else:
        ok = byb[0]["line"] < first_step_line
        F.add("T5", "Before you begin appears before the first numbered procedure", "deterministic", "mandatory",
              "pass" if ok else "fail", f"line {byb[0]['line']}", f"Before you begin at {byb[0]['line']}, first step at {first_step_line}", "")

    # T6 One action per step
    for s in steps:
        loc = f"{s['section']}" + (f" [{s['tab']}]" if s["tab"] else "") + f" step {s['n']} (line {s['line']})"
        fw = first_word(s["text"])
        if fw in NON_IMPERATIVE_STARTERS or fw.endswith("ing"):
            F.add("T6a", "Step begins with an imperative verb", "heuristic", "mandatory", "fail", loc,
                  s["text"][:140], "Start the step with the action verb.")
        elif fw not in IMPERATIVE_VERBS and not re.match(r"^In \*\*", s["text"]):
            F.add("T6a", "Step begins with an imperative verb", "heuristic", "mandatory", "needs-review", loc,
                  f"first word {fw!r}: {s['text'][:120]}", "Confirm the first word is an imperative verb.")
        first_sentence = re.split(r"(?<=[.!?])\s", s["text"])[0]
        first_sentence = re.sub(r"\[[^\]]*\]\([^)]+\)", "link", first_sentence)
        second_actions = [v for v in re.findall(r"(?:,?\s(?:and|then)\s|\bthen\s)([a-z-]+)", first_sentence)
                          if v in IMPERATIVE_VERBS]
        if second_actions:
            F.add("T6b", "Step contains no more than one primary action", "heuristic", "mandatory", "fail", loc,
                  f"second action {second_actions}: {first_sentence[:160]!r}",
                  "Split into one step per action, or demote the second clause to a result sentence.")

    # T7 Product-specific separation
    ps = [h for h in headings if h["text"].lower().startswith("product-specific")]
    markers = [m.group(0) for m in CONDITIONAL_MARKERS.finditer("\n".join(prose) + "\n".join(c[1] for c in callouts))]
    if (tabs or markers) and not ps:
        F.add("T7", "Product, plan, organization, or surface differences appear under Product-specific after the shared procedure",
              "heuristic", "advisory", "fail", "document",
              f"conditional content without a Product-specific heading — tabs: {sorted(set(tabs))}, markers: {sorted(set(markers))[:6]}",
              "Move plan/org/surface conditions under a Product-specific heading; keep the shared procedure unconditional.")
    elif ps:
        F.add("T7", "Product-specific heading present", "deterministic", "advisory", "pass", f"line {ps[0]['line']}", ps[0]["text"], "")

    # T8 Explain access risk
    sec = [h for h in h2s if h["text"].lower() == "security and permissions"]
    triggers = sorted(set(m.group(0).lower() for m in SECURITY_TRIGGERS.finditer("\n".join(prose))))
    if triggers and not sec:
        F.add("T8", "Security and permissions section states what access is granted and how to remove it",
              "deterministic", "mandatory", "fail", "document",
              f"page reads data / installs / handles credentials ({triggers[:6]}) but has no 'Security and permissions' H2",
              "Add a Security and permissions H2 that consolidates access granted, revocation, and removal.")
    elif sec:
        F.add("T8", "Security and permissions section present", "deterministic", "mandatory", "pass", f"line {sec[0]['line']}", "", "")

    # T9 Make failures actionable
    ts = [h for h in h2s if h["text"].lower() == "troubleshooting"]
    if not ts:
        F.add("T9", "Troubleshooting contains a table with exactly Symptom, Check, Fix", "deterministic", "mandatory",
              "fail", "document", "no 'Troubleshooting' H2", "Add a Troubleshooting H2 with a Symptom | Check | Fix table.")
    else:
        start = ts[0]["line"]
        section = [l for l in prose if l.startswith("|")]
        header = next((l for l in section), None)
        cols = [c.strip() for c in header.strip("|").split("|")] if header else []
        rows = [[c.strip() for c in l.strip("|").split("|")] for l in section[2:]]
        bad_rows = [r for r in rows if len(r) < 3 or not r[1] or not r[2]]
        ok = cols == TROUBLESHOOTING_COLUMNS and not bad_rows
        F.add("T9", "Troubleshooting table has exactly Symptom, Check, Fix and every row is complete", "deterministic",
              "mandatory", "pass" if ok else "fail", f"line {start}", f"columns: {cols}; incomplete rows: {len(bad_rows)}", "")

    # T10 End with one path forward
    ns = [h for h in h2s if h["text"] == "Next steps"]
    if len(ns) != 1:
        F.add("T10", "Exactly one H2 named Next steps; first link equals next_action; at most two more links",
              "deterministic", "mandatory", "fail", "document", f"{len(ns)} 'Next steps' H2 found",
              "Add one Next steps H2 whose first link is next_action.")
    else:
        idx = next(i for i, l in enumerate(prose) if l.startswith("## Next steps"))
        body = []
        for l in prose[idx + 1:]:
            if l.startswith("## "): break
            body.append(l)
        lk = links_in("\n".join(body))
        ok = bool(lk) and lk[0] == fm.get("next_action") and len(lk) <= 3
        F.add("T10", "Next steps: first link equals next_action; at most two more links", "deterministic", "mandatory",
              "pass" if ok else "fail", f"line {ns[0]['line']}", f"links: {lk}; next_action: {fm.get('next_action')}", "")

    # Judgment checks
    F.add("J1", "Page helps a reader complete ONE observable job (task-contract-selected)", "judgment", "mandatory",
          "pending", "document", f"H2s: {[h['text'] for h in h2s]}", "Split into one task page per job, or reclassify.")
    F.add("J2", "Examples do not introduce a second object, alternate workflow, or unsupported capability", "judgment",
          "advisory", "pending", "examples", "", "")
    F.add("J3", "Heuristic T6 findings confirmed (imperative verb / one action per step)", "judgment", "advisory",
          "pending", "steps", "", "")
    return F


# ---------- judgment (LLM) ----------

RUBRIC = """You are checking one Claude Docs page against a Task content standard. Answer ONLY with a JSON array.
Each element: {"id": "<J1|J2|J3|T2b>", "status": "pass"|"fail", "evidence": "<quote or location>", "fix": "<one sentence>"}.

J1  Does the page help a reader complete exactly ONE observable job? A page that bundles setup, verification, rotation and
    removal is several jobs. Cite the H2s that are separate jobs.
J2  Do examples stay subordinate to the job? Fail if an example introduces a second object, an alternate workflow, or a capability
    the page does not otherwise support.
J3  Review the flagged steps below. For each, say whether the step really has two primary actions or whether the second clause is
    a result/qualifier. Report one J3 element with the count of confirmed vs rejected flags and the rejected step locations.
T2b Does the first paragraph after the H1 describe the observable result the reader gets, rather than the page's coverage?

FLAGGED STEPS:
{flags}

PAGE (code blocks removed):
{page}
"""


def build_prompt(prose, findings):
    flags = "\n".join(f"- {f['location']}: {f['evidence']}" for f in findings if f["id"] in ("T6a", "T6b"))
    page = "\n".join(prose)[:14000]
    return RUBRIC.replace("{flags}", flags or "(none)").replace("{page}", page)


def call_claude(prompt, model):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", method="POST",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        data=json.dumps({"model": model, "max_tokens": 2000, "messages": [{"role": "user", "content": prompt}]}).encode())
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.load(r)
    text = "".join(b.get("text", "") for b in out.get("content", []))
    m = re.search(r"\[.*\]", text, re.S)
    return json.loads(m.group(0)) if m else []


def merge_judgment(findings, results, source):
    by_id = {r["id"]: r for r in results}
    for f in findings:
        if f["class"] == "judgment" and f["id"] in by_id:
            r = by_id[f["id"]]
            f.update({"status": r.get("status", "pending"), "evidence": r.get("evidence", f["evidence"]),
                      "fix": r.get("fix", f["fix"]), "judged_by": source})


# ---------- report ----------

def render_md(meta, findings):
    fails = [f for f in findings if f["status"] == "fail"]
    mand = [f for f in fails if f["severity"] == "mandatory"]
    lines = [f"# Task-page check: {meta['url']}", "",
             f"- Run: {meta['run_at']}  ·  checker v{VERSION}  ·  standard: {STANDARD}",
             f"- Input: {meta['source']}",
             f"- Result: **{'FAIL' if mand else 'PASS'}** — {len(mand)} mandatory failures, "
             f"{len(fails) - len(mand)} advisory, {sum(f['status']=='needs-review' for f in findings)} needs-review, "
             f"{sum(f['status']=='pending' for f in findings)} pending judgment", "",
             "| ID | Class | Sev | Status | Rule | Location | Evidence |", "|---|---|---|---|---|---|---|"]
    for f in findings:
        ev = f["evidence"].replace("|", "\\|").replace("\n", " ")[:220]
        lines.append(f"| {f['id']} | {f['class']} | {f['severity']} | {f['status']} | {f['rule']} | {f['location']} | {ev} |")
    lines += ["", "## Proposed fixes", ""]
    for f in findings:
        if f["status"] == "fail" and f["fix"]:
            lines.append(f"- **{f['id']}** {f['location']}: {f['fix']}")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?")
    ap.add_argument("--input", help="local .md/.mdx file instead of fetching")
    ap.add_argument("--url", dest="url_meta", help="canonical URL to record when using --input")
    ap.add_argument("--out", default="out")
    ap.add_argument("--save-snapshot", action="store_true")
    ap.add_argument("--model", default=os.environ.get("CLAUDEDOCS_CHECK_MODEL", "claude-sonnet-4-5"))
    ap.add_argument("--judgment-file", help="JSON array of judgment results to merge (out-of-band run)")
    a = ap.parse_args()
    if not a.url and not a.input:
        ap.error("URL or --input required")

    if a.input:
        text = open(a.input, encoding="utf-8").read()
        source = f"local file {a.input}"
        url = a.url_meta or a.url or a.input
    else:
        url = a.url
        fetched_from, text = fetch(url)
        source = f"fetched {fetched_from}"

    slug = re.sub(r"[^a-z0-9]+", "-", re.sub(r"^https?://[^/]+/docs/", "", url).lower()).strip("-") or "page"
    os.makedirs(a.out, exist_ok=True)
    if a.save_snapshot and not a.input:
        with open(os.path.join(a.out, f"{slug}.snapshot.md"), "w", encoding="utf-8") as fh:
            fh.write(text)

    fm, body = split_front_matter(text)
    prose, steps, headings, callouts, tabs, ncode = normalize(body)
    F = run_checks(fm, prose, steps, headings, callouts, tabs)
    findings = F.items

    prompt = build_prompt(prose, findings)
    judged = None
    if a.judgment_file:
        judged = json.load(open(a.judgment_file, encoding="utf-8"))
        merge_judgment(findings, judged, f"judgment file {os.path.basename(a.judgment_file)}")
    else:
        try:
            judged = call_claude(prompt, a.model)
        except Exception as e:  # network or API failure must not hide the deterministic results
            print(f"[warn] judgment call failed: {e}", file=sys.stderr)
        if judged is not None:
            merge_judgment(findings, judged, f"api:{a.model}")
    if judged is None:
        with open(os.path.join(a.out, "judgment-prompt.md"), "w", encoding="utf-8") as fh:
            fh.write(prompt)
        print(f"[info] no ANTHROPIC_API_KEY — judgment checks pending; prompt written to {a.out}/judgment-prompt.md", file=sys.stderr)

    meta = {"url": url, "source": source, "run_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "checker_version": VERSION, "standard": STANDARD, "front_matter": fm,
            "stats": {"headings": len(headings), "steps": len(steps), "tabs": sorted(set(tabs)), "callouts": len(callouts),
                      "code_blocks_removed": ncode}}
    with open(os.path.join(a.out, f"{slug}.findings.json"), "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "findings": findings}, fh, indent=2)
    with open(os.path.join(a.out, f"{slug}.findings.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md(meta, findings))

    mand = [f for f in findings if f["status"] == "fail" and f["severity"] == "mandatory"]
    print(render_md(meta, findings))
    sys.exit(1 if mand else 0)


if __name__ == "__main__":
    main()
