# Research fallback run: cookbook-formatting

`team_probe.py researchteam`: `ok: false`, "missing distributions: PyYAML, aiohttp, mcp, websockets". One fresh Opus Agent (`general-purpose`) ran the `research` prompt as `write_brief.py prompt research` printed it. Its reply, verbatim:

---

I wrote both research files, but the validate line you gave doesn't print `Research passed.` It stops before checking anything:

```
✗ .../cookbook/guidelines/cookbook/authoring/cookbook-formatting: not an artifact source folder (no artifact.json)
```

`cookr validate --research` (the `research_only` function in `cookr/core/research.py`) refuses any folder that has no `artifact.json`. The brief says this folder holds only `research/` until stage 3, and I was told to write no other files, so I didn't add one. Instead I ran cookr's own research checker (`_findings`) on the folder in memory, with a stand-in artifact that has no rules, and wrote nothing. It reported no problems. For the real line to pass, the folder needs an `artifact.json` from stage 3, or the validator needs to accept a folder that holds only research. The sibling `requirement-keywords` and `guideline-formatting` folders have no `artifact.json` either, so the same refusal should apply to them.

**Files**
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/cookbook-formatting/research/research.json`
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/cookbook-formatting/research/research.md`

**Claims per question (93 total)**

| Question | Claims |
|---|---|
| best-practices | 25 (14 are `-prior` claims) |
| known-solutions | 21 |
| platform-guidelines | 40 (3 are `-prior` claims) |
| experts-view | 7 |

**Verdicts**
- cf-valid-json: supported. jsonschema-defined-over-json, rfc8259-parser-accepts-grammar
- cf-schema-valid: supported. jsonschema-defined-over-json, python-jsonschema-iter-errors, schemastore-validate-with-ajv, cargo-version-three-numeric-parts
- cf-type-field: unsupported. cf-type-field-prior, jsonschema-const-keyword
- cf-required-identity-fields: supported. jsonschema-required-keyword, npm-name-version-unique-identifier
- cf-required-project-fields: unsupported. cf-required-project-fields-prior, npm-name-version-required-to-publish
- cf-dependencies-in-cookr-config: unsupported. cf-dependencies-in-cookr-config-prior
- cf-uuid-format: contradicted. cf-uuid-format-prior, rfc9562-obsoletes-rfc4122, rfc9562-hex-and-dash, rfc9562-treat-uuids-opaquely
- cf-rdid-format: supported. npm-name-no-uppercase, cargo-name-characters
- cf-semver-fields: contradicted. cf-semver-fields-prior, semver-normal-version-form, semver-no-leading-zeroes, semver-prerelease-allowed, semver-build-metadata-allowed, semver-suggested-regex, npm-version-node-semver
- cf-format-is-integer: supported. jsonschema-const-keyword, android-versioncode-integer
- cf-structure-present: unsupported. cf-structure-present-prior
- cf-spec-paths-valid: supported. cargo-path-relative-to-manifest, cargo-path-must-point-to-folder, rfc3986-relative-path-reference
- cf-source-domains: unsupported. cf-source-domains-prior, rfc9562-hex-and-dash
- cf-structure-kind: unsupported. cf-structure-kind-prior, jsonschema-enum-keyword
- cf-library-tree-is-arrangement: unsupported. cf-library-tree-is-arrangement-prior
- cf-library-tree-mirrors-code: unsupported. cf-library-tree-mirrors-code-prior
- cf-library-elements-consistent: unsupported. cf-library-elements-consistent-prior
- cf-code-roots: unsupported. cf-code-roots-prior
- cf-code-root-fields: unsupported. cf-code-root-fields-prior
- cf-code-root-coverage: unsupported. cf-code-root-coverage-prior
- cf-no-circular-deps: supported. dependency-graph-is-a-dag, go-import-cycles-illegal, topological-order-needs-dag
- schema-dialect-2020-12: supported. jsonschema-schema-keyword-should-be-used, ietf-jsonschema-draft-not-ready, schemastore-recommends-draft-07
- schema-required-identity: supported. jsonschema-required-keyword, npm-name-version-unique-identifier
- schema-format-const-2: supported. jsonschema-const-keyword, android-versioncode-integer
- schema-id-uuid-pattern: supported. rfc9562-hex-and-dash, rfc9562-mixed-case, jsonschema-pattern-not-anchored
- schema-rdid-pattern: supported. npm-name-no-uppercase, cargo-name-characters, jsonschema-pattern-not-anchored
- schema-version-pattern: contradicted. schema-version-pattern-prior, semver-no-leading-zeroes, semver-prerelease-allowed, semver-build-metadata-allowed, semver-suggested-regex
- schema-license-spdx: supported. spdx-short-identifiers, npm-license-spdx-identifier, cargo-license-spdx-expression
- schema-date-format: supported. jsonschema-date-is-rfc3339-full-date, rfc3339-iso8601-profile, jsonschema-format-assertion-off-by-default
- schema-closed-objects: supported. cargo-warns-unused-keys, schemastore-stricter-checking-for-typos, jsonschema-unknown-keywords-annotations, schemastore-dont-blindly-close
- schema-source-id-pattern: supported. rfc9562-hex-and-dash, rfc9562-mixed-case
- schema-structure-kind-enum: unsupported. schema-structure-kind-enum-prior, jsonschema-enum-keyword
- schema-paths-are-strings: supported. rfc3986-relative-path-reference, cargo-path-relative-to-manifest, jsonschema-uri-reference-format
- schema-depends-on-dot-paths: unsupported. schema-depends-on-dot-paths-prior
- enable-format-assertion: new (SHOULD). jsonschema-format-assertion-off-by-default, python-jsonschema-format-off-by-default, python-jsonschema-format-checker-opt-in, python-jsonschema-format-deps-silent, ajv-formats-not-included, ajv-formats-uuid-rfc4122
- semantic-checks-in-code: new (SHOULD). ajv-data-reference, cargo-package-verify-build, graphlib-cycle-error-reports-cycle, jsonschema-defined-over-json
- report-every-error-with-its-location: new (SHOULD). python-jsonschema-iter-errors, graphlib-cycle-error-reports-cycle
- schema-has-stable-absolute-id: new (SHOULD). jsonschema-id-absolute-uri, schemastore-version-suffixed-schemas
- no-duplicate-member-names: new (SHOULD). rfc8259-names-should-be-unique, rfc8259-duplicate-names-unpredictable
- manifest-is-utf8-without-bom: new (MUST). rfc8259-utf8-exchange, rfc8259-no-bom
- depends-on-items-unique: new (MAY). jsonschema-unique-items
- released-version-is-immutable: new (MUST). semver-released-version-immutable
- schema-has-positive-and-negative-tests: new (SHOULD). schemastore-test-files, schemastore-validate-with-ajv, json-schema-test-suite
- validate-the-schema-strictly: new (SHOULD). ajv-strict-mode-purpose, ajv-unknown-keywords-fail, jsonschema-unknown-keywords-annotations
- closed-objects-keep-an-extension-point: new (MAY). cargo-metadata-ignored, schemastore-new-properties-should-not-error, additionalproperties-same-subschema, unevaluatedproperties-sees-subschemas
- guideline-generated-from-schema: new (MAY). json-schema-for-humans-generates-docs, cloudflare-docs-from-schema
- uuid-compared-not-parsed: new (SHOULD). rfc9562-treat-uuids-opaquely, rfc4122-lowercase-output, rfc9562-mixed-case
- relative-paths-stay-inside-the-cookbook: new (SHOULD). rfc3986-dot-segments, cargo-path-must-point-to-folder
- version-is-full-semver: new (SHOULD). semver-suggested-regex, swiftpm-version-semver, android-semver-good-basis, npm-version-node-semver
- schema-association-declared: new (MAY). vscode-schema-association

The strengths for the new verdicts are given in `research.md`. The verdict entries in `research.json` don't carry a strength field. I didn't commit anything, since the task said to write exactly two files and edit nothing else.

---

## Orchestrator corrections (steps 3 and 4)

- `open_questions` and research.md (*Platform guidelines*, Microsoft / web tooling) said the closed top-level object forbids an in-file `$schema`. The schema at the base commit lists `$schema` under `properties` ("Optional JSON Schema reference for editor support"), so both now say it is already permitted.
