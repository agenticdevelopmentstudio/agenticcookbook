---
id: 3B566ED1-AD27-4E6C-8938-62C159DBC5FF
title: "RecipeName"
type: recipe
version: 2.0.0
status: accepted
language: en
created: 2026-04-05
modified: 2026-11-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: ""
platforms:
  - kotlin
  - swift
  - typescript
  - web
tags: []
ingredients:
  - <ingredient-uuid>   # or its rdid, adc.ingredient.<path>; `cookr update` stores the UUID
depends-on: []
related: []
references: []
approved-by: ""
approved-date: ""
---

# RecipeName

## Overview

Brief description of what this feature is and when to use it.

## Ingredients

| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| | [adc.ingredient.<path>](cookbook:<ingredient-uuid>) | | Yes/No | |

## Integration Requirements

- **do-something**: The recipe MUST ...
- **do-something-else**: The recipe SHOULD ...

## Layout

Describe how ingredients are spatially or logically arranged. Use ASCII diagrams for UI recipes, flow diagrams for infrastructure recipes.

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| | | | one-way/two-way | |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| recipe-001 | do-something | | |

## Edge Cases

- Describe composition-level boundary conditions and error states

## Platform Notes

- **SwiftUI**:
- **Compose**:
- **React/Web**:
- **AppKit / UIKit**:
- **WinUI 3**:

<!-- No `## Reference Implementations` section is authored. Record the code that implements this
recipe with `cookr implements <uuid|rdid> <location> --platform <p>` and `cookr confirm <uuid|rdid>`;
a compiled doc or skill shows those rows as a derived section here. -->

## Design Decisions

Record any decisions made during implementation that affect integration behavior. Each decision should be approved by the user.

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [adc.check.<document>.<check-name>](cookbook:<check-uuid>) | passed | Category |

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-11-09 | Mike Fullerton | cookr format 2: UUID links and rdids; Reference Implementations derived from index.json, not authored |
| 1.1.0 | 2026-09-25 | Mike Fullerton | Library cookbooks: Reference Implementations section and cookbook.json code block |
| 1.0.0 | 2026-04-05 | Mike Fullerton | Initial creation |
