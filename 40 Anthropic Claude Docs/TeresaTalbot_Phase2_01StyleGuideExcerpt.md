# StyleGuide for Claude Docs: Task

## Scope

This excerpt applies to task pages for Skills, Plugins, and Connectors. A task page helps a reader complete one observable job. It is not an overview, comparison, or troubleshooting reference.

## Style guide excerpt: task pages

| Rule                                          | Conformance test                                                                                                                                                                         |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name the job in the H1.                       | The H1 contains an imperative verb and one object. It is 70 characters or fewer.                                                                                                         |
| State the outcome first.                      | The first paragraph is 45 words or fewer and describes the observable result.                                                                                                            |
| Make page identity machine-readable.          | YAML front matter contains exactly one value for `content_type: task`, `object_type`, `owner_team`, `supported_surfaces`, `status`, `last_reviewed`, `canonical_url`, and `next_action`. |
| Orient before action.                         | An **At a glance** block appears before the first H2 and contains exactly `Audience`, `Prerequisites`, and `Outcome`.                                                                    |
| Put prerequisites before the procedure.       | A `Before you begin` section appears before the first numbered procedure.                                                                                                                |
| Give each step one action.                    | Every numbered step begins with an imperative verb and contains no more than one primary action.                                                                                         |
| Separate shared and conditional instructions. | Product, plan, organization, or surface differences appear under a `Product-specific` heading after the shared procedure.                                                                |
| Explain access risk.                          | A `Security and permissions` section states what access is granted and how to remove it whenever the task reads external data, executes code, installs software, or changes user state.  |
| Make failures actionable.                     | `Troubleshooting` contains a table with exactly the columns `Symptom`, `Check`, and `Fix`; every symptom has a check and a fix.                                                          |
| End with one path forward.                    | The page contains exactly one H2 named `Next steps`; its first link equals `next_action`, and it contains no more than two additional links.                                             |
| Keep examples subordinate to the job.         | Examples do not introduce a second object, alternate workflow, or unsupported capability.                                                                                                |

