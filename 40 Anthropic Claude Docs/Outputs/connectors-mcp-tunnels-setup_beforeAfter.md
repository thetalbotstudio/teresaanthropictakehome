# Before/after record — Set up an MCP tunnel

Workflow: `workflow-claude-docs-task-page-builder` v1.1 · Run: 2026-09-03 17:32 PDT · Operator: Teresa Talbot (Cowork session)

## Target manifest

| Field | Value |
|---|---|
| Target path | `Knowledge/claudedocs/Set up an MCP tunnel.md` (untouched) |
| Before snapshot | `Knowledge/claudedocs/Set up an MCP tunnel_BEFORE.md` (byte-identical copy of the target) |
| After path | `Knowledge/claudedocs/Set up an MCP tunnel_AFTER.md` |
| Canonical URL | https://claude.com/docs/connectors/mcp-tunnels/setup |
| Object type | connector |
| Observable job | An Enterprise admin deploys a tunnel and registers an internal MCP server as a custom connector that answers a tool call from Claude |
| Scope | Full page |
| Operation | Create (`_AFTER` file); the canonical target was not replaced |

## Retained context manifest

| Source | Status | Use |
|---|---|---|
| `Knowledge/claudedocs/Set up an MCP tunnel.md` (web clipping, created 2026-09-03) | Current; primary source | All prose claims, links, and the interest-form link |
| `Outputs/claudedocs-checker/snapshots/connectors-mcp-tunnels-setup.md` (raw MDX fetched 2026-09-04 00:20 UTC by the Phase 3 checker) | Current; same canonical page | Tab contents (Helm and Docker Compose steps, code blocks, warnings) that the clipping dropped |
| `Outputs/claudedocs-checker/out/connectors-mcp-tunnels-setup.findings.md` | Current | Prior QA findings against the target (12 mandatory failures) |
| `TeresaTalbot_Phase2_01StyleGuideExcerpt.md`, `TeresaTalbot_Phase2_02ContentTypeTemplate.md`, `Templates/doc-task-topic.md` | Current | Page contract |
| `Knowledge/claude-docs-audit-brief.md`, `Knowledge/knowledge.md` | Current | Scope |
| `Knowledge/claudedocs/Get started with connectors_AFTER.md` | Current | Precedent for front-matter conventions (`owner_team: Docs Platform`, `supported_surfaces: [claude.ai]`) |

Exclusions: no browsing, no product behavior beyond the two source captures. Known discrepancy: the clipping includes the interest-form link (https://claude.com/form/mcp-tunnels); the raw snapshot's Note says only "contact your Anthropic account team". Both kept, since the clipping is the supplied target.

Known uncertainties: `owner_team` is not stated by the source; the value inherits the convention set by the previous run. Live route validity for `/connectors/mcp-tunnels/oauth`, `/troubleshooting` (three anchors), `/overview`, and `/custom/remote-mcp#adding-custom-connectors` is inherited from the source page, which links all of them; they were not re-fetched.

## Source map (after → source)

| After section | Source |
|---|---|
| Front matter | Template; canonical URL from clipping `source:`; `next_action` = oauth page linked in source step 4 |
| Opening, At a glance | Rewritten from source intro paragraphs 1–2 (roles, deployment prerequisites, end-to-end tool call) |
| Before you begin | Source intro paragraphs 1–3 and "Deploy the tunnel stack" intro (Helm vs Compose, routes) |
| Create a Tunnels API key | Source section, steps 1–3 split into 4 single-action steps |
| Deploy with Helm | Snapshot Helm tab, 5 `<Step>` blocks → 7 steps; NetworkPolicy and `helm upgrade` paragraphs retained |
| Deploy with Docker Compose | Snapshot Docker Compose tab, 5 `<Step>` blocks → 10 steps; `data/` protection paragraph moved to Security and permissions |
| Verify the connection | Source section; CodeGroup rendered as labeled code blocks |
| Add tunneled servers as connectors | Source steps 1–5 plus the "connect it yourself and watch the proxy logs" sentence, now steps 7–8; "Add more servers later" retained as H3 |
| Product-specific | Source Note (research preview, Enterprise by request), "Tunnels page appears once enabled", Console-flow caveat |
| Security and permissions | Source: API key purpose, `data/` contents, `allowed_ips`, NetworkPolicy, "Rotate credentials" (condensed), "Remove a tunnel" (condensed) |
| Troubleshooting | Source: rerun-if-empty, cloudflared never registers link, hook error link, IP validation link, `TUNNEL_TOKEN` no-default note, `--reuse-values` warning, Tunnels page visibility |
| Next steps | oauth (next_action), troubleshooting, overview — all linked from the source |

## Material changes and rationale

1. **Added typed front matter** replacing clipping metadata (`title/source/author/published/created/description/tags`) — required by T3; enables ownership, freshness, and next-action checks.
2. **Opening rewritten to the observable result** (30 words, was 74 and described coverage/prerequisites) — T2a/T2b.
3. **Added At a glance and Before you begin** — T4/T5. The deployment-path decision and the route definition moved here from the "Deploy the tunnel stack" intro, because both are decisions the reader makes before running anything.
4. **Helm and Docker Compose tabs became two H2 procedures** with an explicit "follow one / skip the other" instruction. Reason: the clipping lost the tab contents entirely (the target page as saved had no deployment steps at all), and Markdown has no tabs. Both paths are reader-environment choices, not product/plan/surface differences, so they stay as shared procedure rather than under Product-specific.
5. **Every step is one imperative action.** "Open Tunnels API and create a key" split (T6b); "In claude.ai, go to…" rewritten as "Open … in claude.ai" (T6a); Docker Compose "Provision the tunnel" split into read key / run setup / read domain / revoke key / unset; "Start the stack" split into export token / start.
6. **Product-specific added** holding plan availability, the Tunnels-page visibility condition, and the Console-flow caveat — T7.
7. **Security and permissions added** (T8). It consolidates what the API key and tunnel token grant, what is stored locally, and how to limit and remove access.
8. **Rotate credentials and Remove a tunnel demoted from H2 procedures to condensed guidance under Security and permissions.** Reason: J1 (one observable job). The Phase 3 run recommended keeping this page at setup and moving rotation and removal to their own task pages. No routes exist for those pages yet, so nothing links to them; the full procedures with commands are preserved below in the before snapshot and should become `Rotate MCP tunnel credentials` and `Remove an MCP tunnel` task pages. Safety-critical content (revoke the key, 90-day certificate, archive is permanent, compromise response) is retained on this page.
9. **Troubleshooting table added** (T9) from failure conditions already stated in the source; no new failure modes invented.
10. **Next steps added** (T10) with `next_action` first and two additional links.
11. **Verification step made explicit**: the source's "connect the server yourself and ask Claude to use one of its tools" sentence became steps 7–8 of the connector procedure, so the page ends at the outcome named in At a glance.

## AI workflow actions

Loaded workspace context → resolved target and scope → assembled retained context (clipping + raw snapshot) → selected Task contract → drafted `_AFTER` → ran `Outputs/claudedocs-checker/check_task_page.py` on the draft → manual judgment review → wrote this record and the execution log.

## QA history

- Checker v0.1.0 on the target (2026-09-04 00:20 UTC): FAIL — 12 mandatory, 2 advisory.
- Checker v0.1.0 on `_AFTER` (2026-09-04 00:33 UTC): PASS — 0 mandatory, 0 advisory, 2 needs-review (T6a: "Rerun", "Ask" are imperative verbs missing from the checker's verb list — advisory list-coverage gap, not a page defect), 4 pending judgment.
- Manual judgment: T2b pass (opening states the result). J1 pass (one job: working tunneled connector; rotation/removal demoted). J2 pass (`docs`/`search` routes and the example URL illustrate the one job). J3: both T6a flags rejected.
- Gate results: target-resolved ✔ · source-boundary-resolved ✔ · source-eligibility-passed ✔ (one noted discrepancy) · task-contract-selected ✔ · task-contract-qa-passed ✔ · unsupported-claims-qa-passed ✔ · links-qa-passed ✔ (inherited from source, not re-fetched) · technical-leakage-qa-passed ✔ · reader-value-qa-passed ✔ · voice-qa-passed ✔ · before-after-qa-passed ✔ · output-paths-resolved ✔ · approval-before-write: not applicable — canonical target not replaced; `_AFTER` written on user instruction.

## Unresolved issues

1. Rotation and removal procedures need destination pages (proposed routes `/docs/connectors/mcp-tunnels/rotate-credentials`, `/docs/connectors/mcp-tunnels/remove`) before this rewrite could ship; until then the live page should keep those H2s.
2. `owner_team: Docs Platform` is a placeholder convention, not sourced.
3. Internal routes not re-fetched in this run.

## Approval state

Draft. `_AFTER` awaits Teresa's review; the canonical target page is unchanged.

## Complete before snapshot

---
title: "Set up an MCP tunnel"
source: "https://claude.com/docs/connectors/mcp-tunnels/setup"
author:
published:
created: 2026-09-03
description: "Create a Tunnels API key in claude.ai, deploy the MCP tunnel stack with Helm or Docker Compose, verify the connection, add tunneled MCP servers as custom connectors, rotate the tunnel token and certificates, and remove a tunnel."
tags:
  - "clippings"
---
MCP tunnels are in research preview and are available to organizations on the Claude Enterprise plan by request. To request access, [submit the MCP tunnels interest form](https://claude.com/form/mcp-tunnels) or contact your Anthropic account team.

This page covers the full setup of an MCP tunnel for a claude.ai Enterprise organization, from creating the API key that provisioning uses to members calling a tunneled MCP server from Claude. You need the Owner or Primary Owner role in claude.ai, and someone who can deploy containers to a Kubernetes cluster or a Docker host inside your network. Read [MCP tunnels](https://claude.com/docs/connectors/mcp-tunnels/overview) first if the tunnel stack, the tunnel domain, and routes are unfamiliar.

The deployment steps on this page are reference deployments. You are responsible for adapting them to your organization’s security requirements. For the full set of proxy options, certificate requirements, and hardening guidance, see the [MCP tunnels reference](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/reference) and [MCP tunnels security](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/security) pages in the Claude Platform docs. Those pages describe the Claude Console flow, which authenticates the setup component differently. For a claude.ai organization, follow the authentication steps on this page.

## Create a Tunnels API key

The setup component that runs alongside the tunnel stack needs a short-lived credential to create the tunnel, register its certificate authority (CA) certificate with Anthropic, and fetch the tunnel token. In claude.ai that credential is a Tunnels API key.

1. In claude.ai, go to **Organization settings > Tunnels**. This page appears once Anthropic has enabled MCP tunnels for your organization.
2. Open **Tunnels API** and create a key.
3. Copy the key somewhere safe for the next section. You pass it to the setup component once.

The tunnel stack does not use the key at runtime. Revoke the key as soon as setup completes, and create a fresh one later when you rotate the tunnel token.

## Deploy the tunnel stack

Choose Helm if you run Kubernetes. The chart provisions the tunnel, stores the credentials in a Secret, and renews the server certificate automatically. Choose Docker Compose for a single host or a VM, where you run the setup component and certificate renewal yourself.

Both paths need at least one route. A route maps a subdomain of your tunnel domain to the internal URL of an MCP server, in the form `scheme://host:port` with no path. The examples use `docs` pointing at `http://docs-mcp.example.corp:8080`. Replace them with your own servers.

- Helm
- Docker Compose

To restrict the pod’s egress at the network level, set `networkPolicy.enabled: true` in `values.yaml` and list your MCP servers under `networkPolicy.mcpServers`. The policy already allows cloudflared to reach the tunnel edge. Your cluster’s network plugin must support NetworkPolicy.

For later configuration changes such as routes or replica count, edit `values.yaml` and run `helm upgrade` with the same `--version` and `-f values.yaml`, without the API key. Keep a complete `values.yaml` rather than relying on `--reuse-values`, because Helm’s deep merge can silently keep a route you deleted.

The `data/` directory now holds the tunnel ID, tunnel domain, tunnel token, CA key pair, and server key pair. Protect it with your organization’s file-permission, encryption-at-rest, and secrets-management controls, and consider moving `ca.key` and `tunnel-token` to secure storage.

## Verify the connection

Check the logs on your side first. cloudflared logs four `Registered tunnel connection` lines when it has reached the tunnel edge, and the proxy logs one `route configured` line per route.

```shellscript
kubectl -n mcp-tunnel logs deploy/mcp-tunnel -c cloudflared | grep "Registered tunnel connection"
kubectl -n mcp-tunnel logs deploy/mcp-tunnel -c mcp-proxy | grep "route configured"
```

```shellscript
docker compose logs cloudflared | grep "Registered tunnel connection"
docker compose logs mcp-proxy | grep "route configured"
```

The containers take a few seconds to start, so rerun the commands if they come back empty. If cloudflared never registers, see [Troubleshooting](https://claude.com/docs/connectors/mcp-tunnels/troubleshooting#the-tunnel-stack-starts-but-cloudflared-never-connects). The end-to-end check happens from Claude, in the next section.

## Add tunneled servers as connectors

Each route becomes a custom connector for your organization. The connector URL is the route’s tunnel hostname plus the path your MCP server serves. Many servers serve at `/mcp`, and the proxy forwards the path unchanged.

1. In claude.ai, go to **Organization settings > Connectors**.
2. Select **Add**, then **Custom**. If Claude asks for the connector type, choose **Web**.
3. Enter the server URL, for example `https://docs.abc123.tunnel.anthropic.com/mcp`.
4. Configure authentication for the server. If its OAuth authorization server is also inside your network, turn on **Tunnel OAuth configuration** and follow [Authenticate to MCP servers behind a tunnel](https://claude.com/docs/connectors/mcp-tunnels/oauth).
5. Select **Add**.

Members then find the connector in their own connector settings and select **Connect** to sign in, as described in [Third party connectors with remote MCP](https://claude.com/docs/connectors/custom/remote-mcp#adding-custom-connectors). To confirm the tunnel end to end, connect the server yourself and ask Claude to use one of its tools while you watch the proxy logs for the request.

### Add more servers later

Add a route for the new server, apply the change, and register the new hostname as another custom connector. No certificate or cloudflared changes are needed, because the server certificate covers every subdomain of your tunnel domain.

```shellscript
# After adding the route under gateway.config.routes in values.yaml
helm upgrade mcp-tunnel \
  oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
  --version 2.0.2 \
  -n mcp-tunnel \
  -f values.yaml
```

```shellscript
# After adding the route in config/mcp-proxy.yaml
docker compose restart mcp-proxy
```

## Rotate credentials

Three credentials are involved, and each rotates differently.

**Tunnels API key.** Used only while the setup component runs. Revoke it after every use and create a new one in **Organization settings > Tunnels > Tunnels API** when you next need to run setup.

**Tunnel token.** Authenticates cloudflared’s outbound connection. Rotate it on your regular schedule and immediately if you suspect exposure. Rotation does not sever connections that are already established, so you can rotate, restart cloudflared with the new value, and let the old connections drain.

- Helm
- Docker Compose

Increment `tunnel.tokenVersion` in `values.yaml`, create a fresh Tunnels API key, and upgrade. The setup component re-runs, rotates the token, and updates the Secret.

```shellscript
read -rs API_TOKEN && export API_TOKEN

helm upgrade mcp-tunnel \
  oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
  --version 2.0.2 \
  -n mcp-tunnel \
  -f values.yaml \
  --set api.token="$API_TOKEN" \
  --set setup.force=true
```

Revoke the API key once the upgrade completes.

Edit `docker-compose.yaml` and increment the `--token-version` value in the `setup` service (for example from `1` to `2`), so the new value persists for future runs. Then create a fresh Tunnels API key and re-run setup.

```shellscript
read -rs API_TOKEN && export API_TOKEN
docker compose run --rm setup

export TUNNEL_TOKEN=$(sudo cat data/tunnel-token)
docker compose up -d cloudflared
```

Revoke the API key and run `unset API_TOKEN` once rotation completes. For a multi-host deployment, setup writes the new token only to the `data/` directory on the host where it ran, so copy the updated `data/` directory (at minimum `data/tunnel-token`) to every other host that runs a replica. Then repeat the last two commands on each of those hosts so every replica restarts with the new token.

**Server certificate.** The certificate the proxy presents is valid for 90 days, and you are responsible for renewing it before it expires. Renewal is local. It signs a new certificate with the CA already stored in your deployment, makes no API calls, and needs no API key. The proxy reloads the certificate file automatically, so no restart is required.

- Helm
- Docker Compose

The chart deploys a CronJob that runs daily and renews the certificate once it is within 30 days of expiry. Monitor the CronJob and the certificate’s expiry date to confirm renewal completes.

Run the renewal from the deployment directory. With `--renew-before=720h` the command does nothing while more than 30 days of validity remain, so it is safe to run on a schedule such as a daily cron entry.

```shellscript
docker compose run --rm setup renew-cert --output=dir:/data --renew-before=720h
```

## Remove a tunnel

Decommission a tunnel when you no longer need it, or as the first steps of responding to a suspected compromise. Archiving a tunnel invalidates its token, detaches its domain, and is permanent.

If you archived the tunnel because of a suspected compromise, also notify your Anthropic account team, rotate any OAuth tokens or secrets your MCP servers issued, and review the proxy, cloudflared, and MCP server logs for the affected period before you provision a replacement tunnel.

## After snapshot

See `Knowledge/claudedocs/Set up an MCP tunnel_AFTER.md` (identical to the reviewed draft).
