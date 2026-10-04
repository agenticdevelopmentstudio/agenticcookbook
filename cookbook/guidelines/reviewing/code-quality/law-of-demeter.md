---
id: f4acb6cd-1e5b-4175-9556-327506a188fe
title: "Law of Demeter and Tell, Don't Ask"
domain: agenticdevelopercookbook://guidelines/reviewing/code-quality/law-of-demeter
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Talk only to immediate collaborators and tell objects to act rather than asking for their internals, except across documented boundary, builder, and pipeline cases."
platforms: []
tags:
  - coupling
  - code-quality
  - design
depends-on: []
related:
  - agenticdevelopercookbook://principles/connascence
  - agenticdevelopercookbook://principles/separation-of-concerns
references:
  - https://en.wikipedia.org/wiki/Law_of_Demeter
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - code-review
---

# Law of Demeter and Tell, Don't Ask

The Law of Demeter (a "principle of least knowledge") says a method **SHOULD** talk only to its immediate collaborators, not to objects it reaches through them. The related "Tell, Don't Ask" heuristic says you **SHOULD** tell an object to do something rather than ask for its internals and act on them yourself. Both reduce coupling, but both have well-known exceptions — apply them as SHOULD-level review signals, not absolute rules.

## What a method may talk to

A method **SHOULD** only send messages to:

- `this` / `self`
- its own parameters
- objects it creates directly
- its own direct fields/properties
- (in some formulations) globals/singletons it holds — treat these with suspicion regardless

## Detecting violations (greppable signals)

- **Train wrecks**: a chain that walks through structure to reach a target, e.g. `a.getB().getC().doThing()`. Each `.` that traverses a *returned* object (not a fluent self-return) is a violation candidate.
- **Feature envy**: a method that pulls several fields off another object to compute something. The computation **SHOULD** likely live on that object instead.
- **Ask-then-act**: code that queries an object's state and then branches/mutates based on it. Prefer telling the object to perform the action.

A reviewer **MUST** treat a train wreck as a *refactor signal*, not an automatic defect — confirm it crosses object boundaries before flagging.

## Relationship to connascence

A Demeter chain is **connascence of position across object boundaries**: the caller is coupled to the shape of intermediate objects, so a change to any link breaks the caller. Removing the chain (via a delegating method or by relocating behavior) converts strong, distant coupling into weaker, local coupling. See `agenticdevelopercookbook://principles/connascence`.

## Refactoring a violation

- **Add a delegating method**: replace `order.getCustomer().getAddress().getZip()` with `order.shippingZip()`.
- **Move behavior (Tell, Don't Ask)**: replace `if (account.getBalance() < amt) ...` with `account.withdraw(amt)` that enforces the rule internally.

## Exceptions — do NOT flag these (IMPORTANT)

Strict application causes wrapper/delegation bloat and fights idiomatic code. A method chain is **acceptable** and **SHOULD NOT** be flagged when:

- **Fluent builders / DSLs**: `builder.with(x).with(y).build()` — each call returns the same builder, not a traversed collaborator.
- **Immutable pipelines**: `items.map(...).filter(...).reduce(...)` and similar LINQ/stream/sequence chains operate on transformed values, not nested object internals.
- **Boundary DTOs / config / response models**: data-holder objects (parsed JSON, protobuf messages, config trees) exist to be read; navigating their fields is their purpose.
- **Standard-library and framework value types**: e.g. dates, paths, URIs.

Because of these cases, this guideline is SHOULD-level. A reviewer **MUST NOT** demand a wrapper method whose only job is to relay one call to a stable data object — that trades real coupling for ceremony.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
