---
id: b224ef56-65f5-45fd-8842-767b20df6736
title: "Steel thread first"
domain: agenticdevelopercookbook://principles/steel-thread-first
type: principle
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Build the thinnest end-to-end slice through every boundary before breadth — the disciplined answer to scaffolding vs YAGNI."
platforms: []
tags:
  - steel-thread
  - walking-skeleton
  - architecture
depends-on: []
related:
  - agenticdevelopercookbook://principles/yagni
  - agenticdevelopercookbook://principles/small-reversible-decisions
  - agenticdevelopercookbook://principles/manage-complexity-through-boundaries
  - agenticdevelopercookbook://principles/make-it-work-make-it-right-make-it-fast
references:
  - https://www.rubick.com/steel-threads/
  - https://bryceyork.com/steel-threads/
  - https://codeclimate.com/blog/kickstart-your-next-project-with-a-walking-skeleton
  - https://news.ycombinator.com/item?id=35090989
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
---

# Steel thread first

Before building breadth, build the thinnest end-to-end slice that exercises every integration boundary and the deployment path — a "steel thread" or walking skeleton. This is the disciplined answer to "when is scaffolding for a larger design justified?": prove the whole shape connects once, end to end, then fill it in. It bounds the cost of a wrong architecture without inviting speculative generality.

- Thin but complete: one real path through every layer and boundary (UI → API → store → deploy), not a finished feature — connect the architecture before investing in any single part.
- This is the balance with YAGNI: build the shell only for the path you are committed to and that is expensive to wire up later. Do not pre-build features, options, or abstractions you don't yet need — that remains YAGNI.
- Front-load the risky integrations: the thread should pierce the boundaries most likely to surprise you (auth, third-party APIs, the deploy pipeline), so failures surface while they are cheap.
- For agents: validate the end-to-end shape before spending effort on breadth, so a wrong architecture is caught early instead of after generating volume against it.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Cite recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
