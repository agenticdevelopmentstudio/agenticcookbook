---
description: >-
  The {{count}} engineering principles and the pipeline concerns that guide
  every code change, review and design decision. Use before writing,
  modifying or reviewing code, or when making a design decision.
groups:
  - title: Engineering
    default: true
  - title: Ideation
    tags: [brainstorming]
  - title: Research
    tags: [research]
  - title: Meta
    tags: [meta-principle-optimize-for-change]
---
# General principles

These are heuristics for judgment calls, not rigid rules. Keep them in mind for
every change, small ones included. When two conflict, prefer the one that
leaves the most room to change direction tomorrow: **optimize for change**.

In a review or a design decision, name the principle a change advances or
violates instead of appealing to taste. When principles are in tension, name
them so the choice is explicit.

{{principles}}

## Concerns every implementation applies

{{always}}

## Concerns to raise before building

Ask whether each of these applies. Don't assume either way.

{{ask}}

## Full text

Each name in backticks is a routed skill holding the full principle or
guideline. Read one with `skill-router show <name>`, passing your host and
model as the skill-router skill says.
