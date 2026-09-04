# Checker run log — claudedocs-check-task-page v0.1.0

- Date: 2026-09-03 (America/Los_Angeles)
- Target: https://claude.com/docs/connectors/mcp-tunnels/setup
- Standard: `TeresaTalbot_Phase2_01StyleGuideExcerpt.md` (Task pages)
- Problem class from Phase 1: P0 "Customers cannot tell what each object does"
- Script: `Outputs/claudedocs-checker/check_task_page.py`
- Input: `snapshots/connectors-mcp-tunnels-setup.md` — the raw MDX served at `<url>.md`, fetched 2026-09-03 and saved as the run snapshot. The check ran against the saved snapshot (`--input`) because the run environment's egress policy blocks claude.com; the script's own fetch path (`<url>.md`, then `<url>`) is implemented and fails cleanly without network. Re-run on a machine with network to confirm parity.
- Judgment checks (J1, J2, J3, T2b): no `ANTHROPIC_API_KEY` in the run environment, so the script wrote `judgment-prompt.md`; the rubric was answered by Claude in the Cowork session and merged with `--judgment-file judgment-results.json`. The JSON records `judged_by` so this is distinguishable from an API run.
- Result: FAIL — 12 mandatory, 2 advisory. Exit code 1.
- Outputs: `connectors-mcp-tunnels-setup.findings.json`, `connectors-mcp-tunnels-setup.findings.md`, `judgment-prompt.md`, `judgment-results.json`

## Hand-labeled findings

Each finding was reviewed against the page and labeled. TP = a reviewer applying the standard would raise the same finding. FP = a reviewer would dismiss it. FN = a violation the checker missed.

| ID | Status | Label | Note |
|---|---|---|---|
| T1a | pass | TP | "Set up an MCP tunnel", 20 chars. |
| T1b | pass | TP | "Set up" is imperative. |
| T2a | fail | TP | First prose paragraph is 74 words and is about coverage, not outcome. |
| T2b | fail | TP | Judgment agrees: describes coverage and prerequisites. |
| T3 | fail | TP | No YAML front matter at all in the served MDX. Every identity field the memo's P2 asks for is absent, so nothing downstream (At a glance, owner, review date, next action) can be rendered or checked. |
| T4 | fail | TP | No At a glance block. |
| T5 | fail | TP | Prerequisites exist (Owner role, someone who can deploy containers) but are buried in the intro paragraph; there is no Before you begin. |
| T6a line 15 | fail | **FP** | "In claude.ai, go to **Organization settings > Tunnels**." A leading location phrase before one imperative. The rule as written fails it; a reviewer would not. Rule needs a tolerance clause. |
| T6b line 16 | fail | TP | "Open **Tunnels API** and create a key." Two actions. |
| T6a line 135 | fail | **FP** | Same location-phrase pattern as line 15. |
| T7 | fail (advisory) | **partial FP** | Fired on the Helm / Docker Compose tabs plus the "Enterprise plan" note. The Enterprise-plan availability is a plan condition that belongs in At a glance or Product-specific. The Helm vs Docker tabs are a deployment-target choice, not a product, plan, organization, or surface difference; flagging them is wrong under the rule's own definition. |
| T8 | fail | TP, with a caveat | The page has no Security and permissions H2, but the content is present and good — three Warning callouts on revoking the API key, `upstream.allowed_ips`, protecting `data/`. The finding is right that a reader can't find "what access is granted and how to remove it" in one place; the fix is consolidation, not authoring. |
| T9 | fail | **rule defect** | No Troubleshooting table. But the page deliberately delegates to `/docs/connectors/mcp-tunnels/troubleshooting`, which is exactly the IA the Phase 1 memo proposes (one troubleshoot page per object). The rule "Troubleshooting contains a table" is wrong for pages that have a sibling troubleshooting page; it should accept a table OR a single link to the object's troubleshooting page. |
| T10 | fail | TP | No Next steps. The page ends on compromise-response prose. |
| J1 | fail | TP | Six-verb description; Rotate and Remove are separate jobs with different triggers and readers. This is the single highest-value finding on the page and it comes from the judgment class, not the deterministic class. |
| J2 | pass | TP | Examples stay subordinate. |
| J3 | fail (advisory) | TP | Judgment rejected 2 of 3 heuristic step flags (the two FPs above) and confirmed 1. |
| — | (not raised) | **FN** | Helm "Install" step body: "Read the Tunnels API key into an environment variable ... then install into a dedicated namespace." Two actions. Missed because T6 reads only `<Step title>`, not the step body. |
| — | (not raised) | **FN** | Docker "Provision the tunnel" step body: "Read the Tunnels API key ..., then run the setup component." Same miss. |

## Tally

- Findings raised: 17 (14 fail, 3 pass)
- Deterministic class: 11 raised, 0 false positives, 1 rule defect (T9)
- Heuristic class: 4 raised, 2 false positives (T6a ×2), 1 partial (T7), 2 false negatives (T6b on step bodies)
- Judgment class: 4 raised, 0 false positives; J3 correctly overturned the 2 heuristic FPs
- Precision on fail findings: 11 / 14 = 79% (counting T7 as FP, T9 as TP-by-letter)
- Recall against hand-found violations: 11 true fails / (11 + 2 FN) = 85%

## Where the checker got it wrong, in one line each

1. T6a treats a leading location phrase as a non-imperative start (2 FPs). Fix: strip `^In [^,]+, ` before testing the verb.
2. T6b reads only `<Step title>` and misses two-action step bodies (2 FNs). Fix: test the first sentence of the step body too.
3. T7 treats any `<Tabs>` as conditional-content needing Product-specific; deployment-target tabs are not that (partial FP). Fix: fire on plan/org/surface markers only; report tabs as informational.
4. T9 enforces a table on a page that correctly delegates to a sibling troubleshooting page (rule defect, not a code bug). Fix: change the standard, then the check.
5. Not wrong but worth stating: the checker cannot verify `owner_team`, `last_reviewed`, or `status` values are true, only that they exist. A page that fills them with plausible values passes T3. That is the same failure the page-builder workflow produced on the connectors before/after (`owner_team: Docs Platform` with no source).

## What this run shows about the P0 problem

Every field a reader would use to answer "what does this object do, who is it for, what will I have" is absent from the served page: no typed identity, no At a glance, no outcome-first opening, no Next steps. The page is well written at the sentence level and still fails the P0 test at the page level, which is the point of checking structure rather than prose quality.
