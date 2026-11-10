---
id: 66376D65-F0FD-40CF-9614-6A94F2C022C7
title: "Cookbook Formatting Compliance"
type: compliance
version: 2.0.0
status: draft
language: en
created: 2026-04-05
modified: 2026-11-09
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
  - guide/introduction/conventions.md
related:
  - tbd/compliance/artifact-formatting/ingredient-formatting.md
  - tbd/compliance/artifact-formatting/recipe-formatting.md
references: []
---

# Cookbook Formatting Compliance

Cookbooks are JSON manifests that assemble recipes and ingredients into complete applications, plugins, widgets, or libraries. Each cookbook defines a structure tree of structural elements, context for LLM consumption, and resource declarations — all validated against `references/cookbook.schema.json`. Every cookbook, including a source repository like this one, carries its identity in `cookbook.json` (`format`, `id`, `rdid`) and lists its artifacts in `index.json` (`references/index.schema.json`).

## Applicability

This category applies to any `cookbook.json` file. The manifest sits at the root of its cookbook directory; every spec path is relative to that directory.

## Checks

### cf-valid-json

The file MUST be valid JSON. A cookbook that fails JSON parsing cannot be processed by any tooling.

**Applies when:** always.

---

### cf-schema-valid

The file MUST validate against `references/cookbook.schema.json`. Schema validation catches structural errors — missing fields, wrong types, unknown properties — before any semantic checks run.

**Applies when:** always.

---

### cf-type-field

The `type` field MUST be `"cookbook"`. This distinguishes project cookbook manifests from other JSON files in the repository.

**Applies when:** the manifest describes a project (it has a `structure`).

---

### cf-required-fields

The identity fields MUST be present in every manifest: `format` (`2`), `id` and `rdid`. A project cookbook MUST also have `type`, `name`, `version`, `description`, `author`, `license`, `created`, `modified` and `platforms`. Cookbooks this one links into are not listed here: they are `dependencies` in the repo's `.cookr.json` (`references/cookr-config.schema.json`).

**Applies when:** always; the project fields when the manifest has a `structure`.

---

### cf-uuid-format

The `id` field MUST be a valid UUID (RFC 4122). It is the cookbook's identity: a foreign link names it (`<cookbook-uuid>/<artifact-uuid>`), and it stays stable even if the cookbook directory is renamed. The `rdid` MUST be one lowercase kebab-case segment (`adc`); it is the first segment of every rdid in the cookbook's index.

**Applies when:** always.

---

### cf-semver-fields

The `version` field MUST be a valid semver string matching the pattern `^\d+\.\d+\.\d+$`. The manifest format is the whole number `format`, not a semver string.

**Applies when:** `version` is present.

---

### cf-structure-present

The `structure` field MUST be present and contain at least a `description` field. The structure is the root of the element tree — without it, the cookbook defines nothing to build.

**Applies when:** the manifest describes a project. A source cookbook of principles, guidelines, ingredients and recipes has no `structure`.

---

### cf-spec-paths-valid

Every `spec` field in the structure tree MUST reference an existing markdown file (relative to the cookbook directory). Broken spec paths mean the agent cannot find the spec to implement.

**Applies when:** any structural element contains a `spec` field.

---

### cf-source-domains

Every `source.id` field MUST be the UUID of an ingredient or recipe, written `<cookbook-uuid>/<artifact-uuid>` when it is another cookbook's, and MUST resolve in that cookbook's `index.json`. Source provenance ties forked specs back to their cookbook origin.

**Applies when:** any structural element contains a `source` object.

---

### cf-structure-kind

When present, `structure.kind` MUST be one of `app`, `library`, `plugin`, `widget`. It names what the cookbook assembles. A `library` cookbook specifies a set of reusable components rather than one product.

**Applies when:** `structure.kind` is present.

---

### cf-library-layout

In a `library` cookbook the directory tree under the cookbook directory is the arrangement: each directory is a group of components and each ingredient or recipe file is one component, named by its file name. The tree SHOULD mirror the arrangement of the code its implementations (in `index.json`) point at. `structural-elements` MAY be omitted; when present it MUST NOT contradict the directory tree.

**Applies when:** `structure.kind` is `library`.

---

### cf-code-roots

`cookbook.json` MUST NOT carry a `code` block: code roots are tool configuration and live in the repo's `.cookr.json` (`references/cookr-config.schema.json`). There, each root MUST name an existing directory (`path`, relative to the repository root) and a `platform` (`macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`), and MAY give a `kind` (`ui` or `logic`), a `group` (the cookbook folder its recipes belong in) and an `ignore` list of globs; top-level `ignore` globs apply to every root. Every source file under a root MUST be covered by some artifact's implementations; `cookr coverage` reports the files that are not.

**Applies when:** the repo has a `.cookr.json` with `roots`.

**Guidelines:**
- [adc.check.artifact-formatting.ingredient-formatting.if-reference-implementations](cookbook:13785c4f-b4c5-5017-bb90-069232beb6b7)

---

### cf-no-circular-deps

The `depends-on` dot-paths in the structure tree MUST NOT form circular dependencies. Circular dependencies make build ordering impossible.

**Applies when:** any structural element contains a `depends-on` array.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-11-09 | Mike Fullerton | cookr format 2: UUID identity and rdids replace `domain`; implementations live in index.json |
| 1.1.0 | 2026-09-25 | Mike Fullerton | Library cookbooks: Reference Implementations section and cookbook.json code block |
| 1.0.0 | 2026-04-05 | Mike Fullerton | Initial creation |
