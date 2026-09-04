
You will find the system I used to generate clean tasks files in: //40 Anthropic Claude Docs/

To run a check on a Claude Docs task page, enter: run workflow-claude-docs-task-page-builder on [URL].

My workflow system got two things wrong: it referenced files that don’t exist under the names it specified, and its checker flagged “Authenticate” as a possible non-imperative step even though it clearly is one.

I’d evaluate this workflow system against a labeled set of real pages, measuring unsupported-claim escapes, false positives, reviewer rework, and whether readers can complete the task. I’d tolerate up to 10% false positives for ordinary structural checks because some friction is acceptable if the system catches real defects, but I’d set near-zero tolerance for security or unsupported-claim flags. I’d know it had degraded if false positives, missed issues, or reviewer overrides increased across the same types of pages, or if results changed without a corresponding workflow change.

To keep it from becoming another stale artifact, I’d assign an owner, version the workflow and checker, run it against the live corpus on a schedule, track `last_reviewed`, and require fresh results before major documentation releases.

Folders of interest:
-40 Anthropic Claude Docs/Outputs
--40 Anthropic Claude Docs/Outputs/claudedocs-checker
-40 Anthropic Claude Docs/Templates
-40 Anthropic Claude Docs/Workflows
