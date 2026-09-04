# Task-page check: https://claude.com/docs/connectors/custom/remote-mcp

- Run: 2026-09-04T00:57:15+00:00  ·  checker v0.1.0  ·  standard: TeresaTalbot_Phase2_01StyleGuideExcerpt.md
- Input: local file ../../Knowledge/claudedocs/Third party connectors with remote MCP_AFTERCLAUDE.md
- Result: **PASS** — 0 mandatory failures, 0 advisory, 0 needs-review, 0 pending judgment

| ID | Class | Sev | Status | Rule | Location | Evidence |
|---|---|---|---|---|---|---|
| T1a | deterministic | mandatory | pass | H1 is 70 characters or fewer | line 2 | 46 chars: 'Add a custom connector for a remote MCP server' |
| T1b | heuristic | mandatory | pass | H1 begins with an imperative verb | line 2 | first word 'add' |
| T2a | deterministic | mandatory | pass | First paragraph is 45 words or fewer | first paragraph after H1 | 33 words: 'After this task, a remote MCP server of your choosing is registered in Claude as a custom connector, its sign-in method is set, and its tools can be turned on i'… |
| T2b | judgment | mandatory | pass | First paragraph describes the observable result | first paragraph after H1 | 'After this task, a remote MCP server of your choosing is registered in Claude as a custom connector, its sign-in method is set, and its tools can be turned on in a conversation.' States the end state, not coverage. |
| T3 | deterministic | mandatory | pass | Front matter contains exactly one value for each required key | front matter | missing: [] |
| T4 | deterministic | mandatory | pass | At a glance block has exactly Audience, Prerequisites, Outcome | At a glance block | fields: ['Audience', 'Prerequisites', 'Outcome'] |
| T5 | deterministic | mandatory | pass | Before you begin appears before the first numbered procedure | line 11 | Before you begin at 11, first step at 22 |
| T7 | deterministic | advisory | pass | Product-specific heading present | line 60 | Product-specific |
| T8 | deterministic | mandatory | pass | Security and permissions section present | line 67 |  |
| T9 | deterministic | mandatory | pass | Troubleshooting table has exactly Symptom, Check, Fix and every row is complete | line 79 | columns: ['Symptom', 'Check', 'Fix']; incomplete rows: 0 |
| T10 | deterministic | mandatory | pass | Next steps: first link equals next_action; at most two more links | line 92 | links: ['https://claude.com/docs/connectors/building/troubleshooting', 'https://claude.com/docs/connectors/building/authentication', 'https://claude.com/docs/connectors/directory']; next_action: https://claude.com/docs/c |
| J1 | judgment | mandatory | pass | Page helps a reader complete ONE observable job (task-contract-selected) | document | H2s 'Add the connector' and 'Connect and turn on the connector' are two halves of one job (a custom connector that is usable in chat); 'Add a request header' is a conditional sub-procedure inside the same dialog. Concept |
| J2 | judgment | advisory | pass | Examples do not introduce a second object, alternate workflow, or unsupported capability | examples | Examples are the URL 'https://mcp.example.com/mcp' and the 'Bearer your-token' header value; both illustrate fields the reader fills in for this job. No second object or alternate workflow. |
| J3 | judgment | advisory | pass | Heuristic T6 findings confirmed (imperative verb / one action per step) | steps | 0 confirmed, 0 rejected; no T6 flags were raised. |

## Proposed fixes

