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
