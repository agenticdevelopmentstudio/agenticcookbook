---
id: 56394d2f-b784-4771-92a4-faacc037c609
title: "Shared components and tiers"
domain: agenticdevelopercookbook://guidelines/implementing/code-quality/shared-components-and-tiers
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Search for what already exists, put code in the lowest tier that can hold it, point dependencies downward, keep features in shared tiers with apps as thin shells, and organize files into encapsulated directories."
platforms: []
tags:
  - architecture
  - reuse
  - tiers
  - code-quality
depends-on: []
related:
  - agenticdevelopercookbook://principles/dry
  - agenticdevelopercookbook://principles/separation-of-concerns
  - agenticdevelopercookbook://principles/manage-complexity-through-boundaries
  - agenticdevelopercookbook://guidelines/implementing/code-quality/architecture
  - agenticdevelopercookbook://guidelines/implementing/code-quality/dependency-injection
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - new-module
  - code-review
---

# Shared components and tiers

Build upward from the most basic shared pieces, and treat each assembly as a shared piece in its own right. The usual failure is quiet: a well-made component is written inside the feature that first needed it, next to an equivalent one the shared layer already offers. Where a repo declares its tiers (for example in `.abstractr.json`, read with the `abstractr` tool), the tools can check these rules. Where it does not, apply them by judgment.

## Search before you write

- Before creating a source file or a new component, look for what already exists: the repo's tier table, its list of shared exports, and a text search for the concept under several names. Search for "button" and "control", not only the exact filename you had in mind.
- If something close exists, extend or reuse it. Build a new one only when you can say why the existing one cannot serve.
- A new file in a shared tier is allowed, and is how the tier grows. Check that it does not duplicate an existing component under a different name.
- Say what you reused, and what you chose not to reuse and why.

## The lowest tier that can hold it

- Place each piece in the lowest tier whose dependencies it can live with. If it needs only the foundation, it belongs in the foundation tier, not in the feature that needed it first.
- Code written one tier too high is invisible to every sibling that will need it next. Moving it down later costs more than placing it right now.
- Do not create a new tier, framework or target to hold a feature. Adding one is a decision for the project owner.
- Ask of each piece: could a command-line tool link this without the application? If it reads an application settings singleton or an app-only type, pass that value in as a parameter, and the piece moves down.

## Dependencies point downward

- A lower tier MUST NOT import from a higher one. The foundation knows nothing about the features built on it.
- When a lower tier needs something from above, invert the dependency: define a protocol or callback in the lower tier and let the higher tier supply it.
- A cycle between tiers means the shared part belongs in a tier below both. Extract it rather than allowing the cycle.
- This is separation of concerns applied to layers. It limits what a change can break, and lets each tier be understood by itself.

## Features live in shared tiers, apps are shells

- A feature's models, service protocol, client, storage, logic and views go into the repo's existing shared tiers. Any application (a GUI, a daemon, a command-line tool) then assembles the feature from them.
- What legitimately stays in an application: the entry point, config files, and aggregation code, meaning menu assembly, dependency wiring, and thin adapters that bind a shared protocol to that application's data or transport.
- Split a feature by what each piece needs. Models and pure logic go to the foundation, persistence to the storage tier, views to the UI tier, transport clients to the IPC tier, and only the glue stays in the app.
- If a feature exists only in app code, no other app can use it, and the next app will rebuild it.

## Organize into encapsulated directories

- Every file lives inside a directory that names its purpose and belongs to a declared tier. Do not leave source files strewn at the top level of a repo or package.
- Keep a directory cohesive: what is inside changes together and is reached through a small public surface. Details that other code should not touch stay inside it.
- Group by concept, not by file type, so a reader finds a feature in one place.
- When a path belongs to no declared tier, move the file into one. Do not add a tier just to hold it.

## Why this matters

A component written one tier too high is invisible to its siblings, so each rebuilds its own. Placing code in the lowest tier that can hold it, and keeping dependencies pointing down, means features compose from shared parts and a change stays inside its boundary.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
