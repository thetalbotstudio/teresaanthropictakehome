---
content_type: task
object_type: connector
owner_team: Docs Platform
supported_surfaces: [claude.ai]
status: current
last_reviewed: 2026-09-03
canonical_url: https://claude.com/docs/connectors/custom/remote-mcp
next_action: https://claude.com/docs/connectors/overview
---

# Add a third-party remote MCP connector

Add a remote MCP server as a custom connector, configure its authentication, and connect it so Claude can use the server’s tools in a conversation.

> **At a glance**
> - Audience: Claude users adding a third-party remote MCP server
> - Prerequisites: A remote MCP server URL and the Claude account, plan, or organization access required to add a custom connector
> - Outcome: A configured custom connector that you can connect and enable in chat

## Before you begin

- Confirm that you have the HTTPS URL for the remote MCP server.
- Decide whether the server uses OAuth, a fixed credential, or both.
- Review the server’s organization and permission requirements before connecting it.
- If you are on a Team or Enterprise plan, confirm whether you are an owner or a member because the setup steps differ.

## Add the custom connector

1. Open [Claude](https://claude.ai/).
2. Open **Connectors** from the relevant settings area.
3. Select **Add custom connector** or select **Add**, then **Custom**.
4. Choose **Web** when Claude asks for the connector type.
5. Enter the remote MCP server URL.
6. Configure OAuth credentials when the server requires them.
7. Configure request headers when the server uses a fixed credential and the option is available.
8. Select **Add**.
9. Authenticate when Claude prompts you to connect.
10. Enable the connector from the chat **+** menu.

### Product-specific

- **Team and Enterprise owners:** Open **Organization settings > Connectors** or **Admin settings > Connectors**, then add the custom connector. Members find the connector under **Customize > Connectors** and select **Connect** to authenticate.
- **Free, Pro, and Max users:** Open **Customize > Connectors**, select **Add custom connector**, enter the URL, configure OAuth credentials when needed, and select **Add**.
- The two-step dialog is rolling out gradually. If the dialog shows Name, URL, and Advanced settings on one screen, use the same fields in that dialog.
- Request header authentication is in beta and available only to a limited set of organizations. If **Request headers** is absent, your organization does not have access to it.

## Configure the connector

1. Enter a display name in **Name**.
2. Confirm the **Remote MCP server URL**.
3. Choose an **Authentication** option.
4. Choose an **OAuth client** option when OAuth is enabled.
5. Enter request headers when the server requires fixed credentials.
6. Set **Advanced > Transport** only when the server documentation requires a different transport.
7. Select **Add** to save the connector.

Use **Always required** when every user must authenticate through the server’s OAuth flow. Use **Required when the server asks** when the server should request authentication as needed. Use **None** when the server requires no sign-in or uses an API key in **Request headers**.

For OAuth client setup, use Anthropic’s hosted client metadata when the server supports it, register a client automatically, or enter a client ID that you registered with the server. Leave the client secret blank unless the authorization server requires one. For more detail, see [Authentication for connectors](https://claude.com/docs/connectors/building/authentication).

When entering a fixed credential, enter the complete value. For example, enter `Bearer your-token`, including the scheme and space, for an Authorization header. Claude does not add a scheme or prefix.

## Security and permissions

Custom connectors can connect Claude to unverified services. A remote MCP server can let Claude read, create, modify, or delete data in connected applications, or take actions on your behalf. Review the server organization, requested permission scopes, and tool approval requests before connecting.

Use OAuth when each person needs to authenticate with their own account. Use request headers for a shared API key, bearer token, or service credential only when that shared access is appropriate. Claude stores request-header values securely and sends them on every request. Do not configure an `Authorization` request header on an OAuth connection because OAuth owns that header.

Monitor tool behavior, select **Always allow** only for trusted servers, disable unused connectors from the chat **+** menu, and block individual tools under **Customize > Connectors** when you do not need them. To change authentication settings after adding a connector, remove it and add it again. Members must reconnect afterward.

## Troubleshooting

| Symptom | Check | Fix |
|---|---|---|
| The custom connector option is unavailable. | Check your plan, organization policy, and current Claude surface. | Use the connector settings available to your plan or ask an organization owner to add the connector. |
| **Request headers** is not shown. | Check whether your organization has access to the beta feature. | Use OAuth, or contact your organization administrator about request-header availability. |
| Claude rejects the connector URL. | Confirm that the URL is the HTTPS address where the remote MCP server accepts MCP requests. | Correct the URL using the server’s documentation, then add the connector again. |
| Authentication fails. | Check the selected authentication method and the permission scopes requested by the server. | Choose the method the server requires and authenticate again. |
| A bearer-token connection is rejected. | Check whether the Authorization value includes `Bearer ` followed by a space. | Enter the full value, such as `Bearer your-token`, in the header field. |
| A header cannot be saved. | Check whether the custom header name has been approved. | Choose a listed header name or request approval from [Claude support](https://support.claude.com/en/articles/9015913-how-to-get-support). |

## Next steps

[Review how connectors work](https://claude.com/docs/connectors/overview)
