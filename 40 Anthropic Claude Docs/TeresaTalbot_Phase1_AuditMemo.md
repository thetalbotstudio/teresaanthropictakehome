## Executive Summary

Claude Docs has a content-model problem. Skills, Plugins, and Connectors appear parallel, though users experience them as related parts of one system:
    - Connectors provide external data or tools.
    - Skills provide repeatable instructions and behavior.
    - Plugins package shareable jobs from those building blocks, often with commands or sub-agents.

I'm proposing that we create the hub around user tasks: understand, choose, build, install, configure, secure, troubleshoot, and maintain. To do this, we need to separate products from general concepts. Product documentation focuses on use cases, deployment, administration, and permissions. Where as general concepts are shared definitions, terminology, lifecycle guidance, security expectations, and cross-product behavior. In the end, I want users to know when they are in Claude Docs, where they are within Claude Docs, and how to navigate to content that will solve their issues quickly.

Measuring project success requires a baseline of where we are now and then agreeing on metrics, targets, and periodic check ins. For example, find where Claude docs lands with case deflection, establish how we measure it, then agree how much we want to improve over a set period of time.

## What is wrong, in priority order

### P0: Customers cannot tell what each object does

The index and overview pages introduce Connectors, Skills, and Plugins as adjacent features, but they do not explain their boundaries, relationships, or ownership. I suggest one shared hub with a comparison table for purpose, installation, execution context, and maintenance. A short decision guide near the top is also helpful. For example, choose a Connector for external access.

### P1: Product branches repeat the same explanations

Pages for Connectors, Skills, and Plugins reappear in product areas such as Claude for M365, Claude Science, Claude Tag, Government, and Desktop. Repeating definitions and lifecycle guidance gives users competing explanations and creates unnecessary maintenance. We can solve these issues by moving shared explanations into dedicated concept pages while keeping product pages focused on their actual procedures and limits, with clear links back to the shared model. This is an area of expertise for me. Signal-sourcing and keeping repetitive information to a minimum not only aids user comprehension but reduces localization costs and inaccuracy immensely. 

### P2: Lifecycle and ownership information is scattered

Verification, directory submission, updates, organization provisioning, local storage, compatibility, and deprecation appear across different pages. Users and machines lack a reliable place to find the responsible team, current status, review date, and next action. I suggest requiring shared concept pages to expose machine-readable fields such as `content_type`, `object_type`, `owner_team`, `supported_surfaces`, `status`, `last_reviewed`, `primary_url`, and `next_action`. We can then use those fields to render a visible “At a glance” panel.

### P3: Terminology and cross-links force avoidable decisions

Connector, MCP server, MCP app, Desktop Extension, and Plugin describe related but different concepts. Links that send users to build documentation or another site often appear before the terms are defined. It might seem old-school but following standard style guide rules stops the documentation from creating more user questions. I recommend creating publishing workflows that block pages from publishing if they don't follow agreed style taxonomy guidelines.

## Delete, merge, and redirect policy

I've run many large migrations and redirects are essential. Never remove an indexed URL without a permanent redirect. My general policies when migrating docs are:
	-Merge overlapping content when the reader job is the same.
	-Keep separate pages when the job, search intent, or permission model differs.

Here are a few examples of what I'd delete, merge, and always redirect:

| Current pattern                                     | Action                                                                                    | Reader outcome                                                                 |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Connector overview and shared capability definition | Move the shared model to `/docs/capabilities/connectors`; redirect the old definition URL | The reader reaches one explanation, with an anchor for the original topic.     |
| “What should I build?” under Connector building     | Promote to `/docs/capabilities/choose`; redirect the old URL                              | The reader lands on a Connector vs Skill vs Plugin decision guide.             |
| Directory vs custom connector explanations          | Merge under `/docs/capabilities/connectors/distribution`; redirect all duplicates         | The reader sees one distribution model with the relevant choices.              |
| Directory and verification pages                    | Keep as separate governance task pages                                                    | Browsing and verification remain distinct jobs.                                |
| Repeated custom connector pages                     | Keep only where UI, permissions, or deployment differ; redirect the rest                  | Readers no longer encounter competing setup recipes.                           |

Preserve query parameters, add  metadata to destinations, and always test redirects. Never send migrated readers to a generic 404 or the docs home. That can loose us customers quickly.

## Proposed information architecture

Here's a possible architecture to migrate into:

```text
/docs/
  capabilities/
    overview
    choose
    glossary
    connectors/  overview, install, build, distribution, security, troubleshoot, maintain
    skills/      overview, create, install, provision, test, security, troubleshoot, maintain
    plugins/     overview, create, install, compose, publish, security, troubleshoot, maintain
  products/
    cowork/ | claude-for-m365/ | claude-tag/ | claude-science/ | government/ | desktop/
```

I my experience, migration should happen in four passes: inventory and classify URLs; assign  owners and redirects; replace product copies with concise context and links; enforce metadata, terminology, and link checks. Start with the three overview pages, the decision guide, and the highest-traffic duplicates. Avoid complete rewrites.


## Measuring Success

Measuring project success requires a baseline of where we are now. How well do Claude Docs support user task completion and case deflection? How easy is it to find needed information? Is terminology consistent throughout? What is the lifecycle maintenance effort? Do users trust Claude Docs? Once these metrics are agreed on, we can target an agreed percentage increase (10%) each month or quarter.Measure outcomes, not page count:

1. **Task success:** completion of “connect a service,” “create a skill,” and “install a plugin,” paired with a one-question success survey.
2. **Findability:** search-to-destination success, overview-page exits, median clicks to the first task page, and loops among the three object areas.
3. **Consistency:** share of scoped pages with valid metadata, one canonical next action, current owner, review date, and no broken links.
4. **Maintenance:** stale-page rate, time from product change to docs update, redirect usage, and conflicting definitions found by automated checks.
5. **Trust:** support contacts tagged as Connector, Skill, or Plugin confusion, plus sampled answer accuracy.

I have used analytics to gage page views, internal searches, task-link clicks, redirects, feedback, and versioned metadata. I find a dashboard tracking these metrics helps content creators publish useful information.