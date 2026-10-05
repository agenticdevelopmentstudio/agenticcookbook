---
id: a7c3e1f2-9b4d-4e6a-8c5f-2d3e4f5a6b7c
title: "Glossary"
domain: agenticdevelopercookbook://introduction/glossary
type: reference
version: 1.4.0
status: accepted
language: en
created: 2026-03-28
modified: 2026-09-25
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Definitions of terms used throughout the Agentic Developer Cookbook."
platforms: []
tags: [glossary, definitions, terminology]
depends-on: []
related:
  - agenticdevelopercookbook://introduction/conventions
references: []
---

# Glossary

Definitions of terms used throughout the Agentic Developer Cookbook.

---

**Agent** — A Claude Code subagent that runs in isolation with scoped tools and permissions. Defined by a `.md` file in `.claude/agents/` with agent-specific frontmatter (`tools`, `permissionMode`, `maxTurns`).

**Conformance** — Verified match between an implementation and a recipe's requirements. Measured by a conformance checklist mapping each named requirement to its implementing code and test.

**Cookbook** — Two distinct uses: (1) **Top-level cookbook** — the source repository of principles, guidelines, ingredients, and recipes (this repo, `agenticdevelopercookbook/cookbook`). (2) **Project cookbook** — a full application, plugin, widget, or library definition that assembles recipes and ingredients into a complete project. Defined by a `cookbook.json` manifest in a directory with a `-cookbook` suffix. Contains a hierarchical structure of structural elements, resources, and context. Replaces the former "concoction" concept. A **library cookbook** (`structure.kind: library`) specifies reusable components and lives in its repository's `cookbook/` directory, its tree mirroring the code.

**Cookbook Artifact** — A general term for any content item in the cookbook: a principle, guideline, ingredient, or recipe. Each artifact is a standalone markdown file with YAML frontmatter, named requirements, and a change history. The artifact's `type` field identifies which kind it is.

**Domain** — A URL-based identifier for any cookbook content. Format: `<scheme>://<path>#<fragment>`. Example: `agenticdevelopercookbook://ingredients/ui/components/empty-state#requirements/centered-layout`.

**Fragment** — A `#section/item` reference to a specific section or item within a document. Used for within-document and cross-document references. Example: `#requirements/ordered-list`.

**Guideline** — A topic-oriented rule that applies during planning and implementation. Covers testing, security, accessibility, internationalization, concurrency, logging, and more. Organized by topic in `cookbook/guidelines/`.

**Ingredient** — An atomic component spec — the building block of recipes. Defines a single UI component, panel, or infrastructure pattern with full detail: behavioral requirements, appearance, states, accessibility, test vectors, configuration options, and platform notes. Located in `cookbook/ingredients/`.

**Principle** — A foundational engineering idea that guides all design decisions. 27 principles in `cookbook/principles/` including simplicity, YAGNI, fail-fast, dependency injection, immutability, composition over inheritance, connascence, and others.

**Recipe** — A composition of configured ingredients into a coherent feature. Defines how ingredients wire together: integration requirements, layout, shared state, and integration test vectors. Recipes reference ingredients by domain and specify configuration values for each. Located in `cookbook/recipes/`.

**Reference Implementation** — A source file or directory, in the cookbook's own repository, that implements an ingredient or recipe. Listed in the spec's `## Reference Implementations` table by platform and repository-relative path; a directory claims every source file below it.

**Requirement** — A named, testable assertion within a recipe. Uses a descriptive kebab-case name and RFC 2119 keywords (MUST, SHOULD, MAY). Example: `**ordered-list**: The control MUST maintain an ordered list of messages.`

**Rule** — An imperative markdown file that enforces behavior during planning or implementation. Installed into a project's `.claude/rules/` directory. Uses RFC 2119 keywords, explicit file paths, and MUST NOT sections. Located in `rules/`.

**Structural Element** — A named node in a cookbook's structure tree. Each structural element has a spec (referencing an ingredient or recipe), a description, optional platform overrides, dependencies on sibling elements, and child structural elements. The recursive nesting of structural elements defines the architecture of a cookbook.

**Skill** — A Claude Code extension that performs a specific task when invoked by name (e.g., `/validate-cookbook`, `/lint-recipe`). Defined by a `SKILL.md` file in a directory under `skills/`.

**Tier** — A participation level determining how much of the cookbook a project adopts. Three tiers, each additive: (1) guidelines and verification, (2) recipe conformance, (3) community contribution.

**Trusted** — The cookbook's core quality standard. Code is trusted when it is complete, precise, consistent, verified, secure by default, accessible from day one, tested alongside, predictable, maintainable, native, incremental, documented, observable, and performant. See the README for the full definition of each dimension.

**Verification** — The post-implementation validation process. Confirms builds pass, tests pass, linting is clean, logging is correct, accessibility is verified, and all applicable guidelines are met.

---

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.4.0 | 2026-09-25 | Mike Fullerton | Library cookbooks: Reference Implementations section and cookbook.json code block |
| 1.3.0 | 2026-04-06 | Mike Fullerton | Rename Concoction to Cookbook; define top-level and project cookbook distinction |
| 1.2.0 | 2026-04-05 | Mike Fullerton | Add Ingredient, Concoction, Structural Element terms; update Recipe and Cookbook Artifact definitions |
| 1.1.0 | 2026-04-04 | Mike Fullerton | Add Cookbook Artifact term |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial glossary |
