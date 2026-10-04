---
id: 1357be12-5a58-4143-a570-849c114770c5
title: "Separation of concerns"
domain: agenticdevelopercookbook://principles/separation-of-concerns
type: principle
version: 1.1.2
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "A module should have one reason to change; if describing it requires 'and,' consider splitting. This applies at every scale, balanced by locality of behavior."
platforms: []
tags:
  - separation-of-concerns
depends-on: []
related:
  - agenticdevelopercookbook://principles/srp
  - agenticdevelopercookbook://principles/connascence
references:
  - https://htmx.org/essays/locality-of-behaviour/
  - https://shows.acast.com/dead-code/episodes/brutality-of-behaviour-with-carson-gross
  - https://wipdev.netlify.app/posts/separation-of-concerns-locality-of-behavior-and-javascript/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
---

# Separation of concerns

A module should have one reason to change. If describing what a module does requires "and," consider splitting. This applies at every scale: functions, modules, services, teams.

- Describe each module's responsibility in one sentence without using "and" — if you cannot, split it
- Keep UI rendering, business logic, and data access in separate layers that can change independently
- When a change to one feature forces edits in an unrelated feature, treat it as a coupling defect
- Counterweight — locality of behavior: separate by *reason to change*, but co-locate by *reason to read*. If splitting a concern scatters one feature's behavior across many files so you must hop between them to follow it, that fragmentation is its own cost. Separation and locality pull in opposite directions; choose per case rather than maximizing either.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.2 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.1.1 | 2026-06-10 | Mike Fullerton | Cite recovered Tier-1 research sources (adversarially-audited) |
| 1.1.0 | 2026-06-09 | Mike Fullerton | Add locality-of-behavior counterweight; link srp and connascence |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
