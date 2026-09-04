# Claude Docs Workflow

## Scope

This excerpt applies to task pages for Skills, Plugins, and Connectors. A task page helps a reader complete one observable job. It is not an overview, comparison, or troubleshooting reference.

## AI workflow applied

Workflow: [[Users/teresamtalbot/Documents/TheTalbotStudio/Work OS/40 Anthropic Claude Docs/Workflows/workflow-claude-docs-task-page-builder|workflow-claude-docs-task-page-builder]]. 

1. Load the target workspace instructions, memory and the source page.
2. Classify the target as a `task` page.
3. Extract steps in the source page. Where the source is conditional, the rewrite labels as condition instead of presenting it as universal.
4. Rebuilt the page with the [[doc-task-topic]].
5. Check metadata, heading structure, step verbs, permissions guidance, troubleshooting columns, and the single next action.
