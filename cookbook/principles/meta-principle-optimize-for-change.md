---
id: aadd048b-da52-415d-949f-45160b970381
title: "Meta-Principle: Optimize for Change"
domain: agenticdevelopercookbook://principles/meta-principle-optimize-for-change
type: principle
version: 1.1.2
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Every principle is a strategy for making future change cheaper and safer. When evaluating any technical decision, ask whether it makes future change easier or harder."
platforms: []
tags:
  - meta-principle-optimize-for-change
depends-on: []
related: []
references:
  - https://teamtopologies.com/
  - https://teamtopologies.com/news-blogs-newsletters/when-teams-grow-too-large-solving-cognitive-load-issues
  - https://kentbeck.com/summaries
  - https://martinfowler.com/bliki/TeamTopologies.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
---

# Meta-Principle: Optimize for Change

Every principle above is a strategy for making future change cheaper and safer. When evaluating any technical decision, the primary question is: "Does this make future change easier or harder?"

- Before committing to an architecture, ask: "What would it cost to reverse this in six months?"
- Prefer decisions that keep options open over decisions that lock in a technology or pattern
- When two approaches are otherwise equal, choose the one that is easier to change later
- Treat **cognitive load** as the metric the structural principles serve: simplicity, locality of behavior, and boundaries all exist to reduce the cognitive load of understanding and changing the system, so a design — or an agent workflow — **SHOULD** be tested by whether it lowers that load. Caveat: AI and multi-agent tooling can *shift* load onto the human orchestrator rather than remove it, so use cognitive load as a lens (proxies: fan-out, file count, time-to-onboard), not a thresholded metric.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.2 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.1.1 | 2026-06-10 | Mike Fullerton | Cite recovered Tier-1 research sources (adversarially-audited) |
| 1.1.0 | 2026-06-09 | Mike Fullerton | Name cognitive load as the meta-metric |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
