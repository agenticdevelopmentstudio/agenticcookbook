---
id: 66376D65-F0FD-40CF-9614-6A94F2C022C7
title: "Cookbook Formatting Compliance"
domain: agenticdevelopercookbook://compliance/artifact-formatting/cookbook-formatting
type: compliance
version: 1.1.0
status: draft
language: en
created: 2026-04-05
modified: 2026-09-25
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Structural formatting checks for cookbook manifests — JSON files that assemble recipes and ingredients into complete applications."
platforms: []
tags:
  - compliance
  - artifact-formatting
  - cookbook
depends-on:
  - agenticdevelopercookbook://introduction/conventions
related:
  - agenticdevelopercookbook://compliance/artifact-formatting/ingredient-formatting
  - agenticdevelopercookbook://compliance/artifact-formatting/recipe-formatting
references: []
---

# Cookbook Formatting Compliance

Cookbooks are JSON manifests that assemble recipes and ingredients into complete applications, plugins, widgets, or libraries. Each cookbook defines a structure tree of structural elements, context for LLM consumption, and resource declarations — all validated against `reference/cookbook.schema.json`.

## Applicability

This category applies to any `cookbook.json` file. The manifest sits at the root of its cookbook directory; every spec path is relative to that directory.

## Checks

### cf-valid-json

The file MUST be valid JSON. A cookbook that fails JSON parsing cannot be processed by any tooling.

**Applies when:** always.

---

### cf-schema-valid

The file MUST validate against `reference/cookbook.schema.json`. Schema validation catches structural errors — missing fields, wrong types, unknown properties — before any semantic checks run.

**Applies when:** always.

---

### cf-type-field

The `type` field MUST be `"cookbook"`. This distinguishes cookbook manifests from other JSON files in the repository.

**Applies when:** always.

---

### cf-required-fields

All required top-level fields MUST be present: `type`, `schema_version`, `name`, `id`, `version`, `description`, `author`, `license`, `created`, `modified`, `platforms`, `cookbook`.

**Applies when:** always.

---

### cf-uuid-format

The `id` field MUST be a valid UUID (RFC 4122). The UUID serves as a stable identity even if the cookbook directory is renamed.

**Applies when:** always.

---

### cf-semver-fields

Fields `schema_version` and `version` MUST be valid semver strings matching the pattern `^\d+\.\d+\.\d+$`.

**Applies when:** always.

---

### cf-structure-present

The `structure` field MUST be present and contain at least a `description` field. The structure is the root of the element tree — without it, the cookbook defines nothing to build.

**Applies when:** always.

---

### cf-spec-paths-valid

Every `spec` field in the structure tree MUST reference an existing markdown file (relative to the cookbook directory). Broken spec paths mean the agent cannot find the spec to implement.

**Applies when:** any structural element contains a `spec` field.

---

### cf-source-domains

Every `source.domain` field MUST be a valid `agenticdevelopercookbook://ingredients/` or `agenticdevelopercookbook://recipes/` domain. Source provenance ties forked specs back to their cookbook origin.

**Applies when:** any structural element contains a `source` object.

---

### cf-structure-kind

When present, `structure.kind` MUST be one of `app`, `library`, `plugin`, `widget`. It names what the cookbook assembles. A `library` cookbook specifies a set of reusable components rather than one product.

**Applies when:** `structure.kind` is present.

---

### cf-library-layout

In a `library` cookbook the directory tree under the cookbook directory is the arrangement: each directory is a group of components and each ingredient or recipe file is one component, named by its file name. The tree SHOULD mirror the arrangement of the code its Reference Implementations point at. `structural-elements` MAY be omitted; when present it MUST NOT contradict the directory tree.

**Applies when:** `structure.kind` is `library`.

---

### cf-code-roots

When present, `code.roots` MUST be a non-empty list, and each root MUST name an existing directory (`path`, relative to the repository root), a `platform` (`web`, `apple`, `android`, `windows`, `python`), and MAY give a `kind` (`ui` or `logic`), a `recipes` directory (relative to the cookbook directory) where specs for its unclaimed source files are written, and an `ignore` list of globs. `code.ignore` globs apply to every root. The roots name where source lives so tooling can find source files no spec's Reference Implementations claim yet.

**Applies when:** `code` is present.

**Guidelines:**
- [Ingredient Formatting](agenticdevelopercookbook://compliance/artifact-formatting/ingredient-formatting#if-reference-implementations)

---

### cf-no-circular-deps

The `depends-on` dot-paths in the structure tree MUST NOT form circular dependencies. Circular dependencies make build ordering impossible.

**Applies when:** any structural element contains a `depends-on` array.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-09-25 | Mike Fullerton | Library cookbooks: Reference Implementations section and cookbook.json code block |
| 1.0.0 | 2026-04-05 | Mike Fullerton | Initial creation |
