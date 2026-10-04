---
id: 555ad5e1-800f-4848-8c58-6f726bdcb42b
title: "Manage complexity through boundaries"
domain: agenticdevelopercookbook://principles/manage-complexity-through-boundaries
type: principle
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Well-defined boundaries let subsystems evolve independently. Define ports the app owns, use thin adapters to external technologies, and test the core without databases, UIs, or networks."
platforms: []
tags:
  - manage-complexity-through-boundaries
depends-on: []
related:
  - agenticdevelopercookbook://principles/composition-over-inheritance
  - agenticdevelopercookbook://principles/connascence
  - agenticdevelopercookbook://principles/steel-thread-first
  - agenticdevelopercookbook://principles/yagni
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
---

# Manage complexity through boundaries

Well-defined boundaries between subsystems let each side evolve independently. Define ports (interfaces) that describe what the application needs. Use adapters to translate between external technologies and your ports. Test the core application without databases, UIs, or networks.

- Define each external dependency as a protocol the app owns, not a concrete type the vendor owns
- Keep adapter implementations thin — translate and delegate, never add business logic
- If two modules need to share a type, extract it into a shared contract rather than coupling the modules directly
- Verify boundaries by confirming core logic compiles and tests pass with no framework imports
- Extend at the boundary, don't break the contract: once a boundary is stable and widely depended on, add capability through new implementations behind the port rather than changing the port's existing shape — the durable kernel of the open/closed principle. Apply it only to boundaries that have actually stabilized; do not pre-generalize one you are still discovering (see yagni, steel-thread-first).

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.1.0 | 2026-06-09 | Mike Fullerton | Fold open/closed kernel (extend behind stable ports); link composition, connascence, steel-thread-first, yagni |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
