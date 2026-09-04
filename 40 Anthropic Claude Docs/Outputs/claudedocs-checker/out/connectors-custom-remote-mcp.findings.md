# Task-page check: https://claude.com/docs/connectors/custom/remote-mcp

- Run: 2026-09-04T00:54:30+00:00  ·  checker v0.1.0  ·  standard: TeresaTalbot_Phase2_01StyleGuideExcerpt.md
- Input: local file snapshots/connectors-custom-remote-mcp.md
- Result: **FAIL** — 8 mandatory failures, 1 advisory, 3 needs-review, 4 pending judgment

| ID | Class | Sev | Status | Rule | Location | Evidence |
|---|---|---|---|---|---|---|
| T1a | deterministic | mandatory | pass | H1 is 70 characters or fewer | line 1 | 38 chars: 'Third party connectors with remote MCP' |
| T1b | heuristic | mandatory | needs-review | H1 begins with an imperative verb | line 1 | first word 'third' |
| T2a | deterministic | mandatory | pass | First paragraph is 45 words or fewer | first paragraph after H1 | 21 words: 'Custom connectors enable you to link Claude directly to your essential tools and data sources using the Model Context Protocol (MCP).'… |
| T2b | judgment | mandatory | pending | First paragraph describes the observable result | first paragraph after H1 | Custom connectors enable you to link Claude directly to your essential tools and data sources using the Model Context Protocol (MCP). |
| T3 | deterministic | mandatory | fail | Front matter contains exactly one value for each required key | front matter | missing: ['content_type', 'object_type', 'owner_team', 'supported_surfaces', 'status', 'last_reviewed', 'canonical_url', 'next_action'] (no YAML front matter at all) |
| T4 | deterministic | mandatory | fail | At a glance block appears before the first H2 with exactly Audience, Prerequisites, Outcome | before first H2 | no 'At a glance' block found |
| T5 | deterministic | mandatory | fail | Before you begin appears before the first numbered procedure | first step at line 30 | no 'Before you begin' H2 |
| T6a | heuristic | mandatory | needs-review | Step begins with an imperative verb | For Team and Enterprise plans step 4 (line 33) | first word 'optionally': Optionally configure OAuth Client ID/Secret in Advanced settings |
| T6a | heuristic | mandatory | needs-review | Step begins with an imperative verb | For Free, Pro, and Max plans step 4 (line 49) | first word 'optionally': Optionally configure OAuth credentials |
| T6a | heuristic | mandatory | fail | Step begins with an imperative verb | Adding a request header step 1 (line 94) | In the Add custom connector dialog, open **Request headers**. |
| T6b | heuristic | mandatory | fail | Step contains no more than one primary action | Adding a request header step 5 (line 98) | second action ['click']: 'Repeat for any additional headers your server needs (you can add up to four), then click **Add**.' |
| T7 | heuristic | advisory | fail | Product, plan, organization, or surface differences appear under Product-specific after the shared procedure | document | conditional content without a Product-specific heading — tabs: [], markers: ['Organization settings'] |
| T8 | deterministic | mandatory | fail | Security and permissions section states what access is granted and how to remove it | document | page reads data / installs / handles credentials (['api key', 'credential', 'deploy', 'oauth', 'permission', 'secret']) but has no 'Security and permissions' H2 |
| T9 | deterministic | mandatory | fail | Troubleshooting contains a table with exactly Symptom, Check, Fix | document | no 'Troubleshooting' H2 |
| T10 | deterministic | mandatory | fail | Exactly one H2 named Next steps; first link equals next_action; at most two more links | document | 0 'Next steps' H2 found |
| J1 | judgment | mandatory | pending | Page helps a reader complete ONE observable job (task-contract-selected) | document | H2s: ['What are third party connectors?', 'Adding custom connectors', 'The Add custom connector dialog, field by field', 'Authenticating with request headers', 'Managing connectors', 'Security and privacy', 'Reporting is |
| J2 | judgment | advisory | pending | Examples do not introduce a second object, alternate workflow, or unsupported capability | examples |  |
| J3 | judgment | advisory | pending | Heuristic T6 findings confirmed (imperative verb / one action per step) | steps |  |

## Proposed fixes

- **T3** front matter: Add typed front matter: content_type, object_type, owner_team, supported_surfaces, status, last_reviewed, canonical_url, next_action.
- **T4** before first H2: Add a blockquote 'At a glance' with exactly Audience, Prerequisites, and Outcome.
- **T5** first step at line 30: Add a Before you begin section listing roles, access, and inputs the reader needs.
- **T6a** Adding a request header step 1 (line 94): Start the step with the action verb.
- **T6b** Adding a request header step 5 (line 98): Split into one step per action, or demote the second clause to a result sentence.
- **T7** document: Move plan/org/surface conditions under a Product-specific heading; keep the shared procedure unconditional.
- **T8** document: Add a Security and permissions H2 that consolidates access granted, revocation, and removal.
- **T9** document: Add a Troubleshooting H2 with a Symptom | Check | Fix table.
- **T10** document: Add one Next steps H2 whose first link is next_action.
