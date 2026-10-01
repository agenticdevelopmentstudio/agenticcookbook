---
id: 60f8370a-6bef-4e18-aeb5-c2cea210bd5d
title: "Library Cookbooks and Reference Implementations"
domain: agenticdevelopercookbook://appendix/decisions/library-cookbooks
type: reference
version: 1.0.0
status: draft
language: en
created: 2026-09-25
modified: 2026-09-25
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "A cookbook can specify a library of reusable components, living in the repository that implements them: a cookbook/ directory whose tree mirrors the code, specs that name their implementations, and a cookbook.json `code` block that replaces cookr's .cookr.json."
platforms: []
tags:
  - architecture
  - project-format
  - cookr
depends-on:
  - agenticdevelopercookbook://appendix/decisions/ingredient-recipe-cookbook-hierarchy
related:
  - agenticdevelopercookbook://compliance/artifact-formatting/cookbook-formatting
  - agenticdevelopercookbook://introduction/conventions
references: []
---

# Library Cookbooks and Reference Implementations

## Problem

A cookbook (`cookbook.json`) described one product to generate: an app, a plugin or a widget. A shared component library had no place in the format, so recipes extracted from a library's code by `cookr` lived in a flat `recipes/` directory configured by a separate `.cookr.json` file. At scale that broke down:

1. **Names encoded the arrangement.** A flat directory has one namespace, so cookr prefixed each name with its tier and source path to keep it unique (`ai-plugin-runtime-ai-plugin-kit-ai-chat-context`). The arrangement of the code was lost in a string.
2. **The mapping from spec to code was a side table.** `.cookr.json` `renames` and `aliases` assigned source files to recipes by rule, far from the recipes themselves. In one library the file reached 107 KB, with 719 renames and 256 ignore patterns.
3. **Two formats described one thing.** `cookbook.json` and `.cookr.json` each claimed to describe a codebase's components, and neither knew about the other.

## Decision

### A library is a kind of cookbook

`structure.kind` names what a cookbook assembles: `app`, `library`, `plugin` or `widget`. A **library cookbook** specifies a set of reusable components. Its directory tree is its arrangement: each directory is a group, and each ingredient or recipe file is one component, named by its file name alone. The tree mirrors the arrangement of the code, so `cookbook/ai-plugin-kit/models/model-capability.md` specifies the model-capability component of the AI plugin kit. `structural-elements` may be omitted; the directory tree is authoritative.

### The cookbook lives in its repository

A cookbook that specifies code in the same repository is that repository's `cookbook/` directory, with `cookbook/cookbook.json` at its root. A standalone cookbook directory keeps the `-cookbook` suffix. Spec domains follow the path: `<scheme>://cookbook/<group>/<name>`, where the scheme is the repository's name.

### Specs name their implementations

Every ingredient and recipe gains a `## Reference Implementations` section, after `## Platform Notes`: a `| Platform | Path |` table naming each source file or directory that implements the spec, relative to the repository root. A directory path claims every source file below it. The spec is now the single place that says which code implements it, replacing `renames` and `aliases`. In a cookbook with no code the section is omitted or is one `Not applicable` line.

### `code` replaces `.cookr.json`

`cookbook.json` gains an optional `code` block: `roots` (source directories, each with a `platform`, an optional `kind` of `ui` or `logic`, an optional `recipes` directory for new specs, and an optional `ignore` list) and a repository-wide `ignore` list. The roots exist only to find source files no spec claims yet. cookr reads `cookbook/cookbook.json` and no longer reads `.cookr.json`; `cookr organize` converts a flat `.cookr.json` corpus into a library cookbook once.

## Consequences

- A component's identity is its path in the cookbook, not a derived string, so two groups can each hold a `catalog.md`.
- When code moves, the specs' paths go stale and `cookbook validate` reports them; `cookr relink` rewrites them from git's rename record.
- When the cookbook tree and the code tree disagree, `cookr arrangement` reports where, and either side can move to match.

## Change History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2026-09-25 | Mike Fullerton | Initial decision |
