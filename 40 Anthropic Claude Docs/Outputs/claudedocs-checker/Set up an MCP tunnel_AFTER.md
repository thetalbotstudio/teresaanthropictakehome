---
content_type: task
object_type: connector
owner_team: Docs Platform
supported_surfaces: [claude.ai]
status: current
last_reviewed: 2026-09-03
canonical_url: https://claude.com/docs/connectors/mcp-tunnels/setup
next_action: https://claude.com/docs/connectors/mcp-tunnels/oauth
---

# Set up an MCP tunnel

After this task, members of your claude.ai Enterprise organization can use an MCP server inside your network as a custom connector, reached through a tunnel that you deploy and control.

> **At a glance**
> - Audience: claude.ai Owners or Primary Owners, working with whoever deploys containers in your network
> - Prerequisites: MCP tunnels enabled for your organization, and a Kubernetes cluster or Docker host that can reach your MCP servers
> - Outcome: A tunneled MCP server is registered as a custom connector and answers a tool call from Claude

## Before you begin

- Confirm that Anthropic has enabled MCP tunnels for your organization. See [Product-specific](#product-specific) for availability.
- Confirm that you have the Owner or Primary Owner role in claude.ai.
- Read [MCP tunnels](https://claude.com/docs/connectors/mcp-tunnels/overview) if the tunnel stack, the tunnel domain, or routes are unfamiliar.
- Choose one deployment path. Use Helm if you run Kubernetes: the chart provisions the tunnel, stores the credentials in a Secret, and renews the server certificate automatically. Use Docker Compose for a single host or a VM, where you run the setup component and certificate renewal yourself.
- Identify at least one route. A route maps a subdomain of your tunnel domain to the internal URL of an MCP server, in the form `scheme://host:port` with no path. The examples on this page use `docs` pointing at `http://docs-mcp.example.corp:8080`. Replace them with your own servers.
- Review the deployments on this page against your organization's security requirements. They are reference deployments, and you are responsible for adapting them. For proxy options, certificate requirements, and hardening guidance, see the [MCP tunnels reference](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/reference) and [MCP tunnels security](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/security) pages in the Claude Platform docs.

## Create a Tunnels API key

The setup component that runs alongside the tunnel stack needs a short-lived credential to create the tunnel, register its certificate authority (CA) certificate with Anthropic, and fetch the tunnel token. In claude.ai that credential is a Tunnels API key.

1. Open **Organization settings > Tunnels** in claude.ai. This page appears once Anthropic has enabled MCP tunnels for your organization.
2. Open **Tunnels API**.
3. Create a key.
4. Copy the key somewhere safe. You pass it to the setup component once.

The tunnel stack does not use the key at runtime. You revoke it as soon as setup completes, and create a fresh one later when you rotate the tunnel token.

## Deploy with Helm

Follow this section if you run Kubernetes. Otherwise, skip to [Deploy with Docker Compose](#deploy-with-docker-compose).

1. Fetch the default values. The file includes comments explaining each field.

   ```bash
   helm show values \
     oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
     --version 2.0.2 > values.yaml
   ```

2. Edit `values.yaml` so that `gateway.config.routes` lists one entry per MCP server. Leave `tunnel.id` empty so the setup component creates the tunnel during install.

   ```yaml
   tunnel:
     id: ""
     # Increment to rotate the tunnel token on a later upgrade.
     tokenVersion: "1"

   gateway:
     config:
       routes:
         docs: http://docs-mcp.example.corp:8080
         search: http://10.0.12.7:9000
   ```

   With these routes, Claude reaches the servers at `docs.<your-tunnel-domain>` and `search.<your-tunnel-domain>`. If a route targets an address outside the RFC 1918 private ranges, add the range under `gateway.config.upstream.allowed_ips` (see [Troubleshooting](#troubleshooting)).

3. Render the chart with a placeholder key. Review the output according to your organization's practices for third-party manifests. Rendering makes no API calls.

   ```bash
   helm template mcp-tunnel \
     oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
     --version 2.0.2 \
     -n mcp-tunnel \
     -f values.yaml \
     --set api.token=placeholder > rendered.yaml
   ```

4. Read the Tunnels API key into an environment variable so it stays out of your shell history and values file.

   ```bash
   # Paste the Tunnels API key (input is hidden)
   read -rs API_TOKEN && export API_TOKEN
   ```

5. Install the chart into a dedicated namespace. The setup component runs as a pre-install hook, so `helm install` blocks until the tunnel is created, the CA is registered, and the credentials are stored in the `mcp-tunnel` Secret.

   ```bash
   helm install mcp-tunnel \
     oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
     --version 2.0.2 \
     --namespace mcp-tunnel --create-namespace \
     -f values.yaml \
     --set api.token="$API_TOKEN"
   ```

6. Revoke the Tunnels API key in **Organization settings > Tunnels > Tunnels API** as soon as the install completes. Helm records `--set` values in its release history Secrets, and Kubernetes Secrets are not encrypted at rest by default, so the key remains recoverable from the cluster until you revoke it.

7. Read the tunnel domain. You need it to add connectors later. The value looks like `abc123.tunnel.anthropic.com`.

   ```bash
   kubectl -n mcp-tunnel get secret mcp-tunnel \
     -o jsonpath='{.data.tunnel-domain}' | base64 -d
   ```

To restrict the pod's egress at the network level, set `networkPolicy.enabled: true` in `values.yaml` and list your MCP servers under `networkPolicy.mcpServers`. The policy already allows cloudflared to reach the tunnel edge. Your cluster's network plugin must support NetworkPolicy.

For later configuration changes such as routes or replica count, edit `values.yaml` and run `helm upgrade` with the same `--version` and `-f values.yaml`, without the API key. Keep a complete `values.yaml` rather than relying on `--reuse-values`, because Helm's deep merge can silently keep a route you deleted.

## Deploy with Docker Compose

Follow this section for a single host or a VM. Skip it if you deployed with Helm.

1. Prepare the deployment directory. The containers run as the non-root user ID `65532` and need write access to `data/`.

   ```bash
   mkdir -p mcp-tunnel/{config,data}
   cd mcp-tunnel
   sudo chown 65532:65532 data
   ```

2. Write `docker-compose.yaml`. The compose file pins images by digest, runs every container as non-root with a read-only filesystem, drops all Linux capabilities, and disables privilege escalation.

   ```bash
   cat > docker-compose.yaml <<'EOF'
   services:
     # One-time provisioning. Run with: docker compose run --rm setup
     setup:
       image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:efb27b299d627e4134815663cb8896641eeaee025d734c0f695582b4df38f013
       entrypoint: ["/setup"]
       command:
         - init
         - --api-url=https://api.anthropic.com
         - --output=dir:/data
         - --token-version=1
       environment:
         - API_TOKEN
       volumes:
         - ./data:/data
       user: "65532:65532"
       read_only: true
       security_opt:
         - no-new-privileges:true
       cap_drop:
         - ALL
       profiles: ["setup"]

     cloudflared:
       image: cloudflare/cloudflared@sha256:6b599ca3e974349ead3286d178da61d291961182ec3fe9c505e1dd02c8ac31b0
       command: tunnel --no-autoupdate run --url http://localhost:8080
       environment:
         - TUNNEL_TOKEN
       # Share the proxy's network namespace so localhost:8080 reaches it.
       network_mode: "service:mcp-proxy"
       restart: unless-stopped
       user: "65532:65532"
       read_only: true
       security_opt:
         - no-new-privileges:true
       cap_drop:
         - ALL
       stop_grace_period: 30s
       logging:
         options:
           max-size: "10m"
           max-file: "3"

     mcp-proxy:
       image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:efb27b299d627e4134815663cb8896641eeaee025d734c0f695582b4df38f013
       volumes:
         - ./config/mcp-proxy.yaml:/etc/mcp-gateway/config.yaml:ro
         - ./data:/data:ro
       restart: unless-stopped
       user: "65532:65532"
       read_only: true
       security_opt:
         - no-new-privileges:true
       cap_drop:
         - ALL
       # Match shutdown_timeout in the proxy config
       stop_grace_period: 30s
       logging:
         options:
           max-size: "10m"
           max-file: "3"
   EOF
   ```

3. Read the Tunnels API key into an environment variable.

   ```bash
   # Paste the Tunnels API key (input is hidden)
   read -rs API_TOKEN && export API_TOKEN
   ```

4. Run the setup component. It creates the tunnel, generates the CA and server certificate, registers the CA with Anthropic, fetches the tunnel token, and writes everything to `data/`.

   ```bash
   docker compose run --rm setup
   ```

5. Read the tunnel domain into an environment variable for the next steps.

   ```bash
   export TUNNEL_DOMAIN=$(sudo cat data/tunnel-domain)
   echo "$TUNNEL_DOMAIN"
   ```

6. Revoke the Tunnels API key in **Organization settings > Tunnels > Tunnels API** before continuing. The stack does not need the key at runtime.

7. Run `unset API_TOKEN`.

8. Write the proxy config. `tunnel_domain` is required so the proxy can strip the domain from incoming hostnames and look up the remaining subdomain in `routes`. `routes` is a map, not a list.

   ```bash
   cat > config/mcp-proxy.yaml <<EOF
   listen_addr: ":8080"
   log_level: info
   shutdown_timeout: 30s
   tunnel_domain: ${TUNNEL_DOMAIN}
   tls:
     cert_file: /data/tls.crt
     key_file: /data/tls.key
   routes:
     docs: http://docs-mcp.example.corp:8080
     search: http://10.0.12.7:9000
   upstream:
     allowed_ips:
       - 10.0.0.0/8
   EOF
   ```

   `upstream.allowed_ips` is the proxy's protection against server-side request forgery. Use the narrowest ranges that cover your MCP servers. Setting it replaces the RFC 1918 default rather than extending it.

9. Export the tunnel token. The compose file reads `TUNNEL_TOKEN` from the host environment with no default, so repeat this export in every fresh shell and after a reboot.

   ```bash
   export TUNNEL_TOKEN=$(sudo cat data/tunnel-token)
   ```

10. Start the stack.

    ```bash
    docker compose up -d
    ```

For a multi-host deployment, copy the `mcp-tunnel/` directory to each host and start it the same way. The same tunnel token and certificates work across all replicas.

## Verify the connection

1. Check the logs on your side. cloudflared logs four `Registered tunnel connection` lines when it has reached the tunnel edge, and the proxy logs one `route configured` line per route.

   Helm:

   ```bash
   kubectl -n mcp-tunnel logs deploy/mcp-tunnel -c cloudflared | grep "Registered tunnel connection"
   kubectl -n mcp-tunnel logs deploy/mcp-tunnel -c mcp-proxy | grep "route configured"
   ```

   Docker Compose:

   ```bash
   docker compose logs cloudflared | grep "Registered tunnel connection"
   docker compose logs mcp-proxy | grep "route configured"
   ```

2. Rerun the commands if they come back empty. The containers take a few seconds to start.

The end-to-end check happens from Claude, at the end of the next section.

## Add tunneled servers as connectors

Each route becomes a custom connector for your organization. The connector URL is the route's tunnel hostname plus the path your MCP server serves. Many servers serve at `/mcp`, and the proxy forwards the path unchanged.

1. Open **Organization settings > Connectors** in claude.ai.
2. Select **Add**.
3. Select **Custom**. If Claude asks for the connector type, choose **Web**.
4. Enter the server URL, for example `https://docs.abc123.tunnel.anthropic.com/mcp`.
5. Configure authentication for the server. If its OAuth authorization server is also inside your network, turn on **Tunnel OAuth configuration** and follow [Authenticate to MCP servers behind a tunnel](https://claude.com/docs/connectors/mcp-tunnels/oauth).
6. Select **Add**.
7. Connect the server from your own connector settings. Members find the connector in their own connector settings and select **Connect** to sign in, as described in [Third party connectors with remote MCP](https://claude.com/docs/connectors/custom/remote-mcp#adding-custom-connectors).
8. Ask Claude to use one of the server's tools while you watch the proxy logs for the request. A logged request confirms the tunnel end to end.

### Add more servers later

No certificate or cloudflared changes are needed for a new server, because the server certificate covers every subdomain of your tunnel domain.

1. Add a route for the new server, under `gateway.config.routes` in `values.yaml` (Helm) or under `routes` in `config/mcp-proxy.yaml` (Docker Compose).
2. Apply the change.

   Helm:

   ```bash
   helm upgrade mcp-tunnel \
     oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
     --version 2.0.2 \
     -n mcp-tunnel \
     -f values.yaml
   ```

   Docker Compose:

   ```bash
   docker compose restart mcp-proxy
   ```

3. Register the new hostname as another custom connector, using the steps above.

### Product-specific

- MCP tunnels are in research preview and are available to organizations on the Claude Enterprise plan by request. To request access, [submit the MCP tunnels interest form](https://claude.com/form/mcp-tunnels) or contact your Anthropic account team. **Organization settings > Tunnels** appears only after Anthropic has enabled MCP tunnels for your organization.
- The Claude Platform pages linked under [Before you begin](#before-you-begin) describe the Claude Console flow, which authenticates the setup component differently. For a claude.ai organization, follow the authentication steps on this page.

## Security and permissions

**What this task grants.** The Tunnels API key lets the setup component create a tunnel, register your CA certificate with Anthropic, and fetch the tunnel token. The tunnel token authenticates cloudflared's outbound connection from your network. Each custom connector lets members who connect it reach the MCP server behind that route from Claude.

**What is stored on your side.** After setup, the `mcp-tunnel` Secret (Helm) or the `data/` directory (Docker Compose) holds the tunnel ID, tunnel domain, tunnel token, CA key pair, and server key pair. Protect it with your organization's file-permission, encryption-at-rest, and secrets-management controls, and consider moving `ca.key` and `tunnel-token` to secure storage.

**How to limit exposure.**

- Revoke the Tunnels API key after every use. It is not needed at runtime.
- Keep `upstream.allowed_ips` (Docker Compose) or `gateway.config.upstream.allowed_ips` (Helm) to the narrowest ranges that cover your MCP servers.
- Turn on `networkPolicy` (Helm) to restrict the pod's egress.
- Rotate the tunnel token on your regular schedule and immediately if you suspect exposure. Rotation does not sever established connections. On Helm, increment `tunnel.tokenVersion` and upgrade with a fresh Tunnels API key and `--set setup.force=true`; on Docker Compose, increment `--token-version` in the `setup` service, re-run setup with a fresh key, and restart cloudflared with the new token.
- Renew the server certificate before it expires. It is valid for 90 days, and renewal is local and needs no API key. The Helm chart deploys a daily CronJob that renews within 30 days of expiry; on Docker Compose, run `docker compose run --rm setup renew-cert --output=dir:/data --renew-before=720h` on a schedule.

**How to remove access.** Removing a custom connector in **Organization settings > Connectors** stops members from reaching that server. To decommission the tunnel itself, record the tunnel ID, stop the tunnel stack (`helm uninstall mcp-tunnel -n mcp-tunnel` or `docker compose down`), remove the connectors that point at its hostnames, archive the tunnel with the [archive endpoint](https://platform.claude.com/docs/en/api/beta/tunnels/archive) of the Tunnels API using a fresh Tunnels API key, and delete the stored credentials. Archiving invalidates the token, detaches the domain, and is permanent. If you are responding to a suspected compromise, use `docker compose down --timeout 0` to sever the connection immediately, notify your Anthropic account team, rotate any OAuth tokens or secrets your MCP servers issued, and review the proxy, cloudflared, and MCP server logs for the affected period before you provision a replacement tunnel.

## Troubleshooting

| Symptom | Check | Fix |
|---|---|---|
| **Organization settings > Tunnels** does not appear. | Confirm whether Anthropic has enabled MCP tunnels for your organization. | Request access through the interest form or your Anthropic account team. |
| The log commands return nothing. | Confirm that the containers have finished starting. They take a few seconds. | Rerun the log commands. |
| cloudflared never logs `Registered tunnel connection`. | Check the cloudflared logs for connection errors. | Follow [The tunnel stack starts but cloudflared never connects](https://claude.com/docs/connectors/mcp-tunnels/troubleshooting#the-tunnel-stack-starts-but-cloudflared-never-connects). |
| `helm install` fails with a hook error. | Check the output of the setup pre-install hook. | Follow [Helm install fails with a hook error](https://claude.com/docs/connectors/mcp-tunnels/troubleshooting#helm-install-fails-with-a-hook-error). |
| The proxy logs `IP validation failed`. | Check whether the route targets an address outside the RFC 1918 private ranges. | Add the range under `gateway.config.upstream.allowed_ips` (Helm) or `upstream.allowed_ips` (Docker Compose), as described in [Proxy logs IP validation failed](https://claude.com/docs/connectors/mcp-tunnels/troubleshooting#proxy-logs-ip-validation-failed). |
| cloudflared does not start after a reboot or in a new shell (Docker Compose). | Check whether `TUNNEL_TOKEN` is set in the current shell. | Run `export TUNNEL_TOKEN=$(sudo cat data/tunnel-token)`, then `docker compose up -d`. |
| A route you deleted is still served after `helm upgrade`. | Check whether you ran `helm upgrade` with `--reuse-values`. | Keep a complete `values.yaml` and run `helm upgrade` with `-f values.yaml`. |

## Next steps

[Authenticate to MCP servers behind a tunnel](https://claude.com/docs/connectors/mcp-tunnels/oauth)

See also [Troubleshoot MCP tunnels](https://claude.com/docs/connectors/mcp-tunnels/troubleshooting) and [MCP tunnels](https://claude.com/docs/connectors/mcp-tunnels/overview).
