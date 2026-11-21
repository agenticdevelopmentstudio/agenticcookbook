--- draft-1.md
+++ draft.md
@@ -18,7 +18,8 @@
   - json-schema
   - validation
 depends-on: []
-related: []
+related:
+  - 2c5ee8e0-9da5-4b44-9f87-51962abe76ab
 references:
   - https://www.rfc-editor.org/rfc/rfc8259.html
   - https://json-schema.org/draft/2020-12/json-schema-core
@@ -75,7 +76,7 @@
 - **cf-required-project-fields**: A project cookbook MUST also have `type`, `name`, `version`, `description`, `author`, `license`, `created`, `modified` and `platforms`. (claim: cf-required-project-fields-prior)
 - **cf-dependencies-in-cookr-config**: Dependencies MUST NOT be listed in `cookbook.json`. Cookbooks this one links into are not listed here: they are `dependencies` in the repo's `.cookr.json` (`references/cookr-config.schema.json`). (claim: cf-dependencies-in-cookr-config-prior)
 - **cf-semver-fields**: The `version` field MUST be a valid semver string matching the pattern `^\d+\.\d+\.\d+$`. (claim: cf-semver-fields-prior)
-- **version-is-semver**: Every `version` in the manifest SHOULD be a Semantic Versioning 2.0.0 version, as Swift Package Manager and npm require of a package version and as Android's guidance points to: three numeric parts, as Cargo requires, each a non-negative integer with no leading zeroes (`1.2.3`, never `01.2.3`), which semver.org's suggested regular expression checks. (claims: semver-normal-version-form, semver-no-leading-zeroes, semver-suggested-regex, swiftpm-version-semver, npm-version-node-semver, android-semver-good-basis, cargo-version-three-numeric-parts)
+- **version-is-semver**: Every `version` in the manifest SHOULD be a Semantic Versioning 2.0.0 version, as Swift Package Manager and npm require of a package version: three numeric parts, as Cargo requires, each a non-negative integer with no leading zeroes (`1.2.3`, never `01.2.3`), which semver.org's suggested regular expression checks. (claims: semver-normal-version-form, semver-no-leading-zeroes, semver-suggested-regex, swiftpm-version-semver, npm-version-node-semver, cargo-version-three-numeric-parts)
 - **released-version-is-immutable**: Once a version of a cookbook is released, its contents MUST NOT be modified: any change is released under a new `version`. (claim: semver-released-version-immutable)
 - **cf-structure-present**: The `structure` field MUST be present and contain at least a `description` field. The structure is the root of the element tree — without it, the cookbook defines nothing to build. (claim: cf-structure-present-prior)
 - **cf-structure-kind**: When present, `structure.kind` MUST be one of `app`, `library`, `plugin`, `widget`. It names what the cookbook assembles. A `library` cookbook specifies a set of reusable components rather than one product. (claim: cf-structure-kind-prior)
@@ -193,7 +194,7 @@
 - Every `pattern` is anchored with `^` and `$`; the UUID patterns match the 8-4-4-4-12 hex-and-dash form; the rdid pattern admits only lowercase letters, digits and hyphens after a leading letter.
 - No field relies on `format` alone while the validator runs without format assertion, and no format's checker package is silently missing.
 - `version` checks: a semver claim that the `^\d+\.\d+\.\d+$` pattern does not keep (it accepts leading zeroes); a released version whose contents changed without a new `version`.
-- Objects closed with `"additionalProperties": false` are closed for typo detection by choice; an object meant to be extended through `allOf` uses `unevaluatedProperties`.
+- Objects closed with `"additionalProperties": false` are closed for typo detection by choice; an object meant to be extended through `allOf`, if closed, is closed with `unevaluatedProperties` rather than `additionalProperties`, or the change says why.
 - Checks the schema cannot make (path existence, paths climbing out with `..`, cycles, cross-file `source.id` resolution, one field compared with another) live in cookr's code and report every failure, not the first.
 - The project rules hold: `type` is `"cookbook"`, the project fields are present, `structure` has a `description`, `structure.kind` is one of the four values, a library's tree is its arrangement, and code roots and dependencies live in `.cookr.json`, not `cookbook.json`.
 - The schema ships with test manifests, run with a real validator, and is compiled strictly.
@@ -249,7 +250,7 @@
 - `schema-date-format`: `created` and `modified` are checked as RFC 3339 full-dates, or the change says why
 - `enable-format-assertion`: no field relies on `format` alone without format assertion on, or the change says why
 - `schema-closed-objects`: each object closed with `"additionalProperties": false` is closed to catch misspelt keys by choice, or the change says why
-- `closed-objects-keep-an-extension-point`: an extension point, when added, is open for other tools and closed objects extended through `allOf` use `unevaluatedProperties`
+- `closed-objects-keep-an-extension-point`: an extension point, when added, is open for other tools, and a closed object extended through `allOf`, when closed with `unevaluatedProperties`, sees its subschemas' properties
 - `validate-the-schema-strictly`: the schema compiles under strict checking, or the change says why
 - `schema-paths-are-strings`: `spec` and each `path` are strings holding relative-path references, or the change says why
 - `schema-structure-kind-enum`: `kind` is typed as the rule writes it
@@ -263,15 +264,15 @@
 
 A cookbook that fails JSON parsing cannot be processed by any tooling, and JSON Schema is defined over JSON documents, so parsing comes first. JSON exchanged between systems outside a closed ecosystem must be UTF-8 with no byte order mark; a shared cookbook leaves the repository it was written in, so it is not a closed ecosystem.
 
-Schema validation catches structural errors (missing fields, wrong types, unknown properties) before any semantic checks run. It cannot make every check: standard JSON Schema has no way to compare one field with another, to look at the file system, or to read another file, so those checks run in code, as Cargo checks a package by building it rather than by parsing its manifest. A validator that stops at the first error makes the author fix a manifest one error at a time; python-jsonschema yields every error, and graphlib names the cycle it finds.
-
-`format` is an annotation unless the validator asserts it: the 2020-12 format-annotation vocabulary requires format evaluation to be off by default, python-jsonschema checks formats only with a format checker hooked in, and Ajv ships without the specification's formats. A schema that relies on `"format": "date"` with assertion off checks nothing. Unknown keywords are treated as annotations too, so a misspelt keyword in the schema constrains nothing unless the schema is compiled strictly.
+Schema validation catches structural errors (missing fields, wrong types, unknown properties) before any semantic checks run. It cannot make every check: standard JSON Schema has no way to compare one field with another, to look at the file system, or to read another file, so those checks run in code, as Cargo's packaging step checks a package by building it, beyond parsing its manifest. A validator that stops at the first error makes the author fix a manifest one error at a time; python-jsonschema yields every error, and graphlib names the cycle it finds.
+
+`format` is an annotation unless the validator asserts it: the 2020-12 format-annotation vocabulary requires format evaluation to be off by default, python-jsonschema checks formats only with a format checker hooked in, and Ajv ships without the specification's formats. A schema that relies on `"format": "date"` with assertion off checks nothing. JSON Schema 2020-12 says unknown keywords should be treated as annotations, so a misspelt keyword in the schema constrains nothing unless the schema is compiled strictly.
 
 Closed objects catch misspelt keys, which is why Cargo warns on unused keys; SchemaStore's maintainers warn against closing objects by reflex, because a property a newer tool adds then becomes an error. Cargo keeps an ignored `package.metadata` table for other tools. `additionalProperties` sees only the properties declared beside it, so a closed object cannot be extended through `allOf`; `unevaluatedProperties` can.
 
 RFC 9562 obsoletes RFC 4122 and represents a UUID as the hex-and-dash string, in upper, lower or mixed case, and recommends treating UUIDs as opaquely as possible. Semantic Versioning 2.0.0 forbids leading zeroes, which `^\d+\.\d+\.\d+$` accepts, and allows pre-release and build suffixes, which it rejects. A released version's contents must not change. Broken spec paths mean the agent cannot find the spec to implement, and a path's `..` segments can carry it outside the cookbook unless it is checked. Circular dependencies make build ordering impossible: a complete build order exists only for a graph without cycles.
 
-The `type` value, the project fields, `structure`, the `kind` values, the library layout, source provenance and code roots are this cookbook's own design; no outside source requires them or argues against them.
+The `type` value, the project fields, `structure`, the `kind` values, the library layout, source provenance and code roots are this cookbook's own design; no outside source requires them, and npm, for one, requires only `name` and `version`, and only of a package it publishes.
 
 ## References
 
