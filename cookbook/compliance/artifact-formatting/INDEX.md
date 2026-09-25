---
id: 72DAFECD-184A-4974-9EEC-3FCE8D9447A6
title: "Artifact Formatting Compliance"
domain: agenticdevelopercookbook://compliance/artifact-formatting/INDEX
type: reference
version: 1.3.0
status: draft
language: en
created: 2026-04-04
modified: 2026-09-25
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Index of structural formatting checks for cookbook artifacts — principles, guidelines, ingredients, recipes, and cookbooks."
platforms: []
tags:
  - compliance
  - artifact-formatting
  - index
depends-on:
  - agenticdevelopercookbook://introduction/conventions
related:
  - agenticdevelopercookbook://compliance/INDEX
references: []
---

# Artifact Formatting Compliance

Structural formatting checks for cookbook artifacts. Each artifact type (principle, guideline, ingredient, recipe, cookbook) has its own set of checks defining the required sections, ordering, and content rules. These checks are the authoritative spec that `/lint-artifact` and `/approve-artifact` evaluate against.

## Architecture

```
/lint-artifact  →  Formatting Checks  →  Conventions  →  Frontmatter Standard
/approve-artifact     (this category)      (introduction/conventions.md)
```

- **Formatting checks** define required structure per artifact type
- **Conventions** define the shared frontmatter and cross-referencing rules all artifacts share
- Checks here govern the artifact's markdown structure, not the code it describes

## Sub-Categories

| Category | File | Checks | Scope |
|----------|------|--------|-------|
| Principle Formatting | [principle-formatting.md](principle-formatting.md) | 7 | Required structure for principle artifacts |
| Guideline Formatting | [guideline-formatting.md](guideline-formatting.md) | 8 | Required structure for guideline artifacts |
| Ingredient Formatting | [ingredient-formatting.md](ingredient-formatting.md) | 17 | Required structure for ingredient artifacts |
| Recipe Formatting | [recipe-formatting.md](recipe-formatting.md) | 15 | Required structure for recipe artifacts (compositions) |
| Cookbook Formatting | [cookbook-formatting.md](cookbook-formatting.md) | 13 | Required structure for cookbook manifests (JSON) |

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.3.0 | 2026-09-25 | Mike Fullerton | Library cookbooks: Reference Implementations section and cookbook.json code block |
| 1.2.0 | 2026-04-06 | Mike Fullerton | Rename concoction to cookbook |
| 1.1.0 | 2026-04-05 | Mike Fullerton | Add ingredient and concoction formatting categories |
| 1.0.0 | 2026-04-04 | Mike Fullerton | Initial creation |
