# Before/after record — Third party connectors with remote MCP

Workflow: `workflow-claude-docs-task-page-builder` v1.2 · Run: 2026-09-03 17:43 PDT · Operator: Teresa Talbot (Cowork session)

Note: a parallel session produced `Knowledge/claudedocs/Third party connectors with remote MCP_AFTER.md` at 17:49 PDT during this run. Per Teresa's instruction, this run's files carry the `_BEFORECLAUDE` / `_AFTERCLAUDE` suffixes and do not touch that file.

## Target manifest

| Field | Value |
|---|---|
| Request | URL: https://claude.com/docs/connectors/custom/remote-mcp |
| Step 0 fetch | `https://claude.com/docs/connectors/custom/remote-mcp.md`, 2026-09-03 17:46 PDT. Shell `curl` blocked by the egress proxy (403) in both the container and the local VM; fetched via the built-in browser (`<pre>` text of the `.md` route, 10,136 chars, `text/markdown`). |
| Raw snapshot | `Outputs/claudedocs-checker/snapshots/connectors-custom-remote-mcp.md` (unmodified response) |
| Target path | `Knowledge/claudedocs/Third party connectors with remote MCP.md` (clipping built from the snapshot; untouched after creation) |
| Before snapshot | `Knowledge/claudedocs/Third party connectors with remote MCP_BEFORECLAUDE.md` (byte-identical copy of the target, verified with `cmp`) |
| After path | `Knowledge/claudedocs/Third party connectors with remote MCP_AFTERCLAUDE.md` |
| Canonical URL | https://claude.com/docs/connectors/custom/remote-mcp |
| Object type | connector |
| Observable job | A reader registers a remote MCP server as a custom connector, sets its sign-in method, and turns its tools on in a chat |
| Scope | Full page |
| Operation | Create (`_AFTERCLAUDE` file); the canonical target was not replaced |

## Retained context manifest

| Source | Status | Use |
|---|---|---|
| `Outputs/claudedocs-checker/snapshots/connectors-custom-remote-mcp.md` (raw MDX, fetched this run) | Current; primary source | All product claims, UI labels, links |
| `Knowledge/claudedocs/Third party connectors with remote MCP.md` (clipping derived from the snapshot) | Current | Target page |
| `https://claude.com/docs/llms.txt` (read this run via the built-in browser) | Current | Route validation for every internal link on the after page |
| `Outputs/claudedocs-checker/out/connectors-custom-remote-mcp.findings.md` (checker run on the target, this run) | Current | Prior QA: 8 mandatory failures, 1 advisory, 3 needs-review |
| `TeresaTalbot_Phase2_01StyleGuideExcerpt.md`, `TeresaTalbot_Phase2_02ContentTypeTemplate.md`, `Templates/doc-task-topic.md` | Current | Page contract |
| `Knowledge/claude-docs-audit-brief.md`, `Knowledge/knowledge.md` | Current | Scope |
| `Knowledge/claudedocs/Set up an MCP tunnel_AFTER.md` | Current | Precedent for front-matter conventions (`owner_team: Docs Platform`, `supported_surfaces: [claude.ai]`, absolute links) |

Exclusions: no product behavior beyond the snapshot. The parallel `_AFTER.md` was not read as a source.

Known uncertainties: `owner_team` is not stated by the source and inherits the workspace convention. The source names two admin paths, **Organization settings > Connectors** (add) and **Admin settings > Connectors** (manage); both kept as stated, not reconciled. The source does not say whether Free/Pro/Max users see a **Connect** control after adding; the after page's connect step is written from the members flow and the Authentication descriptions ("each user signs in through the server's OAuth flow before using it").

## Source map (after → source)

| After section | Source |
|---|---|
| Front matter | Template; `canonical_url` from the request; `next_action` = `connectors/building/troubleshooting` (route validated in llms.txt; not linked from the source page — see change 10) |
| Opening, At a glance | Rewritten from "Adding custom connectors" intro, Authentication descriptions, "Enabling connectors in chat" |
| Before you begin | "Finding connectors"; Security Notice warning; "Remote MCP server URL" field; Authentication and OAuth client field descriptions; "Owners must / Members then" |
| Add the connector | "For Team and Enterprise plans" steps 1–5, "For Free, Pro, and Max plans" steps 1–5, and the field-by-field section (Name, URL, Authentication, OAuth client, Request headers, Advanced > Transport) |
| Add a request header | "Authenticating with request headers" intro paragraphs 1–3; "Adding a request header" steps 1–5; "Enter the full header value" |
| Connect and turn on the connector | "Members then" steps 1–3; "Enabling connectors in chat" |
| Product-specific | Owner/member split; Free/Pro/Max path; "choose Web" sentence; two-step dialog Note; request-headers beta Note |
| Security and permissions | Security Notice; "Best practices"; "Tool actions" and "Usage guidelines"; request-header storage sentence; `Authorization` exception; "Managing connectors" (edit/remove, settings locked after add, members reconnect); "Reporting issues" |
| Troubleshooting | Two-step dialog Note; request-headers beta Note; custom header approval sentence; "Enter the full header value"; Required-header sentence; "Managing connectors" locked-settings paragraph; members flow; tool Blocked permission |
| Next steps | `building/troubleshooting` (added, validated), `building/authentication` (source), `connectors/directory` (source) |

## Material changes and rationale

1. **Typed front matter added** in place of clipping metadata — T3.
2. **H1 renamed** from "Third party connectors with remote MCP" (noun phrase, T1b needs-review) to "Add a custom connector for a remote MCP server" (46 chars, imperative, one object). The source H1 named the object, not the job.
3. **Opening rewritten to the observable result** (33 words) — T2b. The source opening described what custom connectors enable.
4. **Concept content removed from the page**: "What are third party connectors?" and the "You can: connect / build" list. Reason: J1 and reader-value — the Connectors overview and Building custom connectors pages own it. "Finding connectors" survives as the first Before you begin bullet because it is a decision the reader makes before adding a custom connector.
5. **Two plan-specific procedures merged into one shared procedure** with the differing entry path and button labels moved under Product-specific — T7. The source repeated the same five steps for two plan groups and put the field reference in a separate section; the after page walks through the dialog once, with the field descriptions attached to the step where the reader needs them.
6. **"Optionally configure OAuth…" steps replaced** by explicit Choose-an-option steps (T6a needs-review on "Optionally", twice in the source).
7. **"Adding a request header" step 1 and step 5 repaired** ("In the Add custom connector dialog, open…" → "Open … in the Add custom connector dialog"; "Repeat … then click Add" split so the final **Add** is step 10 of the main procedure) — T6a/T6b mandatory failures in the source.
8. **"Enter the full header value" table converted to prose.** The checker's T9 selected this table (the first table in the document) instead of the Troubleshooting table and reported a false failure; see QA history. The content is unchanged.
9. **"Managing connectors", "Security and privacy", "Tool actions", and "Reporting issues" consolidated into Security and permissions** — T8. Remove/limit/report guidance sits with the access it governs.
10. **Troubleshooting table added** (8 rows) from failure conditions already stated in the source. No new failure modes invented. Rows for changing a bearer-token value or a required header carry the source's "remove and add again" rule because authentication settings are locked after adding.
11. **Next steps added** — T10. `next_action` is the sibling page Troubleshooting connectors (`/docs/connectors/building/troubleshooting`, "Diagnose and resolve common connection failures for custom and directory MCP connectors" per llms.txt). This is the one link not present on the source page; it was added deliberately because it is the reader's most likely next need after adding a custom connector. Flag for review if you prefer a source-only link set — the fallback is `connectors/building/authentication`.
12. **Related-topics cards dropped** (Building Connectors, MCP Overview, Desktop Extensions, MCP in Claude Code): they introduce other objects and the Next steps rule allows at most three links. The Building Connectors and MCP Overview pages remain reachable from the Connectors overview.

## AI workflow actions

Step 0 download (browser fallback), clipping and BEFORECLAUDE creation, checker run on the target, draft, checker run on the draft (T9 fail → prose repair → PASS with in-session judgment results), record and log. All under `40 Anthropic Claude Docs`; no external publish.

## QA history

| Gate | Result | Notes |
|---|---|---|
| target-downloaded | pass | Browser fallback; both saved paths recorded above |
| target-resolved | pass | One page, full scope |
| source-boundary-resolved / source-eligibility-passed | pass | Single current snapshot; one added link (change 11) validated against llms.txt and flagged |
| task-contract-selected | pass | One observable job; concept and management content relocated |
| task-contract-qa-passed | pass | Checker v0.1.0 run 2: PASS, 14/14 checks (`Outputs/claudedocs-checker/out-afterclaude/`) |
| unsupported-claims-qa-passed | pass | Two soft inferences flagged under Known uncertainties (members cannot add; Connect after adding on Free/Pro/Max) |
| links-qa-passed | pass | All 6 internal routes present in llms.txt; `canonical_url` ≠ `next_action`; anchors `#product-specific`, `#add-a-request-header`, `#connect-and-turn-on-the-connector` match headings |
| technical-leakage-qa-passed | pass | Transport/SSE detail kept because it is a field the reader may need to set |
| reader-value-qa-passed | pass | Concept section removed; every remaining section acts, decides, verifies, or recovers |
| voice-qa-passed | pass | Imperative steps, no marketing register; source terminology kept (custom connector, remote MCP server, request header) |
| before-after-qa-passed | pass | Complete before and after snapshots below |
| output-paths-resolved | pass | All paths under the workspace |
| approval-before-write | not exercised | Canonical target not replaced |

Checker run 1 on the draft: 1 mandatory failure — T9 reported `columns: ['You enter', 'Claude sends']` because the check reads the first table in the document rather than the table under the Troubleshooting H2. False positive; recorded as a checker defect (fix: scope T9 to the Troubleshooting section). Draft revised (change 8) rather than leaving the FP standing, so the deliverable passes as-is.

## Unresolved issues

- `owner_team: Docs Platform` is a workspace convention, not a source fact.
- Source names both **Organization settings > Connectors** and **Admin settings > Connectors** for Team/Enterprise owners; kept as stated.
- `next_action` links a page the source does not link (change 11).
- Checker defect T9 (first-table selection) added to the known-defect list.

## Approval state

Draft. Awaiting Teresa's review of `_AFTERCLAUDE.md`. No authoritative page was changed.

## Complete before snapshot

Source: `Knowledge/claudedocs/Third party connectors with remote MCP_BEFORECLAUDE.md`

````markdown
---
title: "Third party connectors with remote MCP"
source: "https://claude.com/docs/connectors/custom/remote-mcp"
author:
published:
created: 2026-09-03
description: "Connect Claude to your tools using the Model Context Protocol"
tags:
  - "clippings"
---
# Third party connectors with remote MCP

> Connect Claude to your tools using the Model Context Protocol

Custom connectors enable you to link Claude directly to your essential tools and data sources using the Model Context Protocol (MCP).

## What are third party connectors?

Custom connectors allow Claude to operate within your preferred software and leverage comprehensive context from your external tools.

You can:

* Connect Claude to existing remote MCP servers
* Build your own remote MCP servers for any tool

### Finding connectors

Browse the [Connectors Directory](/docs/connectors/directory) to discover third-party MCP servers that are ready to use across all Claude products. Some are verified by Anthropic and others are community connectors; see [connector verification](/docs/connectors/verification).

## Adding custom connectors

You can manually add any third-party connector to Claude as long as you have the URL of that remote MCP server.

<Warning>
  **Security Notice**: Custom connectors allow connections to unverified services. Claude can access and perform actions within these services, so review security considerations carefully.
</Warning>

### For Team and Enterprise plans

**Owners must:**

1. Navigate to **Organization settings > Connectors**
2. Select **Add**, then **Custom**. If Claude asks for the connector type, choose **Web**.
3. Enter the remote MCP server URL
4. Optionally configure OAuth Client ID/Secret in Advanced settings
5. Click "Add"

If your Add custom connector dialog has two steps, see [The Add custom connector dialog, field by field](#the-add-custom-connector-dialog-field-by-field).

**Members then:**

1. Go to **Customize > Connectors**
2. Find the connector with "Custom" label
3. Click "Connect" to authenticate

### For Free, Pro, and Max plans

1. Navigate to **Customize > Connectors**
2. Click "Add custom connector"
3. Enter the remote MCP server URL
4. Optionally configure OAuth credentials
5. Click "Add"

If your Add custom connector dialog has two steps, see [The Add custom connector dialog, field by field](#the-add-custom-connector-dialog-field-by-field).

### Enabling connectors in chat

Use the "+" button in your chat interface to access "Connectors," where you can enable/disable connectors per conversation.

## The Add custom connector dialog, field by field

<Note>
  The two-step dialog described here is rolling out gradually. If your dialog shows a name, URL, and Advanced settings on one screen, your organization has the earlier version; the steps above still apply.
</Note>

**Name**: the display name shown in the connectors list.

**Remote MCP server URL**: the HTTPS address where the server accepts MCP requests, for example `https://mcp.example.com/mcp`. After you continue, Claude checks the URL and pre-fills the authentication settings it detects, marked "Detected."

**Authentication**: how people connect to the server.

* **Always required**: each user signs in through the server's OAuth flow before using it.
* **Required when the server asks**: Claude connects without credentials and prompts users to sign in when the server asks.
* **None**: no sign-in. Anyone with access to the server URL can use the connector. If the server uses an API key, choose None and add the key under **Request headers**; Claude stores it as the connector's credential.

**OAuth client** (shown unless you chose None): how Claude identifies itself to the server's authorization server.

* **Use Anthropic's hosted client metadata** (recommended): the server reads Claude's client details from a URL Anthropic hosts (Client ID Metadata Document). Nothing to set up; the server must support it.
* **No client ID — register one automatically**: Claude registers OAuth clients with the server as users connect (Dynamic Client Registration). Works with most servers, but adds client registrations over time.
* **Use your own OAuth client**: enter a client ID you registered with the server. Leave the secret blank unless your authorization server requires one. See [Authentication for connectors](/docs/connectors/building/authentication).

**Request headers**: fixed credentials such as API keys, sent on every request. See [Authenticating with request headers](#authenticating-with-request-headers).

**Advanced > Transport**: set from the URL automatically; a URL ending in `/sse` selects the older SSE transport. Change it only if the server's documentation says to.

## Authenticating with request headers

<Note>
  Request header authentication is in beta and available to a limited set of organizations. If you don't see the **Request headers** section in the Add custom connector dialog, your organization doesn't have access yet.
</Note>

If your MCP server authenticates with an API key, bearer token, or other fixed credential instead of OAuth, you can configure it in the **Request headers** section of the Add custom connector dialog. Claude stores each header value securely, does not show it again after you save, and sends it on every request to your server.

Request headers suit services where everyone in your organization shares one credential, such as an internal tool or a service account. If each person needs to sign in with their own account, use OAuth instead.

You can also use request headers in addition to OAuth, including OAuth with your own pre-registered client credentials. Headers configured on an OAuth connection are sent on every request alongside the OAuth bearer token. This is useful for verifying where a request came from, passing additional client metadata, or working with tunnels and gateways that need their own routing header. The one exception is `Authorization`: OAuth owns that header, so it cannot be configured as a request header on an OAuth connection.

### Adding a request header

1. In the Add custom connector dialog, open **Request headers**.
2. Select a header name from the list, or choose **Custom header** to enter a different name. The list offers standard authentication and routing header names such as `authorization`, `x-api-key`, and `x-auth-token`, which every connector can use. Anthropic reviews and approves each custom header name before Claude will send it to a third-party server, which prevents connector configuration from being used to send arbitrary header names. If you enter a header name that isn't approved, Claude rejects the save with an error. To request approval for a custom header name, contact [Claude support](https://support.claude.com/en/articles/9015913-how-to-get-support).
3. Enter the header value exactly as your server expects to receive it.
4. Choose whether the header is **Required**. When a required header has no stored value at connection time, the connection fails. When an optional header has no value, Claude simply omits it from the request.
5. Repeat for any additional headers your server needs (you can add up to four), then click **Add**.

### Enter the full header value

Claude sends the value exactly as you enter it. It does not add an authentication scheme or any other prefix.

For an `Authorization` header, include the scheme in the value:

| You enter           | Claude sends                       |
| ------------------- | ---------------------------------- |
| `Bearer your-token` | `Authorization: Bearer your-token` |
| `your-token`        | `Authorization: your-token`        |

Most servers that use bearer tokens reject the second form. If your server's documentation shows `Authorization: Bearer YOUR_TOKEN`, enter `Bearer ` followed by your token, including the space. The same applies to Basic authentication: enter `Basic ` followed by the base64-encoded credentials.

## Managing connectors

To edit a connector's name or URL, or to remove a connector:

1. Go to **Customize > Connectors** (Team and Enterprise owners: **Admin settings > Connectors**)
2. Click "Remove" or select the three-dot menu
3. Follow the prompts

Authentication settings (OAuth credentials and request headers) can't be changed after a connector is added. To change them, remove the connector and add it again with the new details. Members will need to reconnect.

## Security and privacy

### Best practices

* Only connect to servers from trusted organizations
* Carefully review requested permission scopes during authentication
* Be aware of prompt injection risks; Claude has built-in protections
* Monitor for unexpected changes in tool behavior

### Tool actions

Remote MCP servers enable Claude to invoke tools that can:

* Read data from applications
* Create, modify, or delete data
* Take actions on your behalf

**Usage guidelines:**

* Monitor Claude's actions for unintended effects
* Review tool approval requests carefully
* Only click "Always allow" for trusted servers
* Turn off connectors you aren't using with the toggles in the chat "+" menu's **Connectors** item
* Block individual tools you don't need under **Customize > Connectors** by selecting the connector and setting the tool's permission to **Blocked**

## Reporting issues

Report malicious MCP servers to [Anthropic's Bug Bounty Program](https://www.anthropic.com/responsible-disclosure-policy).

## Related topics

<Columns cols={2}>
  <Card title="Building Connectors" icon="hammer" href="/docs/connectors/building/">
    Learn to build your own MCP servers.
  </Card>

  <Card title="Connectors Directory" icon="book" href="/docs/connectors/directory">
    Browse pre-built connectors.
  </Card>

  <Card title="MCP Overview" icon="plug" href="/docs/connectors/building/mcp">
    Understand the Model Context Protocol.
  </Card>

  <Card title="Desktop Extensions" icon="desktop" href="/docs/connectors/custom/desktop-extensions">
    Deploy enterprise-grade MCP servers.
  </Card>

  <Card title="MCP in Claude Code" icon="terminal" href="https://code.claude.com/docs/en/mcp-quickstart">
    Add the same server to Claude Code from the command line.
  </Card>
</Columns>

````

## After snapshot

Source: `Knowledge/claudedocs/Third party connectors with remote MCP_AFTERCLAUDE.md`

````markdown
---
content_type: task
object_type: connector
owner_team: Docs Platform
supported_surfaces: [claude.ai]
status: current
last_reviewed: 2026-09-03
canonical_url: https://claude.com/docs/connectors/custom/remote-mcp
next_action: https://claude.com/docs/connectors/building/troubleshooting
---

# Add a custom connector for a remote MCP server

After this task, a remote MCP server of your choosing is registered in Claude as a custom connector, its sign-in method is set, and its tools can be turned on in a conversation.

> **At a glance**
> - Audience: Anyone on a Free, Pro, or Max plan, or an Owner on a Team or Enterprise plan, who has the URL of a remote MCP server
> - Prerequisites: The server's HTTPS MCP URL and, if the server needs one, its OAuth client details or fixed credential
> - Outcome: The connector appears in your connectors list and can be turned on from the **+** menu in a chat

## Before you begin

- Check the [Connectors Directory](https://claude.com/docs/connectors/directory) before you add a custom connector. Directory connectors are ready to use, and some are verified by Anthropic; see [connector verification](https://claude.com/docs/connectors/verification).
- Confirm that the server comes from an organization you trust. A custom connector is an unverified service that Claude can read from and act in.
- Get the remote MCP server URL: the HTTPS address where the server accepts MCP requests, for example `https://mcp.example.com/mcp`.
- Find out how the server authenticates: OAuth, where each person signs in; a fixed credential such as an API key, which you add as a request header; or no sign-in.
- If you will use your own OAuth client, have the client ID you registered with the server. You need the client secret only if the server's authorization server requires one.
- On a Team or Enterprise plan, confirm that you have the Owner role. Members cannot add custom connectors; they connect to a connector after an Owner adds it.

## Add the connector

1. Open the Connectors settings for your plan. See [Product-specific](#product-specific) for the path.
2. Select **Add custom connector**. On a Team or Enterprise plan, select **Add**, then **Custom**.
3. Enter a **Name**. This is the display name shown in the connectors list.
4. Enter the **Remote MCP server URL**.
5. Go to the authentication settings. In the two-step dialog, Claude checks the URL after you continue and pre-fills the settings it detects, marked "Detected."
6. Choose an **Authentication** option:
   - **Always required**: each user signs in through the server's OAuth flow before using it.
   - **Required when the server asks**: Claude connects without credentials and prompts users to sign in when the server asks.
   - **None**: no sign-in. Anyone with access to the server URL can use the connector. If the server uses an API key, choose None and add the key as a request header.
7. Choose an **OAuth client** option, shown unless you chose None:
   - **Use Anthropic's hosted client metadata** (recommended): the server reads Claude's client details from a URL that Anthropic hosts. Nothing to set up; the server must support it.
   - **No client ID — register one automatically**: Claude registers an OAuth client with the server as each user connects. Works with most servers, but adds client registrations over time.
   - **Use your own OAuth client**: enter the client ID you registered with the server. Leave the secret blank unless your authorization server requires one. See [Authentication for connectors](https://claude.com/docs/connectors/building/authentication).
8. Add request headers if the server uses a fixed credential, or needs a routing header alongside OAuth. See [Add a request header](#add-a-request-header).
9. Leave **Advanced > Transport** as set from the URL. A URL ending in `/sse` selects the older SSE transport. Change it only if the server's documentation says to.
10. Select **Add**.

### Add a request header

Use request headers for a credential that everyone in your organization shares, such as an internal tool or a service account. If each person needs their own account, use OAuth instead. You can also add headers to an OAuth connection; they are sent alongside the OAuth bearer token.

1. Open **Request headers** in the Add custom connector dialog.
2. Select a header name from the list, or choose **Custom header** to enter a different name. The list offers standard names such as `authorization`, `x-api-key`, and `x-auth-token`.
3. Enter the header value exactly as your server expects to receive it. Claude adds no scheme or prefix.
4. Choose whether the header is **Required**. A required header with no stored value makes the connection fail; an optional one is omitted.
5. Repeat for each additional header the server needs, up to four in total.

For an `Authorization` header, include the scheme in the value. If you enter `Bearer your-token`, Claude sends `Authorization: Bearer your-token`. If you enter only `your-token`, Claude sends `Authorization: your-token`, which most servers that use bearer tokens reject. The same applies to Basic authentication: enter `Basic ` followed by the base64-encoded credentials.

## Connect and turn on the connector

1. Go to **Customize > Connectors**.
2. Find the connector labeled **Custom**.
3. Select **Connect** to authenticate.
4. Open the **+** menu in a chat.
5. Select **Connectors**.
6. Turn on the connector for that conversation.

### Product-specific

- **Team and Enterprise plans.** Owners add the connector under **Organization settings > Connectors** with **Add**, then **Custom**. If Claude asks for the connector type, choose **Web**. Members then complete only [Connect and turn on the connector](#connect-and-turn-on-the-connector).
- **Free, Pro, and Max plans.** Add the connector under **Customize > Connectors** with **Add custom connector**.
- **Dialog version.** The two-step dialog is rolling out gradually. If your dialog shows a name, URL, and Advanced settings on one screen, your organization has the earlier version: configure the OAuth Client ID and Secret under Advanced settings. The steps above still apply.
- **Request headers.** Request header authentication is in beta and available to a limited set of organizations. If the **Request headers** section is absent from the dialog, your organization doesn't have access yet.

## Security and permissions

A custom connector lets Claude call the server's tools, which can read data from applications, create, modify, or delete data, and take actions on your behalf. The server is unverified by Anthropic, so review the permission scopes it requests during authentication, review each tool approval request, and select **Always allow** only for servers you trust. Be aware of prompt injection risks; Claude has built-in protections. Watch for unexpected changes in tool behavior.

Credentials: with OAuth, each person signs in with their own account. A request header value is stored securely, is not shown again after you save, and is sent on every request to the server. On an OAuth connection, OAuth owns the `Authorization` header, so it cannot be configured as a request header.

To limit access, turn off connectors you aren't using with the toggles under **Connectors** in the chat **+** menu, or block individual tools under **Customize > Connectors** by selecting the connector and setting the tool's permission to **Blocked**.

To remove a connector, or to edit its name or URL, go to **Customize > Connectors** (Team and Enterprise owners: **Admin settings > Connectors**), select **Remove** or the three-dot menu, and follow the prompts. Authentication settings, both OAuth credentials and request headers, cannot be changed after a connector is added: remove the connector and add it again with the new details, and members reconnect afterward.

Report malicious MCP servers to [Anthropic's Bug Bounty Program](https://www.anthropic.com/responsible-disclosure-policy).

## Troubleshooting

| Symptom | Check | Fix |
|---|---|---|
| The dialog shows name, URL, and Advanced settings on one screen | Your organization has the earlier dialog version | Enter the OAuth Client ID and Secret under Advanced settings; the same steps apply |
| The **Request headers** section isn't in the dialog | Request header authentication is in beta for a limited set of organizations | Use an OAuth authentication option; your organization doesn't have request headers yet |
| Claude rejects the save with an error about the header name | Whether the custom header name is approved by Anthropic | Choose a listed header name, or contact [Claude support](https://support.claude.com/en/articles/9015913-how-to-get-support) to request approval |
| The server rejects a bearer token | Whether the `Authorization` value starts with `Bearer ` and a space | Remove the connector and add it again with `Bearer ` followed by the token |
| The connection fails when someone connects | Whether a header marked **Required** has no stored value | Remove the connector and add it again with a value for that header, or leave it optional |
| You need to change OAuth credentials or request headers | Authentication settings are locked after a connector is added | Remove the connector and add it again; members must reconnect |
| A member on a Team or Enterprise plan can't find the connector | Whether an Owner has added it under **Organization settings > Connectors** | Ask an Owner to add it; members then look for the **Custom** label under **Customize > Connectors** |
| Claude uses a tool from the server that you don't want it to use | The tool's permission under **Customize > Connectors** | Set the tool's permission to **Blocked**, or turn the connector off in the chat **+** menu |

## Next steps

[Troubleshooting connectors](https://claude.com/docs/connectors/building/troubleshooting) diagnoses connection failures for custom connectors. To understand OAuth options for a server you run, see [Authentication for connectors](https://claude.com/docs/connectors/building/authentication). To find servers that are ready to use, browse the [Connectors Directory](https://claude.com/docs/connectors/directory).

````
