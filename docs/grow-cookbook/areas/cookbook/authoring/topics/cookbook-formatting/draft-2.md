---
id: 4c7be774-12c6-4bf0-a9ee-82e8633610dc
title: "Cookbook Formatting"
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-21
modified: 2026-11-21
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Rules for cookbook.json and its schema: UTF-8 JSON, identity fields, UUIDs, semver, paths, acyclic depends-on, and checks kept in schema or code."
platforms: []
tags:
  - cookbook
  - manifest
  - json-schema
  - validation
depends-on: []
related:
  - 2c5ee8e0-9da5-4b44-9f87-51962abe76ab
references:
  - https://www.rfc-editor.org/rfc/rfc8259.html
  - https://json-schema.org/draft/2020-12/json-schema-core
  - https://json-schema.org/draft/2020-12/json-schema-validation
  - https://www.ietf.org/archive/id/draft-ietf-jsonschema-json-schema-04.html
  - https://json-schema.org/understanding-json-schema/reference/object
  - https://www.rfc-editor.org/rfc/rfc9562.html
  - https://www.rfc-editor.org/rfc/rfc4122.html
  - https://www.rfc-editor.org/rfc/rfc3986.html
  - https://www.rfc-editor.org/rfc/rfc3339.html
  - https://semver.org/
  - https://spdx.org/licenses/
  - https://python-jsonschema.readthedocs.io/en/stable/validate/
  - https://ajv.js.org/guide/formats.html
  - https://ajv.js.org/strict-mode.html
  - https://ajv.js.org/guide/combining-schemas.html
  - https://docs.npmjs.com/cli/v10/configuring-npm/package-json
  - https://doc.rust-lang.org/cargo/reference/manifest.html
  - https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html
  - https://doc.rust-lang.org/cargo/commands/cargo-package.html
  - https://bazel.build/concepts/dependencies
  - https://go.dev/ref/spec
  - https://docs.python.org/3/library/graphlib.html
  - https://developer.android.com/studio/publish/versioning
  - https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html
  - https://code.visualstudio.com/docs/languages/json
  - https://github.com/SchemaStore/schemastore/blob/master/CONTRIBUTING.md
  - https://github.com/json-schema-org/JSON-Schema-Test-Suite
  - https://github.com/coveooss/json-schema-for-humans
  - https://blog.cloudflare.com/cloudflares-json-powered-documentation-generator/
approved-by: ""
approved-date: ""
triggers:
  - recipe-authoring
  - configuration
---

# Cookbook Formatting

A cookbook's `cookbook.json` is UTF-8 JSON that validates against `references/cookbook.schema.json` and carries the cookbook's identity (`format`, `id`, `rdid`); a project cookbook adds the fields and the structure tree it assembles. The schema checks the shape; cookr's code checks what a schema cannot, such as paths that resolve and a `depends-on` graph without cycles, and reports every error it finds.

## Rules

- **cf-valid-json**: The file MUST be valid JSON: text that conforms to the JSON grammar of RFC 8259, which every conforming JSON parser accepts. (claim: rfc8259-parser-accepts-grammar)
- **manifest-is-utf8-without-bom**: The file MUST be encoded in UTF-8 and MUST NOT begin with a byte order mark (U+FEFF). (claims: rfc8259-utf8-exchange, rfc8259-no-bom)
- **no-duplicate-member-names**: The member names within each object of the file SHOULD be unique: software that reads an object with duplicate names behaves unpredictably, and a schema validator sees only the member its parser kept. (claims: rfc8259-names-should-be-unique, rfc8259-duplicate-names-unpredictable)
- **cf-schema-valid**: The file MUST validate against `references/cookbook.schema.json`, checked with a real JSON Schema validator. (claims: schemastore-validate-with-ajv, python-jsonschema-iter-errors)
- **cf-required-identity-fields**: The identity fields MUST be present in every manifest: `format` (`2`), `id` and `rdid`. (claims: jsonschema-required-keyword, jsonschema-const-keyword, npm-name-version-unique-identifier)
- **cf-format-is-integer**: The manifest format MUST be the whole number `format`, not a semver string: the version programs compare is kept apart from the version people read. (claims: jsonschema-const-keyword, android-versioncode-integer)
- **cf-uuid-format**: The `id` field MUST be a valid UUID (RFC 4122). It is the cookbook's identity: a foreign link names it (`<cookbook-uuid>/<artifact-uuid>`), and it stays stable even if the cookbook directory is renamed. (claim: cf-uuid-format-prior)
- **uuid-compared-not-parsed**: Tools SHOULD treat the `id` and every `source.id` UUID as opaque: compare them without regard to letter case, and not parse their fields for meaning. (claims: rfc9562-treat-uuids-opaquely, rfc9562-mixed-case, rfc4122-lowercase-output)
- **cf-rdid-format**: The `rdid` MUST be one lowercase kebab-case segment (`adc`); it is the first segment of every rdid in the cookbook's index. (claims: npm-name-no-uppercase, cargo-name-characters)
- **cf-type-field**: The `type` field MUST be `\"cookbook\"`. This distinguishes project cookbook manifests from other JSON files in the repository. (claim: cf-type-field-prior)
- **cf-required-project-fields**: A project cookbook MUST also have `type`, `name`, `version`, `description`, `author`, `license`, `created`, `modified` and `platforms`. (claim: cf-required-project-fields-prior)
- **cf-dependencies-in-cookr-config**: Dependencies MUST NOT be listed in `cookbook.json`. Cookbooks this one links into are not listed here: they are `dependencies` in the repo's `.cookr.json` (`references/cookr-config.schema.json`). (claim: cf-dependencies-in-cookr-config-prior)
- **cf-semver-fields**: The `version` field MUST be a valid semver string matching the pattern `^\d+\.\d+\.\d+$`. (claim: cf-semver-fields-prior)
- **version-is-semver**: Every `version` in the manifest SHOULD be a Semantic Versioning 2.0.0 version, as Swift Package Manager and npm require of a package version: three numeric parts, as Cargo requires, each a non-negative integer with no leading zeroes (`1.2.3`, never `01.2.3`), which semver.org's suggested regular expression checks. (claims: semver-normal-version-form, semver-no-leading-zeroes, semver-suggested-regex, swiftpm-version-semver, npm-version-node-semver, cargo-version-three-numeric-parts)
- **released-version-is-immutable**: Once a version of a cookbook is released, its contents MUST NOT be modified: any change is released under a new `version`. (claim: semver-released-version-immutable)
- **cf-structure-present**: The `structure` field MUST be present and contain at least a `description` field. The structure is the root of the element tree — without it, the cookbook defines nothing to build. (claim: cf-structure-present-prior)
- **cf-structure-kind**: When present, `structure.kind` MUST be one of `app`, `library`, `plugin`, `widget`. It names what the cookbook assembles. A `library` cookbook specifies a set of reusable components rather than one product. (claim: cf-structure-kind-prior)
- **cf-library-tree-is-arrangement**: A `library` cookbook MUST be arranged by its directory tree. In a `library` cookbook the directory tree under the cookbook directory is the arrangement: each directory is a group of components and each ingredient or recipe file is one component, named by its file name. (claim: cf-library-tree-is-arrangement-prior)
- **cf-library-tree-mirrors-code**: The tree SHOULD mirror the arrangement of the code its implementations (in `index.json`) point at. (claim: cf-library-tree-mirrors-code-prior)
- **cf-library-elements-consistent**: `structural-elements` MAY be omitted; when present it MUST NOT contradict the directory tree. (claim: cf-library-elements-consistent-prior)
- **cf-spec-paths-valid**: Every `spec` field in the structure tree MUST reference an existing markdown file (relative to the cookbook directory). (claims: cargo-path-relative-to-manifest, cargo-path-must-point-to-folder, rfc3986-relative-path-reference)
- **relative-paths-stay-inside-the-cookbook**: Every relative path in the manifest (`spec`, a resource's `path`, a context entry's `path`) SHOULD, once its `.` and `..` segments are resolved, point at the exact file it names inside the cookbook directory, never climb out of it. (claims: rfc3986-dot-segments, cargo-path-must-point-to-folder)
- **cf-source-domains**: Every `source.id` field MUST be the UUID of an ingredient or recipe, written `<cookbook-uuid>/<artifact-uuid>` when it is another cookbook's, and MUST resolve in that cookbook's `index.json`. Source provenance ties forked specs back to their cookbook origin. (claim: cf-source-domains-prior)
- **cf-no-circular-deps**: The `depends-on` dot-paths in the structure tree MUST NOT form circular dependencies, direct or indirect. Circular dependencies make build ordering impossible. (claims: dependency-graph-is-a-dag, go-import-cycles-illegal, topological-order-needs-dag)
- **cf-code-roots**: `cookbook.json` MUST NOT carry a `code` block: code roots are tool configuration and live in the repo's `.cookr.json` (`references/cookr-config.schema.json`). (claim: cf-code-roots-prior)
- **cf-code-root-fields**: There, each root MUST name an existing directory (`path`, relative to the repository root) and a `platform` (`macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`), and MAY give a `kind` (`ui` or `logic`), a `group` (the cookbook folder its recipes belong in) and an `ignore` list of globs; top-level `ignore` globs apply to every root. (claim: cf-code-root-fields-prior)
- **cf-code-root-coverage**: Every source file under a root MUST be covered by some artifact's implementations; `cookr coverage` reports the files that are not. (claim: cf-code-root-coverage-prior)
- **semantic-checks-in-code**: A check standard JSON Schema cannot express (comparing one field with another, finding a cycle in `depends-on`, finding that a path or a `source.id` resolves) SHOULD be made in cookr's code on the parsed manifest, beyond schema validation, not through a non-standard keyword such as Ajv's `$data`. (claims: ajv-data-reference, cargo-package-verify-build, graphlib-cycle-error-reports-cycle, jsonschema-defined-over-json)
- **report-every-error**: cookr SHOULD report every validation error in a manifest, not only the first, and SHOULD report a `depends-on` cycle by the nodes on it, the first and the last the same. (claims: python-jsonschema-iter-errors, graphlib-cycle-error-reports-cycle)
- **schema-dialect-2020-12**: `references/cookbook.schema.json` SHOULD declare its dialect in its root with `"$schema": "https://json-schema.org/draft/2020-12/schema"`: its IETF successor is a draft not ready to replace it, though SchemaStore's catalogue still recommends draft-07. (claims: jsonschema-schema-keyword-should-be-used, ietf-jsonschema-draft-not-ready, schemastore-recommends-draft-07)
- **schema-has-stable-absolute-id**: The schema's root SHOULD carry an `$id` that is an absolute URI, and the schema for a new format version SHOULD be published beside the old one rather than over it. (claims: jsonschema-id-absolute-uri, schemastore-version-suffixed-schemas)
- **schema-required-identity**: The schema MUST list `format`, `id` and `rdid` in its top-level `required`. (claims: jsonschema-required-keyword, npm-name-version-unique-identifier)
- **schema-format-const-2**: The schema MUST pin `format` to the integer `2` with `"const": 2`. (claims: jsonschema-const-keyword, android-versioncode-integer)
- **schema-id-uuid-pattern**: The schema SHOULD give `id` a string pattern, anchored with `^` and `$`, that matches the hex-and-dash UUID form: 8, 4, 4, 4 and 12 hex digits joined by hyphens. (claims: rfc9562-hex-and-dash, jsonschema-pattern-not-anchored)
- **schema-source-id-pattern**: The schema SHOULD give `source.id` a string pattern, anchored with `^` and `$`, that matches a hex-and-dash UUID, optionally preceded by another and a slash (`<cookbook-uuid>/<artifact-uuid>`). (claims: rfc9562-hex-and-dash, jsonschema-pattern-not-anchored)
- **schema-rdid-pattern**: The schema MUST give `rdid` a string pattern, anchored with `^` and `$`, that admits only a lowercase letter followed by lowercase letters, digits and hyphens. (claims: npm-name-no-uppercase, cargo-name-characters, jsonschema-pattern-not-anchored)
- **schema-version-pattern**: The schema MUST type `version` as written here: "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$", "description": "Cookbook version (semver)" } (claim: schema-version-pattern-prior)
- **schema-license-spdx**: A manifest's `license` SHOULD name its license in SPDX terms, with the SPDX License List's standard short identifiers, as npm's and Cargo's license fields do. (claims: spdx-short-identifiers, npm-license-spdx-identifier, cargo-license-spdx-expression)
- **schema-date-format**: The schema SHOULD check `created` and `modified` as RFC 3339 full-dates (`YYYY-MM-DD`), the profile of ISO 8601 that JSON Schema's `"format": "date"` names; `"format": "date"` alone asserts nothing while format assertion is off (see `enable-format-assertion`). (claims: jsonschema-date-is-rfc3339-full-date, rfc3339-iso8601-profile, jsonschema-format-assertion-off-by-default)
- **enable-format-assertion**: Every field whose check rests on `format` SHOULD either be validated with format assertion turned on (python-jsonschema with a format checker hooked into its validator and the packages its formats need installed, or Ajv with the ajv-formats plugin, which supplies `uuid`, `date` and `uri-reference`) or carry a `pattern` as well: by default `format` asserts nothing, and python-jsonschema passes a format whose checker package is missing. (claims: jsonschema-format-assertion-off-by-default, python-jsonschema-format-off-by-default, python-jsonschema-format-checker-opt-in, python-jsonschema-format-deps-silent, ajv-formats-not-included, ajv-formats-uuid-rfc4122)
- **schema-closed-objects**: Where the schema closes an object with `"additionalProperties": false` (as it closes the top-level object, `context`, `structural-element`, `source`, `resource` and `context-entry`), it SHOULD be to report a misspelt key rather than ignore it, a choice made for that object and not by reflex. (claims: cargo-warns-unused-keys, schemastore-stricter-checking-for-typos, schemastore-dont-blindly-close)
- **closed-objects-keep-an-extension-point**: The schema MAY leave the manifest an open member for other tools' data, which cookr neither reads nor rejects, as Cargo leaves its `package.metadata` table open, so a property a newer tool adds need not be an error; a closed object meant to be extended through `allOf` MAY be closed with `unevaluatedProperties`, which sees the properties its subschemas declare, where `additionalProperties` sees only those declared beside it. (claims: cargo-metadata-ignored, schemastore-new-properties-should-not-error, additionalproperties-same-subschema, unevaluatedproperties-sees-subschemas)
- **validate-the-schema-strictly**: The schema itself SHOULD be compiled strictly, so an unknown or misspelt keyword in it is an error, as Ajv's strict mode makes it by default, rather than an annotation that constrains nothing, as JSON Schema 2020-12 says unknown keywords should be treated. (claims: ajv-strict-mode-purpose, ajv-unknown-keywords-fail, jsonschema-unknown-keywords-annotations)
- **schema-paths-are-strings**: The schema SHOULD type `spec`, a resource's `path` and a context entry's `path` as strings holding relative-path references (no leading `/`), resolved against the cookbook directory as a manifest's path is resolved against its manifest, and MAY mark them `"format": "uri-reference"`, the format that accepts relative references. (claims: rfc3986-relative-path-reference, cargo-path-relative-to-manifest, jsonschema-uri-reference-format)
- **schema-structure-kind-enum**: "kind": { "type": "string", "enum": [ "app", "library", "plugin", "widget" ], "description": "What the element is. Set on the top-level structure; a library's directory tree is its arrangement and its elements MAY be omitted" } (claim: schema-structure-kind-enum-prior)
- **schema-depends-on-dot-paths**: The schema MUST type `depends-on` as written here: "depends-on": { "type": "array", "items": { "type": "string" }, "description": "Dot-path structural element keys this element depends on" } (claim: schema-depends-on-dot-paths-prior)
- **depends-on-items-unique**: The schema MAY mark each `depends-on` array `"uniqueItems": true`, so a list that names the same element twice fails. (claim: jsonschema-unique-items)
- **schema-has-positive-and-negative-tests**: The schema SHOULD ship with positive test manifests, which must validate, and MAY ship negative ones, which must fail, every one run against the schema with a real validator; the validator itself MAY be checked against the JSON Schema Test Suite. (claims: schemastore-test-files, schemastore-validate-with-ajv, json-schema-test-suite)
- **schema-association-declared**: A `cookbook.json` MAY name its schema with a top-level `$schema` member, which editors such as VS Code use to associate the file with its schema; the other way is VS Code's `json.schemas` setting. (claim: vscode-schema-association)
- **guideline-generated-from-schema**: The schema rules of this guideline MAY be generated from `references/cookbook.schema.json` by a tool that writes documentation from a JSON Schema, as Cloudflare generates its API documentation from the schemas that describe the API. (claims: json-schema-for-humans-generates-docs, cloudflare-docs-from-schema)

## Validating a Manifest

Check a manifest in this order; each step assumes the one before it passed.

1. **Read the bytes.** Refuse a file that begins with the UTF-8 byte order mark (`EF BB BF`), then decode it as UTF-8 (`manifest-is-utf8-without-bom`).
2. **Parse the JSON.** Refuse text that is not JSON (`cf-valid-json`) and an object that repeats a member name (`no-duplicate-member-names`): a parser that keeps the last duplicate hides the first from the schema.
3. **Validate against the schema.** Collect every error, each with the path to the member it is about (`cf-schema-valid`, `report-every-error`). Either turn format assertion on or give each `format` field a `pattern` as well (`enable-format-assertion`).
4. **Run the semantic checks in code** (`semantic-checks-in-code`): each `spec` resolves to an existing markdown file inside the cookbook directory (`cf-spec-paths-valid`, `relative-paths-stay-inside-the-cookbook`); each `source.id` resolves in its cookbook's `index.json` (`cf-source-domains`); `depends-on` has no cycle (`cf-no-circular-deps`).

In Python, with python-jsonschema and the standard library's `graphlib`:

```python
import json
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

from jsonschema import Draft202012Validator


def _unique_members(pairs):
    names = [name for name, _ in pairs]
    repeated = sorted({name for name in names if names.count(name) > 1})
    if repeated:
        raise ValueError(f"duplicate member names: {', '.join(repeated)}")
    return dict(pairs)


def schema_errors(manifest: Path, schema: dict) -> list[str]:
    raw = manifest.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return [f"{manifest}: begins with a byte order mark"]
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_members)
    # One way to keep enable-format-assertion; a `pattern` beside each `format` is the other.
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    return [
        f"{manifest}: /{'/'.join(str(p) for p in error.absolute_path)}: {error.message}"
        for error in validator.iter_errors(data)
    ]


def depends_on_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    """graph maps each element's dot-path to its depends-on list."""
    try:
        tuple(TopologicalSorter(graph).static_order())
    except CycleError as error:
        return error.args[1]  # the cycle's nodes, the first and the last the same
    return None
```

Check the schema itself the same way before any manifest: compile it strictly (`validate-the-schema-strictly`; in Ajv, strict mode is the default) and run it against its positive and negative test manifests (`schema-has-positive-and-negative-tests`).

## Examples

The smallest manifest, a source cookbook's identity and nothing else:

```json
{
  "format": 2,
  "id": "8f14e45f-ceea-4e7a-9e3b-2c1d0a7b6f55",
  "rdid": "adc"
}
```

Versions against `version-is-semver`:

| `version` | Semantic Versioning 2.0.0 |
|---|---|
| `1.2.3` | a normal version |
| `01.2.3` | not a version: a leading zero, which `^\d+\.\d+\.\d+$` still accepts |
| `1.2` | not a version: two numeric parts |

A `depends-on` cycle, reported by its nodes (`report-every-error`): an element `app.ui` that depends on `app.store`, which depends on `app.ui`, gives `['app.ui', 'app.store', 'app.ui']`.

## What a reviewer looks for

- The manifest is read as bytes: a byte order mark is refused, the text decoded as UTF-8, and a repeated member name caught before the schema sees the parsed object.
- The schema declares draft 2020-12 with `$schema`, carries an absolute-URI `$id`, requires `format`, `id` and `rdid`, and pins `format` with `const`.
- Every `pattern` is anchored with `^` and `$`; the UUID patterns match the 8-4-4-4-12 hex-and-dash form; the rdid pattern admits only lowercase letters, digits and hyphens after a leading letter.
- No field relies on `format` alone while the validator runs without format assertion, and no format's checker package is silently missing.
- `version` checks: a semver claim that the `^\d+\.\d+\.\d+$` pattern does not keep (it accepts leading zeroes); a released version whose contents changed without a new `version`.
- Objects closed with `"additionalProperties": false` are closed for typo detection by choice; an object meant to be extended through `allOf`, if closed, is closed with `unevaluatedProperties` rather than `additionalProperties`, or the change says why.
- Checks the schema cannot make (path existence, paths climbing out with `..`, cycles, cross-file `source.id` resolution, one field compared with another) live in cookr's code and report every failure, not the first.
- The project rules hold: `type` is `"cookbook"`, the project fields are present, `structure` has a `description`, `structure.kind` is one of the four values, a library's tree is its arrangement, and code roots and dependencies live in `.cookr.json`, not `cookbook.json`.
- The schema ships with test manifests, run with a real validator, and is compiled strictly.

## A complete review must establish

- Every MUST rule is kept, with no exception: `cf-valid-json`, `manifest-is-utf8-without-bom`, `cf-schema-valid`, `cf-required-identity-fields`, `cf-format-is-integer`, `cf-uuid-format`, `cf-rdid-format`, `cf-type-field`, `cf-required-project-fields`, `cf-dependencies-in-cookr-config`, `cf-semver-fields`, `released-version-is-immutable`, `cf-structure-present`, `cf-structure-kind`, `cf-library-tree-is-arrangement`, `cf-library-elements-consistent`, `cf-spec-paths-valid`, `cf-source-domains`, `cf-no-circular-deps`, `cf-code-roots`, `cf-code-root-fields`, `cf-code-root-coverage`, `schema-required-identity`, `schema-format-const-2`, `schema-rdid-pattern`, `schema-version-pattern`, `schema-depends-on-dot-paths`
- Every SHOULD rule is kept, or the change says why not: `no-duplicate-member-names`, `uuid-compared-not-parsed`, `version-is-semver`, `cf-library-tree-mirrors-code`, `relative-paths-stay-inside-the-cookbook`, `semantic-checks-in-code`, `report-every-error`, `schema-dialect-2020-12`, `schema-has-stable-absolute-id`, `schema-id-uuid-pattern`, `schema-source-id-pattern`, `schema-license-spdx`, `schema-date-format`, `enable-format-assertion`, `schema-closed-objects`, `validate-the-schema-strictly`, `schema-paths-are-strings`, `schema-has-positive-and-negative-tests`
- Every MAY rule that is taken is kept as written: `closed-objects-keep-an-extension-point`, `schema-structure-kind-enum`, `depends-on-items-unique`, `schema-association-declared`, `guideline-generated-from-schema`

A review passes when it establishes every item above.

## A build must establish

- `cf-valid-json`: `cookbook.json` parses as JSON
- `manifest-is-utf8-without-bom`: `cookbook.json` is UTF-8 and does not begin with a byte order mark
- `no-duplicate-member-names`: no object in `cookbook.json` repeats a member name, or the change says why
- `cf-schema-valid`: `cookbook.json` validates against `references/cookbook.schema.json` with a real validator
- `cf-required-identity-fields`: `format` (`2`), `id` and `rdid` are present
- `cf-format-is-integer`: `format` is a whole number, not a semver string
- `cf-uuid-format`: `id` is a valid UUID
- `uuid-compared-not-parsed`: code compares UUIDs without regard to case and does not parse their fields, or says why
- `cf-rdid-format`: `rdid` is one lowercase kebab-case segment
- `cf-type-field`: a project manifest's `type` is `"cookbook"`
- `cf-required-project-fields`: a project manifest has `type`, `name`, `version`, `description`, `author`, `license`, `created`, `modified` and `platforms`
- `cf-dependencies-in-cookr-config`: no linked cookbook is listed in `cookbook.json`; they are `dependencies` in `.cookr.json`
- `cf-semver-fields`: `version` is a semver string matching `^\d+\.\d+\.\d+$`
- `version-is-semver`: every `version` is a Semantic Versioning 2.0.0 version with no leading zeroes, or the change says why
- `released-version-is-immutable`: no released version's contents changed without a new `version`
- `cf-structure-present`: a project manifest has `structure` with a `description`
- `cf-structure-kind`: `structure.kind`, when present, is `app`, `library`, `plugin` or `widget`
- `cf-library-tree-is-arrangement`: a `library` cookbook's directory tree is its arrangement of groups and components
- `cf-library-tree-mirrors-code`: a `library` cookbook's tree mirrors its code's arrangement, or the change says why
- `cf-library-elements-consistent`: a `library` cookbook's `structural-elements`, when present, does not contradict its tree
- `cf-spec-paths-valid`: every `spec` resolves to an existing markdown file relative to the cookbook directory
- `relative-paths-stay-inside-the-cookbook`: no relative path resolves outside the cookbook directory, or the change says why
- `cf-source-domains`: every `source.id` is an ingredient's or recipe's UUID that resolves in its cookbook's `index.json`
- `cf-no-circular-deps`: the `depends-on` graph has no cycle
- `cf-code-roots`: `cookbook.json` has no `code` block
- `cf-code-root-fields`: each root in `.cookr.json` names an existing `path` and a valid `platform`
- `cf-code-root-coverage`: every source file under a root is covered by some artifact's implementations
- `semantic-checks-in-code`: the checks the schema cannot express run in cookr's code, or the change says why
- `report-every-error`: cookr reports every validation error, and a cycle by its nodes, or the change says why
- `schema-dialect-2020-12`: the schema's root declares `"$schema": "https://json-schema.org/draft/2020-12/schema"`, or the change says why
- `schema-has-stable-absolute-id`: the schema's root has an absolute-URI `$id`, and a new format version's schema sits beside the old one, or the change says why
- `schema-required-identity`: the schema's top-level `required` lists `format`, `id` and `rdid`
- `schema-format-const-2`: the schema pins `format` with `"const": 2`
- `schema-id-uuid-pattern`: `id` has an anchored hex-and-dash UUID pattern, or the change says why
- `schema-source-id-pattern`: `source.id` has an anchored pattern for a UUID, optionally after a cookbook UUID and a slash, or the change says why
- `schema-rdid-pattern`: `rdid` has an anchored pattern admitting only a lowercase letter, then lowercase letters, digits and hyphens
- `schema-version-pattern`: `version` is typed as the rule writes it
- `schema-license-spdx`: `license` uses SPDX short identifiers, or the change says why
- `schema-date-format`: `created` and `modified` are checked as RFC 3339 full-dates, or the change says why
- `enable-format-assertion`: no field relies on `format` alone without format assertion on, or the change says why
- `schema-closed-objects`: each object closed with `"additionalProperties": false` is closed to catch misspelt keys by choice, or the change says why
- `closed-objects-keep-an-extension-point`: an extension point, when added, is open for other tools, and a closed object extended through `allOf`, when closed with `unevaluatedProperties`, sees its subschemas' properties
- `validate-the-schema-strictly`: the schema compiles under strict checking, or the change says why
- `schema-paths-are-strings`: `spec` and each `path` are strings holding relative-path references, or the change says why
- `schema-structure-kind-enum`: `kind` is typed as the rule writes it
- `schema-depends-on-dot-paths`: `depends-on` is typed as the rule writes it
- `depends-on-items-unique`: `depends-on`, when marked, carries `"uniqueItems": true`
- `schema-has-positive-and-negative-tests`: the schema has positive test manifests, run with a real validator, or the change says why
- `schema-association-declared`: a `$schema` member, when present, names the cookbook schema
- `guideline-generated-from-schema`: generated schema rules, when generated, come from `references/cookbook.schema.json`

## Rationale

A cookbook that fails JSON parsing cannot be processed by any tooling, and JSON Schema is defined over JSON documents, so parsing comes first. JSON exchanged between systems outside a closed ecosystem must be UTF-8 with no byte order mark; a shared cookbook leaves the repository it was written in, so it is not a closed ecosystem.

Schema validation catches structural errors (missing fields, wrong types, unknown properties) before any semantic checks run. It cannot make every check: standard JSON Schema has no way to compare one field with another, to look at the file system, or to read another file, so those checks run in code, as Cargo's packaging step checks a package by building it, beyond parsing its manifest. A validator that stops at the first error makes the author fix a manifest one error at a time; python-jsonschema yields every error, and graphlib names the cycle it finds.

`format` is an annotation unless the validator asserts it: the 2020-12 format-annotation vocabulary requires format evaluation to be off by default, python-jsonschema checks formats only with a format checker hooked in, and Ajv ships without the specification's formats. A schema that relies on `"format": "date"` with assertion off checks nothing. JSON Schema 2020-12 says unknown keywords should be treated as annotations, so a misspelt keyword in the schema constrains nothing unless the schema is compiled strictly.

Closed objects catch misspelt keys, which is why Cargo warns on unused keys; SchemaStore's maintainers warn against closing objects by reflex, because a property a newer tool adds then becomes an error. Cargo keeps an ignored `package.metadata` table for other tools. `additionalProperties` sees only the properties declared beside it, so a closed object cannot be extended through `allOf`; `unevaluatedProperties` can.

RFC 9562 obsoletes RFC 4122 and represents a UUID as the hex-and-dash string, in upper, lower or mixed case, and recommends treating UUIDs as opaquely as possible. Semantic Versioning 2.0.0 forbids leading zeroes, which `^\d+\.\d+\.\d+$` accepts, and allows pre-release and build suffixes, which it rejects. A released version's contents must not change. Broken spec paths mean the agent cannot find the spec to implement, and a path's `..` segments can carry it outside the cookbook unless it is checked. Circular dependencies make build ordering impossible: a complete build order exists only for a graph without cycles.

The `type` value, the project fields, `structure`, the `kind` values, the library layout, source provenance and code roots are this cookbook's own design; no outside source requires them, and npm, for one, requires only `name` and `version`, and only of a package it publishes.

## References

- [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259.html)
- [JSON Schema 2020-12 Core](https://json-schema.org/draft/2020-12/json-schema-core) and [Validation](https://json-schema.org/draft/2020-12/json-schema-validation)
- [The IETF JSON Schema draft](https://www.ietf.org/archive/id/draft-ietf-jsonschema-json-schema-04.html)
- [Understanding JSON Schema: object](https://json-schema.org/understanding-json-schema/reference/object)
- [RFC 9562: Universally Unique IDentifiers (UUIDs)](https://www.rfc-editor.org/rfc/rfc9562.html) and [RFC 4122](https://www.rfc-editor.org/rfc/rfc4122.html)
- [RFC 3986: URI Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986.html)
- [RFC 3339: Date and Time on the Internet](https://www.rfc-editor.org/rfc/rfc3339.html)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [SPDX License List](https://spdx.org/licenses/)
- [python-jsonschema: Schema Validation](https://python-jsonschema.readthedocs.io/en/stable/validate/)
- [Ajv: formats](https://ajv.js.org/guide/formats.html), [strict mode](https://ajv.js.org/strict-mode.html) and [combining schemas](https://ajv.js.org/guide/combining-schemas.html)
- [npm: package.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json)
- [Cargo: the manifest format](https://doc.rust-lang.org/cargo/reference/manifest.html), [specifying dependencies](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html) and [cargo package](https://doc.rust-lang.org/cargo/commands/cargo-package.html)
- [Bazel: Dependencies](https://bazel.build/concepts/dependencies)
- [The Go Programming Language Specification](https://go.dev/ref/spec)
- [Python graphlib](https://docs.python.org/3/library/graphlib.html)
- [Android: Version your app](https://developer.android.com/studio/publish/versioning)
- [Swift Package Manager: PackageDescription](https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html)
- [VS Code: JSON](https://code.visualstudio.com/docs/languages/json)
- [SchemaStore: CONTRIBUTING](https://github.com/SchemaStore/schemastore/blob/master/CONTRIBUTING.md)
- [JSON Schema Test Suite](https://github.com/json-schema-org/JSON-Schema-Test-Suite)
- [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans)
- [Cloudflare: Cloudflare's JSON-powered documentation generator](https://blog.cloudflare.com/cloudflares-json-powered-documentation-generator/)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-21 | Mike Fullerton | Initial creation, written from research |
