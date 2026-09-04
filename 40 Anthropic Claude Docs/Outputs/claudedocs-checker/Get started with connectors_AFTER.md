---
content_type: task
object_type: connector
owner_team: Docs Platform
supported_surfaces: [claude.ai]
status: current
last_reviewed: 2026-09-03
canonical_url: https://claude.com/docs/connectors/getting-started
next_action: https://claude.com/docs/connectors/overview
---

# Connect Claude to a service

Connect one of your services to Claude, authorize the requested access, and use that service's content in a conversation.

> **At a glance**
> - Audience: Claude users connecting a work service
> - Prerequisites: A Claude account and an account on the service you want to connect
> - Outcome: One authenticated connector is available in a Claude conversation

## Before you begin

- Confirm that your Claude plan and organization allow the connector you want to use.
- Sign in to the service you want to connect.
- Decide which data Claude needs for the task. Connect only services with relevant data.

## Connect a service

1. Open [claude.ai](https://claude.ai/).
2. Open **Customize** in the sidebar.
3. Open **Connectors**.
4. Choose the service you want to connect.
5. Select **Connect** next to the service.
6. Sign in to the service when prompted.
7. Review and grant the requested permissions.
8. Return to Claude and start a new conversation.

## Use connected data

1. Open the add-content control in the conversation.
2. Choose the connected service.
3. Select the content to include.
4. Ask a question about the selected content.

### Product-specific

In a project, open the project, select **Add Content**, choose the connector, and add documents to the project knowledge. The available controls and connector list can vary by plan, organization policy, and product surface.

## Security and permissions

Connecting a service authorizes Claude to access the data and actions listed in the service's permission request. Review that request before granting access. Connect only the data sources needed for your task, and disconnect a service from connector settings when you no longer want Claude to access it.

## Troubleshooting

| Symptom | Check | Fix |
|---|---|---|
| The connector will not authenticate. | Confirm that you can sign in to the source service and that your plan or organization permits the connector. | Sign in again, then disconnect and reconnect the service. |
| Expected data does not appear. | Confirm that your account can access the data in the source service. | Wait for synchronization to finish, then retry the search or selection. |
| The connection has expired. | Check the connector status in **Customize** > **Connectors**. | Reauthenticate the service and grant the requested permissions again. |

## Next steps

[Review how connectors work](https://claude.com/docs/connectors/overview)
