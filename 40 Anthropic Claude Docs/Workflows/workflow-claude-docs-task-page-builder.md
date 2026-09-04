---
name: claude-docs-task-page-builder
# Adapted from the REBOOT article-builder pattern; this workflow's rules below control Claude Docs work.
source_copy: /Users/teresamtalbot/Documents/TheTalbotStudio/Work OS/20 REBOOT/Workflows/workflow-reboot-pack-article-builder.md
version: 1.2
status: active
log_execution: true
description: Create or update one Claude Docs Task page from approved source material using the Task content contract and machine-checkable editorial standards.
triggers:
  - "Claude Docs task page"
  - "rewrite a Claude Docs page"
  - "apply the Claude Docs Task template"
  - "run the workflow on [claude.com/docs URL]"
context:
  required:
    - "Knowledge/knowledge.md"
    - "Knowledge/claude-docs-audit-brief.md"
    - "TeresaTalbot_Phase2_StyleGuideExcerpt.md"
    - "TeresaTalbot_Phase2_ContentTypeTemplate.md"
    - "Templates/doc-task-topic.md"
    - "The exact target Markdown source (a local clipping, or the Markdown downloaded in Step 0 when the request gives a URL)"
  conditional:
    - condition: existing-page
      load: "The current target page before editing"
    - condition: source-material
      load: "Only the supplied or explicitly mapped canonical source material"
    - condition: url-target
      load: "The raw Markdown served at [canonical URL].md, saved locally before Step 1"
outputs:
  - id: rewritten-page
    artifact: Rewritten Claude Docs Task page
    class: authoritative-content
    destination: "Knowledge/claudedocs/"
    lifecycle: create-or-replace-after-approval
    review: explicit-user-approval-of-final-proposed-page
  - id: before-after-record
    artifact: Phase 2 before/after and rationale
    class: evidence
    destination: "Outputs/"
    filename: "[page-slug]_beforeAfter.md"
    lifecycle: create-after-run
    review: system
    minimum_fields: "target manifest, retained context manifest, complete before snapshot, after path or snapshot, source map, material-change rationale, QA history, approval state"
  - id: execution-log
    artifact: Workflow execution record
    class: log
    destination: "Outputs/logs/"
    filename: "YYYY-MM-DD-HHMM-claude-docs-task-page-builder.md"
    lifecycle: create-after-run
    review: system
    minimum_fields: "target path, source paths, workflow version, gate results, revisions, approval state, saved paths, final verification"
gates:
  - id: target-downloaded
    check: When the request gives a URL, the page's Markdown is saved locally as a clipping in `Knowledge/claudedocs/` and as a raw snapshot in `Outputs/claudedocs-checker/snapshots/` before any source is read.
    on-fail: "Download the page as Markdown using the Step 0 fallback order, or ask the user for a clipping. Do not draft from a rendered HTML page or from memory of the page."
  - id: target-resolved
    check: Exactly one target page and one bounded rewrite scope are identified.
    on-fail: "Resolve one Claude Docs page and whether the rewrite covers the full page or a named section."
  - id: source-boundary-resolved
    check: Every substantive claim is mapped to supplied or explicitly approved source material.
    on-fail: "Do not invent product behavior. Resolve the source boundary or mark the claim unresolved."
  - id: source-eligibility-passed
    check: Every mapped source is available, canonical, and current or explicitly approved for use; stale, superseded, or unresolved sources are identified before drafting.
    on-fail: "Resolve the source status or exclude the source from the retained context manifest."
  - id: task-contract-selected
    check: The page has one observable job and is appropriate for the Task content type.
    on-fail: "Use a different content type if the page is an overview, concept, reference, or troubleshooting page."
  - id: task-contract-qa-passed
    check: The page passes the Task contract, including typed front matter, outcome-first opening, three-field At a glance block, prerequisites, imperative single-action steps, Product-specific separation, security guidance, troubleshooting table, and one Next steps path.
    on-fail: "Repair the Task contract failures before approval."
  - id: unsupported-claims-qa-passed
    check: The rewrite adds no unsupported behavior, availability, permission, or surface claim.
    on-fail: "Remove the claim or map it to an approved source."
  - id: links-qa-passed
    check: Every internal Claude Docs link resolves to a valid route, and canonical_url and next_action are distinct valid Claude Docs URLs.
    on-fail: "Repair the link using an unambiguous mapped route or flag it unresolved."
  - id: technical-leakage-qa-passed
    check: Reader-facing content contains only implementation detail needed to act, understand a consequence, configure, verify, or recover; provenance remains in the evidence record.
    on-fail: "Remove or relocate unnecessary implementation detail without removing useful behavior or safety guidance."
  - id: reader-value-qa-passed
    check: Every section helps the intended reader act, decide, verify success, or recover, and does not duplicate an overview, reference, or troubleshooting page.
    on-fail: "Remove, consolidate, or relocate low-value or misowned content."
  - id: voice-qa-passed
    check: The page uses direct, clear Claude Docs language, approved terminology, and a consistent non-marketing register.
    on-fail: "Repair terminology, audience fit, or tone before approval."
  - id: before-after-qa-passed
    check: The retained record contains the complete before snapshot, the after path or snapshot, and a rationale for each material change.
    on-fail: "Complete the before/after evidence before handoff."
  - id: output-paths-resolved
    check: The page, evidence record, and execution log each have one resolved path under the target workspace before any write occurs.
    on-fail: "Resolve the output paths and confirm that no file will be written outside the target workspace."
  - id: approval-before-write
    check: The user explicitly approves the final proposed page before authoritative content is written.
    on-fail: "Do not replace the target page without approval of the final proposed page."
---

# Claude Docs Task Page Builder

**What it does:** Applies the Claude Docs Task content contract to one canonical Skills, Plugins, or Connectors page and records the before, after, and rationale.

**Job to be done:** When a Claude Docs page has an identifiable reader job but inconsistent structure or unclear object behavior, produce a page that tells readers what the object does, what they need, what to do, what access is involved, and what to do next.

**Scope:** This copy is for `/Users/teresamtalbot/Documents/TheTalbotStudio/Work OS/40 Anthropic Claude Docs`. It does not change the REBOOT workflow or its pack/article system.

**Hard rules:**

- Work on one page per run.
- When the request gives a URL instead of a local file, download the page as Markdown first (Step 0) and treat the saved copy as the target. Never draft from the live page or from recollection of it.
- Treat the supplied Claude Docs brief and mapped source material as authoritative for scope and claims.
- Treat the exact retained context manifest as the complete source boundary for drafting.
- Use the Task template and style-guide rules as the page contract.
- Keep product, plan, organization, and surface differences under `Product-specific` after the shared procedure.
- Preserve the before snapshot in the evidence deliverable.
- Do not silently add unsupported links, capabilities, plans, or permissions.
- Run QA before handoff and report any unresolved issue.

## Step 0: Download the target page when the request gives a URL

[GATE: target-downloaded]

Skip this step when the request names a local Markdown file. Otherwise:

1. Normalize the URL: strip the fragment and query string, remove a trailing slash, and append `.md` (Claude Docs serves each page's raw Markdown/MDX at `https://claude.com/docs/<path>.md`).
2. Fetch the Markdown, trying in this order and stopping at the first that returns `text/markdown` with the page's H1:
   1. `curl -sSL "<url>.md"` from the workspace shell (or the container shell).
   2. If the shell cannot reach claude.com (a known constraint for this workspace), open `<url>.md` in the built-in browser and read the text of the page's `<pre>` element.
   3. If neither works, stop and ask the user for a clipping of the page. Do not substitute a rendered HTML scrape or a page from memory.
3. Save the raw response unchanged to `Outputs/claudedocs-checker/snapshots/<slug>.md`, where `<slug>` is the URL path after `/docs/` with `/` replaced by `-` (for example `connectors-custom-remote-mcp`). This is the checker's `--input` file.
4. Save the target clipping to `Knowledge/claudedocs/<H1 title>.md` using the workspace clipping front matter (`title`, `source`, `author`, `published`, `created` = today's local date, `description` = the page's blockquote subtitle, `tags: [clippings]`), followed by the page body. Drop the site-wide `> ## Documentation Index` blockquote that precedes the H1; keep everything else, including MDX components such as `<Note>`, `<Warning>`, `<Card>`, and `<Columns>`, and keep internal links as served (`/docs/...`).
5. Record in the target manifest: the exact URL fetched, the fetch method that succeeded, the local time of the fetch, and both saved paths. Downstream steps read only the saved copy.

## Step 1: Resolve the target and scope

[GATE: target-resolved]

Identify one target Markdown page (the Step 0 clipping when the request gave a URL), its object type, its observable reader job, and whether the run covers the full page or a named section. For a page that explains rather than executes a job, stop and recommend the appropriate content type.

If the request does not identify exactly one page or scope, ask one focused question before loading source material. Record a target manifest with the target path, canonical URL, object type, observable job, scope, and create-or-update operation.

## Step 2: Assemble the writing context

[GATE: source-boundary-resolved]

Load `Knowledge/knowledge.md`, the Claude Docs brief, `TeresaTalbot_Phase2_StyleGuideExcerpt.md`, `TeresaTalbot_Phase2_ContentTypeTemplate.md`, `Templates/doc-task-topic.md`, the target page, and only the supplied or explicitly mapped source material. Record a retained context manifest with exact source paths, source dates or status, known uncertainties, exclusions, current page version, and the bounded rewrite brief before drafting. Do not browse or infer additional product behavior beyond that source set.

## Step 3: Select the Task contract

[GATE: task-contract-selected]

Use `content_type: task` only when the page helps a reader complete one observable job. Set `object_type` to exactly one of `skill`, `plugin`, or `connector`. Use the current canonical URL as `canonical_url` and a different valid Claude Docs URL as `next_action`. Preserve established URL and owner information unless the mapped source explicitly authorizes a change.

## Step 4: Draft the page and evidence record

Draft the page with this required shape: typed front matter, H1 naming one job in 70 characters or fewer, outcome-first opening of 45 words or fewer, exactly three At a glance fields, prerequisites, numbered imperative steps with one primary action each, Product-specific section when needed, Security and permissions, Troubleshooting with exactly `Symptom | Check | Fix` columns, and one Next steps H2. Preserve unaffected content in update mode. Examples must remain subordinate to the one job and may not introduce unsupported capability.

Create the before/after record alongside the draft for review, but persist it only as an approved run output. Include the complete before text, proposed after text or resolved after path, source map, AI workflow actions, unresolved issues, and a reason for every material change. Resolve output paths and run `[GATE: output-paths-resolved]` before any write.

## Step 5: Run QA and revise

Run the gates in this order:

1. `[GATE: source-boundary-resolved]` and `[GATE: source-eligibility-passed]` to identify unsupported claims, missing source coverage, or stale inputs.
2. `[GATE: task-contract-qa-passed]` to validate metadata, headings, fields, steps, permissions, troubleshooting, and next action.
3. `[GATE: unsupported-claims-qa-passed]` and `[GATE: links-qa-passed]` to test product behavior, availability, permissions, and routes.
4. `[GATE: technical-leakage-qa-passed]`, `[GATE: reader-value-qa-passed]`, and `[GATE: voice-qa-passed]` to review audience-facing quality.
5. `[GATE: before-after-qa-passed]` to verify the evidence record.

For each failure, record the exact location, violated rule, evidence, and proposed correction. Classify findings as mandatory or advisory, assign stable recommendation IDs, apply only approved corrections, and rerun affected checks after revision.

Present mandatory failures with the exact location, evidence, and proposed correction. Apply only approved substantive corrections. Safe, unambiguous link formatting fixes may be recorded as silent repairs.

## Step 6: Obtain approval and persist the result

[GATE: approval-before-write]

After explicit approval of the final proposed page, replace only the selected target page and save the before/after record in `Outputs/` using `[page-slug]_beforeAfter.md`. Save the execution log in `Outputs/logs/` using `YYYY-MM-DD-HHMM-claude-docs-task-page-builder.md`. Do not modify the source REBOOT workflow. Do not publish externally.

## Step 7: Verify and hand off

Re-read the first and last sections of every saved file. Confirm the exact target path and scope, front matter values, required Task sections, resolved links, source-boundary result, claim support, before/after record, execution log, and QA result. Report changed files, unresolved issues, and the exact next action. If approval was not given, report that no authoritative page was changed.
