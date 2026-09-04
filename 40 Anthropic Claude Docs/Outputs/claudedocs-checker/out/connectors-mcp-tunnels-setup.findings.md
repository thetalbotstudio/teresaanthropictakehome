# Task-page check: https://claude.com/docs/connectors/mcp-tunnels/setup

- Run: 2026-09-04T00:20:43+00:00  ·  checker v0.1.0  ·  standard: TeresaTalbot_Phase2_01StyleGuideExcerpt.md
- Input: local file snapshots/connectors-mcp-tunnels-setup.md
- Result: **FAIL** — 12 mandatory failures, 2 advisory, 0 needs-review, 0 pending judgment

| ID | Class | Sev | Status | Rule | Location | Evidence |
|---|---|---|---|---|---|---|
| T1a | deterministic | mandatory | pass | H1 is 70 characters or fewer | line 1 | 20 chars: 'Set up an MCP tunnel' |
| T1b | heuristic | mandatory | pass | H1 begins with an imperative verb | line 1 | first word 'set' |
| T2a | deterministic | mandatory | fail | First paragraph is 45 words or fewer | first paragraph after H1 | 74 words: 'This page covers the full setup of an MCP tunnel for a claude.ai Enterprise organization, from creating the API key that provisioning uses to members calling a '… |
| T2b | judgment | mandatory | fail | First paragraph describes the observable result | first paragraph after H1 | The first paragraph describes coverage and prerequisites ('This page covers the full setup ... You need the Owner or Primary Owner role ...'), not the observable result. The Mintlify description blockquote above it is a  |
| T3 | deterministic | mandatory | fail | Front matter contains exactly one value for each required key | front matter | missing: ['content_type', 'object_type', 'owner_team', 'supported_surfaces', 'status', 'last_reviewed', 'canonical_url', 'next_action'] (no YAML front matter at all) |
| T4 | deterministic | mandatory | fail | At a glance block appears before the first H2 with exactly Audience, Prerequisites, Outcome | before first H2 | no 'At a glance' block found |
| T5 | deterministic | mandatory | fail | Before you begin appears before the first numbered procedure | first step at line 15 | no 'Before you begin' H2 |
| T6a | heuristic | mandatory | fail | Step begins with an imperative verb | Create a Tunnels API key step 1 (line 15) | In claude.ai, go to **Organization settings > Tunnels**. This page appears once Anthropic has enabled MCP tunnels for your organization. |
| T6b | heuristic | mandatory | fail | Step contains no more than one primary action | Create a Tunnels API key step 2 (line 16) | second action ['create']: 'Open **Tunnels API** and create a key.' |
| T6a | heuristic | mandatory | fail | Step begins with an imperative verb | Add tunneled servers as connectors step 1 (line 135) | In claude.ai, go to **Organization settings > Connectors**. |
| T7 | heuristic | advisory | fail | Product, plan, organization, or surface differences appear under Product-specific after the shared procedure | document | conditional content without a Product-specific heading — tabs: ['Docker Compose', 'Helm'], markers: ['Enterprise plan', 'Organization settings'] |
| T8 | deterministic | mandatory | fail | Security and permissions section states what access is granted and how to remove it | document | page reads data / installs / handles credentials (['api key', 'credential', 'deploy', 'install', 'oauth', 'permission']) but has no 'Security and permissions' H2 |
| T9 | deterministic | mandatory | fail | Troubleshooting contains a table with exactly Symptom, Check, Fix | document | no 'Troubleshooting' H2 |
| T10 | deterministic | mandatory | fail | Exactly one H2 named Next steps; first link equals next_action; at most two more links | document | 0 'Next steps' H2 found |
| J1 | judgment | mandatory | fail | Page helps a reader complete ONE observable job (task-contract-selected) | document | The page bundles at least three reader jobs. Set up (H2s 'Create a Tunnels API key', 'Deploy the tunnel stack', 'Verify the connection', 'Add tunneled servers as connectors') is one job with one outcome: a tunneled serve |
| J2 | judgment | advisory | pass | Examples do not introduce a second object, alternate workflow, or unsupported capability | examples | Examples stay inside the one job: the 'docs' and 'search' routes, the example URL 'https://docs.abc123.tunnel.anthropic.com/mcp', and the example tunnel domain all illustrate configuring and registering a route. No examp |
| J3 | judgment | advisory | fail | Heuristic T6 findings confirmed (imperative verb / one action per step) | steps | 1 confirmed, 2 rejected. Confirmed: 'Create a Tunnels API key' step 2 'Open **Tunnels API** and create a key' has two primary actions. Rejected: step 1 (line 15) and 'Add tunneled servers as connectors' step 1 (line 135) |

## Proposed fixes

- **T2a** first paragraph after H1: Open with one paragraph of 45 words or fewer that states the observable result.
- **T2b** first paragraph after H1: Open with the result: 'After this task, members of your claude.ai Enterprise organization can use an MCP server inside your network as a custom connector, reached through a tunnel you control.'
- **T3** front matter: Add typed front matter: content_type, object_type, owner_team, supported_surfaces, status, last_reviewed, canonical_url, next_action.
- **T4** before first H2: Add a blockquote 'At a glance' with exactly Audience, Prerequisites, and Outcome.
- **T5** first step at line 15: Add a Before you begin section listing roles, access, and inputs the reader needs.
- **T6a** Create a Tunnels API key step 1 (line 15): Start the step with the action verb.
- **T6b** Create a Tunnels API key step 2 (line 16): Split into one step per action, or demote the second clause to a result sentence.
- **T6a** Add tunneled servers as connectors step 1 (line 135): Start the step with the action verb.
- **T7** document: Move plan/org/surface conditions under a Product-specific heading; keep the shared procedure unconditional.
- **T8** document: Add a Security and permissions H2 that consolidates access granted, revocation, and removal.
- **T9** document: Add a Troubleshooting H2 with a Symptom | Check | Fix table.
- **T10** document: Add one Next steps H2 whose first link is next_action.
- **J1** document: Keep this page as 'Set up an MCP tunnel' ending at the first successful tool call; move 'Rotate credentials' and 'Remove a tunnel' to their own task pages under connectors/mcp-tunnels and link them from Next steps.
- **J3** steps: Allow a leading location phrase in T6a; extend T6b to the first sentence of a <Step> body, not only its title.
