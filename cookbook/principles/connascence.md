---
id: ec59e5cc-5591-4c0b-87f8-00df54394607
title: "Connascence"
domain: agenticdevelopercookbook://principles/connascence
type: principle
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Coupling has a rankable strength; a good refactor moves it to a weaker form, and weaker still as distance grows."
platforms: []
tags:
  - connascence
  - coupling
depends-on: []
related:
  - agenticdevelopercookbook://principles/separation-of-concerns
  - agenticdevelopercookbook://principles/manage-complexity-through-boundaries
  - agenticdevelopercookbook://principles/explicit-over-implicit
references:
  - https://en.wikipedia.org/wiki/Connascence
  - https://thoughtbot.com/blog/connascence-as-a-vocabulary-to-discuss-coupling
  - https://connascence.io/pages/about.html
  - https://coupling.dev/posts/related-topics/connascence/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
---

# Connascence

Coupling is not binary — it has a *strength* you can rank, and a good refactor moves it to a weaker form. Connascence names the ways two pieces of code must change together. Two rules govern it: **minimize** overall connascence by keeping coupled things close, and **weaken** strong forms into weaker ones as the distance between them grows. This turns "this feels too coupled" into an objective call.

- Rank, don't just detect: judge each coupling on three axes — strength (how hard it is to change in concert), degree (how many elements share it), and locality (how far apart they live). A positional dependency is stronger than a name dependency; a shared magic value (connascence of meaning) is stronger still.
- Weaken with distance: the same coupling is cheap inside one function and expensive across two services. The farther apart two coupled elements live, the weaker the form between them must be — e.g. positional args → named parameters → a typed message across a boundary.
- Prefer the weakest form that does the job: replace positional arguments with named ones, magic numbers with named constants, duck-typed shapes with explicit types.
- Use it as the vocabulary for coupling reviews: "connascence of position across a module boundary — convert to connascence of name" is a decision, not a matter of taste.
- Reference lattice (weak → strong): static — name < type < meaning < position < algorithm; dynamic — execution < timing < value < identity. Reach for the full lattice only when the three axes above don't settle the call.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Cite recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
