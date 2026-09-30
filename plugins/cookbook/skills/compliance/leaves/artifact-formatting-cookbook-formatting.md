<!-- leaf: compliance/artifact-formatting-cookbook-formatting · source: compliance/artifact-formatting/cookbook-formatting.md -->

**Rules** (cite as `compliance/artifact-formatting-cookbook-formatting#<slug>`):

- `file-valid-json-cookbook-fails` MUST — The file MUST be valid JSON. A cookbook that fails JSON parsing cannot be processed by any tooling.
- `file-validate-against-reference-cookbook` MUST — The file MUST validate against reference/cookbook.schema.json. Schema validation catches structural errors — missing …
- `type-field-cookbook-distinguishes-cookbook-manifests` MUST — The type field MUST be "cookbook". This distinguishes cookbook manifests from other JSON files in the repository.
- `top-level-fields-present-type-schema-version` MUST — All required top-level fields MUST be present: type, schema_version, name, id, version, description, author, license, …
- `id-field-valid-uuid-rfc-4122` MUST — The id field MUST be a valid UUID (RFC 4122). The UUID serves as a stable identity even if the cookbook directory is …
- `schema-version-version-valid-semver-strings-matching` MUST — Fields schema_version and version MUST be valid semver strings matching the pattern ^\d+\.\d+\.\d+$.
- `structure-field-present-contain-least-description` MUST — The structure field MUST be present and contain at least a description field. The structure is the root of the element …
- `field-structure-tree-reference-existing-markdown-file` MUST — Every spec field in the structure tree MUST reference an existing markdown file (relative to the cookbook directory). …
- `source-domain-field-valid-agenticdevelopercookbook-ingredients-agenticdevelopercookbook` MUST — Every source.domain field MUST be a valid agenticdevelopercookbook://ingredients/ or …
- `paths-structure-tree-not-form-circular-dependencies-circular` MUST — The depends-on dot-paths in the structure tree MUST NOT form circular dependencies. Circular dependencies make build …

# Cookbook Formatting Compliance

Cookbooks are JSON manifests that assemble recipes and ingredients into complete applications, plugins, or widgets. Each cookbook defines a structure tree of structural elements, context for LLM consumption, and resource declarations — all validated against `reference/cookbook.schema.json`.

## Applicability

This category applies to any `cookbook.json` file.

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

### cf-no-circular-deps

The `depends-on` dot-paths in the structure tree MUST NOT form circular dependencies. Circular dependencies make build ordering impossible.

**Applies when:** any structural element contains a `depends-on` array.
