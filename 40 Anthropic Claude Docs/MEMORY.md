# Memory — 40 Anthropic Claude Docs

## Project Context
- **Goal:** A completed, submitted Anthropic take-home project (audit memo → standards → automated checker → adoption plan).
- **Domain:** Technical content engineering — Claude Docs (claude.com/docs), specifically Skills, Plugins, and Connectors; content standards, templates, and docs-quality tooling.
- **Key people:** Not specified
- **Brief:** `Knowledge/claude-docs-audit-brief.md` (source: `31 The Talbot Studio/Outputs/claudeDocsAudit/ClaudeDocsAuditInstructions.md`)

## Brief Summary
- **Role framing:** owner of the unification and standardization layer across Claude Docs — architecture, standards, systems that keep quality high, pruning and curating.
- **Scope:** Claude Docs = docs for Claude's apps (Connectors, Cowork, Claude for M365, Plugins, Claude Tag, Skills). Audit focus: Skills, Plugins, Connectors. Excluded: platform.claude.com/docs, code.claude.com/docs.
- **Corpus index:** `claude.com/docs/llms.txt` gives the full page index.
- **Phase 1 — Audit:** short memo: what's wrong, prioritized; what to delete/merge and what happens to readers on those URLs; proposed IA for Skills/Plugins/Connectors and the path to get there; what to measure and how to instrument it. Be opinionated.
- **Phase 2 — Standards:** style-guide excerpt + one content-type template that would have prevented Phase 1 problems; apply to one existing page (before/after + note on what changed and why). Rules must be applicable the same way twice by a reviewer or a machine.
- **Phase 3 — System:** working prototype of an automated check against the real docs flagging one problem class from Phase 1. Deliver GitHub link + output on the real corpus (including false positives) + how to evaluate the checker: FP tolerance and why, degradation detection, staleness prevention.
- **Phase 4 — Adoption:** a few paragraphs on getting adoption from product teams that don't report to you, including the team that ignores the system.
- **Submission:** P1 memo (markdown/PDF/in GitHub); P2 style-guide excerpt, template, before/after (markdown or in GitHub); P3 GitHub link + run output; P4 a few paragraphs max.

## Key Decisions
- 2026-09-03: Workspace name kept as `40 Anthropic Claude Docs` to match the folder (three words; bends the two-word guideline).
- 2026-09-03: Skill prefix `claudedocs-`.

## Notes to Remember
<!-- Added when you say "remember this" -->
