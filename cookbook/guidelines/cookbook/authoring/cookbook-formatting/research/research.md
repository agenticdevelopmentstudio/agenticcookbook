# cookbook-formatting research

Researched 2026-11-21 against base commit `071e52f9572bf4b7c534cfcf95fb111282abc423`. The claims, citations and verdicts are in `research.json`; each finding below names its claim id. Keyword case and lint severity belong to the sibling topic requirement-keywords and are not decided here.

## Best practices

- **A dependency graph must be acyclic.** Bazel describes the depends-upon relation as a DAG over targets (`dependency-graph-is-a-dag`). Go makes a direct or indirect self-import illegal (`go-import-cycles-illegal`). A complete build order exists only when the graph has no directed cycles (`topological-order-needs-dag`). Together these support cf-no-circular-deps at MUST strength.
- **Paths in a manifest are relative to the manifest and must point at the exact folder.** Cargo resolves a path relative to the `Cargo.toml` it is written in (`cargo-path-relative-to-manifest`) and requires it to point at the exact folder (`cargo-path-must-point-to-folder`). This supports cf-spec-paths-valid.
- **Name and version identify a package, and only they are required.** npm treats name plus version as the unique identifier (`npm-name-version-unique-identifier`). It requires only those two fields, and only to publish (`npm-name-version-required-to-publish`). That supports cf-required-identity-fields. It does not support cf-required-project-fields, whose nine required fields are the owner's choice (`cf-required-project-fields-prior`). The sources support SHOULD at most for the extra fields: description, author and license.
- **A released version is immutable.** Semantic Versioning forbids changing a released version's contents (`semver-released-version-immutable`). This gives a new MUST-strength rule, released-version-is-immutable.
- **A schema ships with tests.** SchemaStore asks for positive test files and accepts negative ones (`schemastore-test-files`). Every schema must validate them with a real validator (`schemastore-validate-with-ajv`). This gives a new SHOULD-strength rule, schema-has-positive-and-negative-tests.
- **Versioned schemas sit side by side.** SchemaStore suffixes schema names with the version (`schemastore-version-suffixed-schemas`). With the core spec's absolute `$id` (`jsonschema-id-absolute-uri`), this gives a new SHOULD-strength rule, schema-has-stable-absolute-id.
- **Project-design rules have no outside source.** The following are this cookbook's own design and are recorded as unsupported. No outside source requires them or argues against them.
  - The `type` discriminator (`cf-type-field-prior`).
  - Dependencies living in `.cookr.json` (`cf-dependencies-in-cookr-config-prior`).
  - A required `structure` with a description (`cf-structure-present-prior`).
  - `source.id` resolving in another cookbook's `index.json` (`cf-source-domains-prior`).
  - The four `structure.kind` values (`cf-structure-kind-prior`).
  - The library directory tree as arrangement (`cf-library-tree-is-arrangement-prior`), the tree mirroring the code (`cf-library-tree-mirrors-code-prior`), and elements agreeing with the tree (`cf-library-elements-consistent-prior`).
  - Code roots kept out of `cookbook.json` (`cf-code-roots-prior`), their fields (`cf-code-root-fields-prior`), and full coverage of the files under a root (`cf-code-root-coverage-prior`).
  - The `kind` enum in the schema (`schema-structure-kind-enum-prior`).
  - `depends-on` holding dot-paths (`schema-depends-on-dot-paths-prior`).

  The sources do support the mechanisms these rules use. A fixed value is expressed with `const` (`jsonschema-const-keyword`) and a closed list with `enum` (`jsonschema-enum-keyword`). The sources do not support the particular values chosen.

## Known solutions

- **Format checking is off unless enabled.** In python-jsonschema, the validator cookr uses, format is not asserted by default (`python-jsonschema-format-off-by-default`). It is asserted only when a format checker is hooked in (`python-jsonschema-format-checker-opt-in`). Even then, a format whose extra package is missing passes silently (`python-jsonschema-format-deps-silent`). Ajv ships without the spec's formats (`ajv-formats-not-included`), and its ajv-formats plugin supplies `uuid`, `date` and `uri-reference` (`ajv-formats-uuid-rfc4122`). This gives a new SHOULD-strength rule, enable-format-assertion. Either the validator runs with a format checker, or the field also carries a `pattern`. Without one of those, schema-date-format's `format: date` checks nothing.
- **Report every error.** python-jsonschema can yield every error, not only the first (`python-jsonschema-iter-errors`). graphlib's `CycleError` names the cycle it found (`graphlib-cycle-error-reports-cycle`). This gives a new SHOULD-strength rule, report-every-error-with-its-location.
- **Semantic checks run in code.** Standard JSON Schema cannot compare one field with another; Ajv needs its non-standard `$data` option for that (`ajv-data-reference`). Cargo checks a package by building it from a pristine state (`cargo-package-verify-build`). Schema validation applies only to a document already parsed as JSON (`jsonschema-defined-over-json`). This gives a new SHOULD-strength rule, semantic-checks-in-code. Path existence, cycles, cross-file resolution and created ≤ modified are checked by cookr, not by the schema.
- **Package managers check versions with a semver parser.** Cargo requires three numeric parts (`cargo-version-three-numeric-parts`). npm requires the version to parse with node-semver (`npm-version-node-semver`).
- **Name rules.** npm forbids uppercase letters in new names (`npm-name-no-uppercase`). Cargo allows only alphanumerics, `-` and `_` (`cargo-name-characters`). These support cf-rdid-format and schema-rdid-pattern by analogy. The schema's `^[a-z][a-z0-9-]*$` accepts trailing and doubled hyphens, so it is looser than "kebab-case" (see open questions).
- **Licenses are SPDX.** npm advises an SPDX identifier (`npm-license-spdx-identifier`). crates.io reads an SPDX 2.3 expression (`cargo-license-spdx-expression`).
- **Unknown keys.** Cargo warns on unused keys to catch typos (`cargo-warns-unused-keys`). It also leaves one table, `package.metadata`, open for other tools (`cargo-metadata-ignored`). This supports schema-closed-objects. It also gives a new MAY-strength rule, closed-objects-keep-an-extension-point.
- **Schemas are checked strictly.** Ajv's strict mode exists to catch silently ignored mistakes in schemas (`ajv-strict-mode-purpose`). It refuses unknown keywords by default (`ajv-unknown-keywords-fail`). This gives a new SHOULD-strength rule, validate-the-schema-strictly.
- **Test suites and doc generators exist.** The JSON Schema organisation keeps a shared test suite for validators (`json-schema-test-suite`). json-schema-for-humans generates HTML or Markdown documentation from a schema (`json-schema-for-humans-generates-docs`).

## Platform guidelines

- **JSON (RFC 8259).**
  - Valid JSON is defined by the grammar every parser must accept (`rfc8259-parser-accepts-grammar`). With `jsonschema-defined-over-json`, this supports cf-valid-json.
  - Object names SHOULD be unique (`rfc8259-names-should-be-unique`), because software reads duplicates unpredictably (`rfc8259-duplicate-names-unpredictable`). This gives a new SHOULD-strength rule, no-duplicate-member-names.
  - JSON exchanged outside a closed ecosystem MUST be UTF-8 (`rfc8259-utf8-exchange`), with no byte order mark (`rfc8259-no-bom`). This gives a new MUST-strength rule, manifest-is-utf8-without-bom. A shared cookbook leaves the authoring repo, so it is not a closed ecosystem.
- **JSON Schema 2020-12.**
  - `$schema` SHOULD declare the dialect (`jsonschema-schema-keyword-should-be-used`). The IETF successor says it is not ready to replace 2020-12 (`ietf-jsonschema-draft-not-ready`). Together these support schema-dialect-2020-12. SchemaStore still recommends draft-07 for its catalogue (`schemastore-recommends-draft-07`), but that is a catalogue convention, not a ruling against 2020-12.
  - The root SHOULD carry an absolute-URI `$id` (`jsonschema-id-absolute-uri`).
  - `required` (`jsonschema-required-keyword`) supports cf-required-identity-fields and schema-required-identity.
  - `const` (`jsonschema-const-keyword`) supports cf-format-is-integer and schema-format-const-2.
  - `pattern` is not implicitly anchored (`jsonschema-pattern-not-anchored`), so every whole-value pattern needs `^…$`. The schema's patterns are anchored.
  - Unknown keywords are annotations (`jsonschema-unknown-keywords-annotations`), so a misspelt keyword constrains nothing.
  - Format evaluation MUST be off by default (`jsonschema-format-assertion-off-by-default`). `date` is RFC 3339's full-date (`jsonschema-date-is-rfc3339-full-date`), and RFC 3339 is a profile of ISO 8601 (`rfc3339-iso8601-profile`). This supports schema-date-format, but only once format is asserted.
  - The spec defines `uuid` (`jsonschema-uuid-format-rfc4122`) and `uri-reference` (`jsonschema-uri-reference-format`) formats. The latter, with RFC 3986's relative-path reference (`rfc3986-relative-path-reference`), supports schema-paths-are-strings.
  - `uniqueItems` (`jsonschema-unique-items`) gives a new MAY-strength rule, depends-on-items-unique.
- **UUIDs (RFC 9562).**
  - RFC 9562 obsoletes RFC 4122 (`rfc9562-obsoletes-rfc4122`), so cf-uuid-format's citation of RFC 4122 is contradicted (`cf-uuid-format-prior`). Its substance, that `id` is a UUID in hex-and-dash form (`rfc9562-hex-and-dash`), stands under RFC 9562.
  - Letters may be upper, lower or mixed case (`rfc9562-mixed-case`), which supports schema-id-uuid-pattern and schema-source-id-pattern as written. The obsoleted RFC 4122 required lowercase output (`rfc4122-lowercase-output`).
  - UUIDs should be treated opaquely (`rfc9562-treat-uuids-opaquely`). This gives a new SHOULD-strength rule, uuid-compared-not-parsed.
- **Semantic Versioning 2.0.0.**
  - A normal version is X.Y.Z of non-negative integers (`semver-normal-version-form`) with no leading zeroes (`semver-no-leading-zeroes`). It may carry a pre-release suffix (`semver-prerelease-allowed`) and build metadata (`semver-build-metadata-allowed`). semver.org's suggested regex excludes leading zeroes (`semver-suggested-regex`).
  - `^\d+\.\d+\.\d+$` accepts `01.2.3` and rejects `1.0.0-rc.1` and `1.0.0+build`. So cf-semver-fields (`cf-semver-fields-prior`) and schema-version-pattern (`schema-version-pattern-prior`) are contradicted: the sources support the field being semver, and they reject this pattern as a semver check.
  - Apple's SwiftPM requires versions to conform to semver (`swiftpm-version-semver`). Android points at semver as a good basis (`android-semver-good-basis`). npm parses with node-semver (`npm-version-node-semver`). Together these give a new SHOULD-strength rule, version-is-full-semver. Whether to accept pre-release suffixes is an open question.
- **Android.** versionCode is a positive integer that programs compare, kept apart from the user-visible string (`android-versioncode-integer`). This is an analogue for the integer `format` beside a semver `version`.
- **Paths (RFC 3986).** Dot segments are resolved when a path is (`rfc3986-dot-segments`). With `cargo-path-must-point-to-folder`, this gives a new SHOULD-strength rule, relative-paths-stay-inside-the-cookbook.
- **SPDX.** The SPDX list gives standard short identifiers (`spdx-short-identifiers`). This supports schema-license-spdx.
- **Microsoft / web tooling.** VS Code associates a file with its schema through an in-file `$schema` or the `json.schemas` setting (`vscode-schema-association`). This gives a new MAY-strength rule, schema-association-declared. The schema at the base commit already permits an optional top-level `$schema` string, so the in-file form is allowed today.

## The expert's view

- **Close objects deliberately, not by reflex.** SchemaStore's maintainers say not to add `additionalProperties: false` blindly (`schemastore-dont-blindly-close`). A property added by a newer tool version should not error (`schemastore-new-properties-should-not-error`). Stricter checking is still accepted when the goal is catching typos (`schemastore-stricter-checking-for-typos`). For a first-party manifest whose schema ships with its tool, catching typos is the main gain, which supports schema-closed-objects. The expert would add an extension point (`cargo-metadata-ignored`) and a forward-compatibility story.
- **What people get wrong about closed objects.** `additionalProperties` sees only the properties declared beside it (`additionalproperties-same-subschema`), so a closed object cannot be extended through `allOf`. `unevaluatedProperties` is the 2020-12 keyword that can (`unevaluatedproperties-sees-subschemas`).
- **What people get wrong about format.** People assume `format: date` or `format: uuid` validates. By default it does not (`jsonschema-format-assertion-off-by-default`, `python-jsonschema-format-off-by-default`).
- **What people get wrong about semver.** People write `\d+\.\d+\.\d+` and call it semver. It is not (`semver-no-leading-zeroes`, `semver-suggested-regex`).
- **What people get wrong about schema typos.** People assume a misspelt schema keyword is an error. It is silently ignored (`jsonschema-unknown-keywords-annotations`) unless the schema is compiled strictly (`ajv-unknown-keywords-fail`).
- **Keep prose and schema in one place.** Cloudflare generated its complete API documentation from the same schemas that describe the API (`cloudflare-docs-from-schema`), and tools exist for it (`json-schema-for-humans-generates-docs`). This gives a new MAY-strength rule, guideline-generated-from-schema, so the schema-* rules and the guideline cannot drift. The support is secondary and dated.
