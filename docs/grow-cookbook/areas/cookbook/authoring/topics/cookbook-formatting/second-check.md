## rfc9562-obsoletes-rfc4122
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The abstract of RFC 9562 says it obsoletes RFC 4122.

## rfc9562-hex-and-dash
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Section 4 says that in URNs or as text, a UUID "should be represented by the 'hex-and-dash' string format". Its ABNF gives 4-2-2-2-6 hex octets, which is 8-4-4-4-12 hex digits.

## rfc9562-treat-uuids-opaquely
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: Section 6.12 recommends avoiding parsing "unless absolutely necessary" and allows that application concerns "could ... require some degree of introspection". The claim's "never parsed" is stronger than that guidance, and the claim's application to manifests is its own.
- correction: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST

## semver-normal-version-form
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Item 2 of SemVer 2.0.0 says this word for word, at MUST strength.

## semver-no-leading-zeroes
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source says X, Y and Z "MUST NOT contain leading zeroes". The claim's point that `^\d+\.\d+\.\d+$` accepts 01.2.3 is a true fact about that regex.

## semver-prerelease-allowed
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Item 9 holds the quote at MAY strength. The regex claim is a fact about the pattern.

## semver-build-metadata-allowed
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Item 10 holds the quote at MAY strength.

## semver-suggested-regex
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The FAQ gives a numbered-group regex "compatible with ECMA Script (JavaScript), PCRE ..., Python and Go". Its core `(0|[1-9]\d*)` excludes leading zeroes.

## npm-version-node-semver
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The full sentence is "Version must be parseable by node-semver, which is bundled with npm as a dependency." The same page says version is optional if you don't publish.

## jsonschema-format-assertion-off-by-default
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Section 7.2.1 (Format-Annotation vocabulary) says implementations MAY assert format, but such evaluation "MUST be disabled by default".

## python-jsonschema-format-off-by-default
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The "Validating Formats" section says this word for word.

## python-jsonschema-format-checker-opt-in
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The next sentence in the source says the same, followed by a `format_checker=` example.

## python-jsonschema-format-deps-silent
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The warning reads "If a dependency is not installed when using a checker that requires it, validation will succeed without throwing an error".

## ajv-formats-not-included
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source continues "these and several other formats are provided by ajv-formats plugin."

## ajv-formats-uuid-rfc4122
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The same list has "date: full-date according to RFC3339" and "uri-reference: URI reference, including full and relative URIs".

## ajv-data-reference
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The "$data reference" section holds the quote, says "See proposal for more information", and presents it as an Ajv option.

## cargo-package-verify-build
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The package step extracts the .crate and builds it to verify it. The source notes `--no-verify` skips this step.

## graphlib-cycle-error-reports-cycle
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The cycle's nodes are in `args[1]` of the CycleError, with the first and last node the same. Only one cycle is reported if there are several.

## jsonschema-defined-over-json
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The very next sentence says "any document or memory structure that can be parsed into ... the JSON Schema data model can be interpreted against a JSON Schema, including media types like CBOR". So "validates only JSON documents" overstates the source.
- correction: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST

## python-jsonschema-iter-errors
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The docstring of `iter_errors` matches, and its example prints two errors for one instance.

## jsonschema-id-absolute-uri
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source uses SHOULD and the claim keeps SHOULD.

## schemastore-version-suffixed-schemas
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote is SchemaStore's how-to for "a JSON Schema with multiple versions" (e.g. agripparc-1.2/1.3/1.4). It does not say that every change to a format must be published under a new name rather than overwritten, and it is not a general rule beyond SchemaStore.
- correction: refuted (quote-found yes, supports-claim partly); trust 62 -> 42; a rule citing it cannot carry MUST

## rfc8259-names-should-be-unique
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Section 4 says this at SHOULD strength.

## rfc8259-duplicate-names-unpredictable
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source goes on to say many implementations report only the last pair, and others error or report all pairs. That backs the claim that a validator sees what its parser kept, though the RFC does not name schema validators.

## rfc8259-utf8-exchange
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Section 8.1 says this at MUST strength.

## rfc8259-no-bom
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Section 8.1 says this at MUST NOT strength. Parsers MAY ignore a BOM.

## jsonschema-unique-items
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The uniqueItems definition in 2020-12 Validation matches. The depends-on example is the claim's own.

## semver-released-version-immutable
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Item 3 follows with "Any modifications MUST be released as a new version."

## schemastore-test-files
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Positive tests are "optional, but _strongly_ recommended" and negative tests are "(optional)", which matches the claim's should/may.

## schemastore-validate-with-ajv
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: CONTRIBUTING.md says "All schemas must" validate against their tests using Ajv.

## json-schema-test-suite
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The opening of the README matches.

## ajv-strict-mode-purpose
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The strict-mode page holds this word for word.

## ajv-unknown-keywords-fail
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The strict-mode page holds this word for word.

## jsonschema-unknown-keywords-annotations
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: Core 2020-12 says unknown keywords "SHOULD be treated as annotations". The claim says flatly that an unknown keyword "is an annotation, not an error", which is stronger than SHOULD; Ajv's strict mode, for example, rejects unknown keywords.
- correction: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST

## cargo-metadata-ignored
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The same page says "There is a similar table at the workspace level at workspace.metadata". So package.metadata is not Cargo's one open table.
- correction: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST

## schemastore-new-properties-should-not-error
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote sits under "Do not blindly add `additionalProperties: false`". The same section says stricter checks belong in validator options.

## additionalproperties-same-subschema
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page says additionalProperties "can restrict you from 'extending' a schema using ... allOf". It presents unevaluatedProperties as the fix, labelled "New in draft 2019-09", so it is present in 2020-12 rather than new there.

## unevaluatedproperties-sees-subschemas
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The "Unevaluated Properties" section holds this word for word.

## json-schema-for-humans-generates-docs
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The README tagline matches (no trailing period in the source) and lists HTML and Markdown output.

## cloudflare-docs-from-schema
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The schemas are the JSON Hyper-Schema that describes Cloudflare's endpoints, and they generate the HTML docs at api.cloudflare.com. The post is from 2016.

## rfc4122-lowercase-output
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Section 3 says this in its definition of the string representation. It is plain specification text, not a BCP 14 MUST.

## rfc9562-mixed-case
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence continues "Section 2.3 of [RFC5234]". ABNF HEXDIG is case-insensitive.

## rfc3986-dot-segments
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Section 5.2.4 holds the quote. The claim's point that a resolved path can leave its base directory is an inference; it holds because remove_dot_segments clamps only at the root.

## cargo-path-must-point-to-folder
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source adds "unlike with git dependencies, cargo does not traverse local paths."

## swiftpm-version-semver
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The `Version` struct docs say this. Elsewhere the page says "The version rule requires Swift packages to conform to semantic versioning."

## android-semver-good-basis
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence before it is "Versioning requirements vary between different projects", so the guidance does not mandate SemVer.

## vscode-schema-association
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence continues "or in the User or Workspace settings ... under the property json.schemas". The page adds that extensions can also map schemas.
