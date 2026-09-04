# Claude Docs Task Content Type Template

## Scope

This excerpt applies to task pages for Skills, Plugins, and Connectors. A task page helps a reader complete one observable job. It is not an overview, comparison, or troubleshooting reference.
### Content-type template: Task

```markdown
---
content_type: task
object_type: skill | plugin | connector
owner_team: team-name
supported_surfaces: [claude.ai, cowork]
status: draft | current | deprecated
last_reviewed: YYYY-MM-DD
canonical_url: https://claude.com/docs/...
next_action: https://claude.com/docs/...
---

# [Imperative verb] [object]

[In 45 words or fewer: state what the reader will accomplish.] 

> **At a glance**
> - Audience: [one role]
> - Prerequisites: [one short sentence]
> - Outcome: [observable result]

## Before you begin

- [Prerequisite or permission requirement]

## [Verb-led task section]

1. [Imperative step with one primary action]
2. [Imperative step with one primary action]
3. [Imperative step with one primary action]

### Product-specific

[Only conditional UI, plan, permission, or surface differences.]

## Security and permissions

[What data or state the task accesses, what the user authorizes, and how to remove access or undo the change.]

## Troubleshooting

| Symptom | Check | Fix |
|---|---|---|
| [Observable failure] | [Diagnostic check] | [Corrective action] |

## Next steps

[Primary action link matching `next_action`]
```

