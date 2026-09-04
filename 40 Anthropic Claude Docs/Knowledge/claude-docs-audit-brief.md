I'm working with Claude Docs (claude.com/docs) building AI-assisted review and maintenance.
Claude Docs is the documentation for Claude's apps: Connectors, Cowork, Claude for M365, Plugins, Claude Tag, and Skills. It's a constantly shifting surface that is written by many hands across many product teams.
Two separate sites are not part of this exercise:
platform.claude.com/docs, which covers the developer platform and API, and
code.claude.com/docs, which covers Claude Code and the Agent SDK.

I own the unification and standardization layer across all of Claude Docs, not writing every page, but setting the architecture and the standards, building the systems that keep quality high and enable more teams to contribute, while pruning and curating what's already there.

claude.com/docs/llms.txt gives me the full page index in a single file.

Phase 1: Audit
Audit it Skills, Plugins, and Connectors, as they're used by more than one surface and documented very unevenly.&#x20;
Create a short memo covering:
-What's actually wrong and what what to improve. No issue is too small or too large, prioritize what's most important to address first.
-What should be deleted or merged, and what happens to readers who land on those URLs afterward.
-A proposed information architecture for Skills, Plugins, and Connectors, and what it would take to get there from here.
-What to measure to know if the improvements work, and how to instrument it.

Be opinionated! We appreciate people who have opinions about the right way to do something, even if (especially if!) it's different from how we've done it in the past.

Phase 2: Standards
An estate written by many hands needs conventions those hands will actually follow! Write the piece of a style guide and one content-type template that would have prevented the problems found in Phase 1. Then apply it: take one existing page from Skills, Plugins, and Connectors and rewrite it according to spec. Record the before and the after, plus a note on what changed and why.

Be specific about conformance. "Pages should be scannable" isn't a standard. Write rules a reviewer, or a machine, could apply the same way twice.

Phase 3: System
Build a working prototype of an automated check that runs against the real docs and flags one class of problem found in Phase 1. Point it at the live site or a scrape of it (you can draw from claude.com/docs/llms.txt). It can be as simple as a script that fetches pages and asks Claude to evaluate them against the standard from Phase 2. What matters is that it runs, that it ran on the real site, and that it show us what it found.
Send it as a GitHub link, along with:
-The output on the real corpus, including a few cases where the checker got it wrong.
-How to evaluate the checker itself. The tolerance for false positives, and why that number? How to know if it degraded? What keeps this from becoming another stale artifact in six months?

Phase 4: Adoption
How to get adoption from several product teams that don't report to you. What to do about the team
that ignores the system? Describe the approach in only a few paragraphs.

Submission
-Phase 1: memo, as markdown or PDF or part of the GitHub submission
-Phase 2: style guide excerpt, content-type template, and the before/after page, in markdown separately or as part of the GitHub submission
-Phase 3: GitHub link, plus the output from your run
-Phase 4: a few paragraphs maximum