# Claude Docs Workflow

## Scope

This excerpt applies to task pages for Skills, Plugins, and Connectors. A task page helps a reader complete one observable job. It is not an overview, comparison, or troubleshooting reference.

## What changed and why

- Replaced the vague title and opening with the single job: connect a service and use its data.
- Replaced clipping metadata with a typed contract that can support ownership, surface, freshness, and next-action checks.
- Added the required three-field orientation block so readers can identify audience, prerequisites, and result before scanning the procedure.
- Consolidated setup into one numbered procedure. Each step starts with an imperative verb and has one primary action.
- Moved project instructions into a labeled `Product-specific` section so conditional UI does not look universal.
- Added explicit permission review and disconnect guidance because connectors read external data and can change authorization state.
- Converted the unlabeled troubleshooting fragments into a repeatable symptom/check/fix table.
- Added one canonical next action. The page now has a clear continuation without competing navigation.

## Verification notes

- The rewritten target has `content_type: task` and `object_type: connector`.
- The H1 is 27 characters and names one job.
- The opening paragraph is 19 words.
- The At a glance block contains exactly three fields.
- The page has one `Next steps` H2 and its first link matches `next_action`.
- No claim was added for connectors beyond the supplied source text. The source's plan and organization variability is retained as a condition.
