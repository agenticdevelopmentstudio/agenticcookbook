# Write brief: cookbook-formatting

Today is 2026-11-21.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/cookbook-formatting (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/cookbook-formatting/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/cookbook-formatting/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/cookbook-formatting/owner-list.md.
cookr, this checkout's own (never an installed one): PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook <command>

Review criteria. Stage 4 reviews against exactly these, and the author writes to them:

1. Every guideline in /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/recipe-quality/:
   behavioral-requirements, completeness, cookbook-compliance,
   cross-recipe-consistency, source-fidelity and template-conformance.
2. Source fidelity means fidelity to the research:
   - every rule follows from the claims it cites, at the strength it states;
   - no claim with a `supported` or `new` verdict is left without a rule;
   - every rule ends with its citation, and every cited claim exists.
3. The strength rule: each rule is at the strength of the weakest claim it
   cites. A claim the second check refuted (listed under "Second-check
   corrections, refuted" in the write brief; its `trust.basis` says "Second
   check … refuted") cannot carry MUST. A claim that only lost a citation
   whose source lacked the quote (listed under "citation dropped") is still
   supported, and its strength is unchanged.
4. A rule's citations are authoritative. A verdict's `claims` list is stage
   2's record of the old rule: nobody compares it with the rule's citations,
   and research is not edited after stage 2. A rule may cite any claim of
   research.json that some verdict names. Prior rule names (the names the
   verdicts key on) are fixed; new rules may be named and renamed freely.
5. The owner list (owner-list.md): a prior rule listed there keeps its prior
   text word for word, citing `<rule>-prior`. Only its wording is exempt from
   review, nothing else. Where the prior text has no RFC keyword, one lead-in
   in front of it carries the keyword the old text implied ("In TypeScript,
   the panel MUST be reached this way:"); owner-list.md lists the lead-in, and
   it is the one change accepted. An open question listed there is the
   owner's: the text does not settle it, and it is never a finding.
6. Frontmatter: the author updates `summary` (160 characters or fewer,
   describing the new text), `tags`, `platforms` and `related` to match the
   new guideline. `version`, `modified` and Change History are left for stage
   5's `cookr bump`: a stale version, modified date or history is never a
   finding.
7. One topic at a time: a finding about a sibling topic's guideline names the
   sibling, and the orchestrator routes it there; it is not this topic's to
   fix.

Write one roled guideline, as a single markdown doc with frontmatter, that:
- keeps every rule whose verdict is `supported`, reworded only where the
  research says it is wrong or unclear, at the strength of its weakest cited
  claim;
- adds a named rule for every `new` verdict, at the strength of its weakest
  cited claim;
- leaves every rule on the owner list below worded exactly as its prior
  text, citing its `<rule-name>-prior` claim: `(claim: <rule-name>-prior)`.
  Where the prior text has no MUST, SHOULD or MAY, put one lead-in in front of
  it carrying the keyword the old text implied, and keep the text after it
  word for word;
- settles none of the open questions on the owner list;
- follows /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/tbd/compliance/artifact-formatting/guideline-formatting.md,
  gf-roled-parts and gf-named-rules: an intro; a `## Rules` section of
  named rules `- **kebab-name**: … MUST|SHOULD|MAY …`; how-to and example
  sections; `## What a reviewer looks for`;
  `## A complete review must establish`; `## A build must establish`;
  `## Rationale`; `## References`; `## Change History`;
- gives `## A build must establish` exactly one line per named rule,
  `` - `rule-name`: … ``, and no line naming anything that is not a named
  rule of `## Rules` (`cookr roles check` refuses a rule with no line and a
  line naming no rule);
- cites research exactly as `cookr validate` enforces it: every named rule
  ends with one citation, `(claim: <id>)` or `(claims: <id>, <id>)`, with
  nothing after it, not even a full stop; only one citation per rule;
  every id is a claim `id` in research.json that some verdict names
  (gf-rule-cites-research);
- updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` to match the new text, and leaves `version`, `modified` and Change History to stage 5's `cookr bump`.

Edit only the draft. Never edit research, the owner list or another topic.
A finding you think is wrong is disputed, not obeyed: see the round sections
below, when there are any.

Verdicts:
- cf-valid-json: supported (claims: jsonschema-defined-over-json, rfc8259-parser-accepts-grammar)
- cf-schema-valid: supported (claims: jsonschema-defined-over-json, python-jsonschema-iter-errors, schemastore-validate-with-ajv, cargo-version-three-numeric-parts)
- cf-type-field: unsupported (claims: cf-type-field-prior, jsonschema-const-keyword)
- cf-required-identity-fields: supported (claims: jsonschema-required-keyword, npm-name-version-unique-identifier)
- cf-required-project-fields: unsupported (claims: cf-required-project-fields-prior, npm-name-version-required-to-publish)
- cf-dependencies-in-cookr-config: unsupported (claims: cf-dependencies-in-cookr-config-prior)
- cf-uuid-format: contradicted (claims: cf-uuid-format-prior, rfc9562-obsoletes-rfc4122, rfc9562-hex-and-dash, rfc9562-treat-uuids-opaquely)
- cf-rdid-format: supported (claims: npm-name-no-uppercase, cargo-name-characters)
- cf-semver-fields: contradicted (claims: cf-semver-fields-prior, semver-normal-version-form, semver-no-leading-zeroes, semver-prerelease-allowed, semver-build-metadata-allowed, semver-suggested-regex, npm-version-node-semver)
- cf-format-is-integer: supported (claims: jsonschema-const-keyword, android-versioncode-integer)
- cf-structure-present: unsupported (claims: cf-structure-present-prior)
- cf-spec-paths-valid: supported (claims: cargo-path-relative-to-manifest, cargo-path-must-point-to-folder, rfc3986-relative-path-reference)
- cf-source-domains: unsupported (claims: cf-source-domains-prior, rfc9562-hex-and-dash)
- cf-structure-kind: unsupported (claims: cf-structure-kind-prior, jsonschema-enum-keyword)
- cf-library-tree-is-arrangement: unsupported (claims: cf-library-tree-is-arrangement-prior)
- cf-library-tree-mirrors-code: unsupported (claims: cf-library-tree-mirrors-code-prior)
- cf-library-elements-consistent: unsupported (claims: cf-library-elements-consistent-prior)
- cf-code-roots: unsupported (claims: cf-code-roots-prior)
- cf-code-root-fields: unsupported (claims: cf-code-root-fields-prior)
- cf-code-root-coverage: unsupported (claims: cf-code-root-coverage-prior)
- cf-no-circular-deps: supported (claims: dependency-graph-is-a-dag, go-import-cycles-illegal, topological-order-needs-dag)
- schema-dialect-2020-12: supported (claims: jsonschema-schema-keyword-should-be-used, ietf-jsonschema-draft-not-ready, schemastore-recommends-draft-07)
- schema-required-identity: supported (claims: jsonschema-required-keyword, npm-name-version-unique-identifier)
- schema-format-const-2: supported (claims: jsonschema-const-keyword, android-versioncode-integer)
- schema-id-uuid-pattern: supported (claims: rfc9562-hex-and-dash, rfc9562-mixed-case, jsonschema-pattern-not-anchored)
- schema-rdid-pattern: supported (claims: npm-name-no-uppercase, cargo-name-characters, jsonschema-pattern-not-anchored)
- schema-version-pattern: contradicted (claims: schema-version-pattern-prior, semver-no-leading-zeroes, semver-prerelease-allowed, semver-build-metadata-allowed, semver-suggested-regex)
- schema-license-spdx: supported (claims: spdx-short-identifiers, npm-license-spdx-identifier, cargo-license-spdx-expression)
- schema-date-format: supported (claims: jsonschema-date-is-rfc3339-full-date, rfc3339-iso8601-profile, jsonschema-format-assertion-off-by-default)
- schema-closed-objects: supported (claims: cargo-warns-unused-keys, schemastore-stricter-checking-for-typos, jsonschema-unknown-keywords-annotations, schemastore-dont-blindly-close)
- schema-source-id-pattern: supported (claims: rfc9562-hex-and-dash, rfc9562-mixed-case)
- schema-structure-kind-enum: unsupported (claims: schema-structure-kind-enum-prior, jsonschema-enum-keyword)
- schema-paths-are-strings: supported (claims: rfc3986-relative-path-reference, cargo-path-relative-to-manifest, jsonschema-uri-reference-format)
- schema-depends-on-dot-paths: unsupported (claims: schema-depends-on-dot-paths-prior)
- enable-format-assertion: new (claims: jsonschema-format-assertion-off-by-default, python-jsonschema-format-off-by-default, python-jsonschema-format-checker-opt-in, python-jsonschema-format-deps-silent, ajv-formats-not-included, ajv-formats-uuid-rfc4122)
- semantic-checks-in-code: new (claims: ajv-data-reference, cargo-package-verify-build, graphlib-cycle-error-reports-cycle, jsonschema-defined-over-json)
- report-every-error-with-its-location: new (claims: python-jsonschema-iter-errors, graphlib-cycle-error-reports-cycle)
- schema-has-stable-absolute-id: new (claims: jsonschema-id-absolute-uri, schemastore-version-suffixed-schemas)
- no-duplicate-member-names: new (claims: rfc8259-names-should-be-unique, rfc8259-duplicate-names-unpredictable)
- manifest-is-utf8-without-bom: new (claims: rfc8259-utf8-exchange, rfc8259-no-bom)
- depends-on-items-unique: new (claims: jsonschema-unique-items)
- released-version-is-immutable: new (claims: semver-released-version-immutable)
- schema-has-positive-and-negative-tests: new (claims: schemastore-test-files, schemastore-validate-with-ajv, json-schema-test-suite)
- validate-the-schema-strictly: new (claims: ajv-strict-mode-purpose, ajv-unknown-keywords-fail, jsonschema-unknown-keywords-annotations)
- closed-objects-keep-an-extension-point: new (claims: cargo-metadata-ignored, schemastore-new-properties-should-not-error, additionalproperties-same-subschema, unevaluatedproperties-sees-subschemas)
- guideline-generated-from-schema: new (claims: json-schema-for-humans-generates-docs, cloudflare-docs-from-schema)
- uuid-compared-not-parsed: new (claims: rfc9562-treat-uuids-opaquely, rfc4122-lowercase-output, rfc9562-mixed-case)
- relative-paths-stay-inside-the-cookbook: new (claims: rfc3986-dot-segments, cargo-path-must-point-to-folder)
- version-is-full-semver: new (claims: semver-suggested-regex, swiftpm-version-semver, android-semver-good-basis, npm-version-node-semver)
- schema-association-declared: new (claims: vscode-schema-association)

Second-check corrections, refuted (criteria 3 applies to these claims):
- rfc9562-treat-uuids-opaquely: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST
- jsonschema-defined-over-json: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST
- schemastore-version-suffixed-schemas: refuted (quote-found yes, supports-claim partly); trust 62 -> 42; a rule citing it cannot carry MUST
- jsonschema-unknown-keywords-annotations: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST
- cargo-metadata-ignored: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **cf-type-field** — verdict `unsupported` (claims: cf-type-field-prior, jsonschema-const-keyword). Prior text, kept word for word: "The `type` field MUST be `\"cookbook\"`. This distinguishes project cookbook manifests from other JSON files in the repository."
  - against: JSON Schema's const keyword pins a field to one exact value, such as a format integer.
- **cf-required-project-fields** — verdict `unsupported` (claims: cf-required-project-fields-prior, npm-name-version-required-to-publish). Prior text, kept word for word: "A project cookbook MUST also have `type`, `name`, `version`, `description`, `author`, `license`, `created`, `modified` and `platforms`."
  - against: npm requires only name and version, and only for a package that will be published; the other manifest fields are optional.
- **cf-dependencies-in-cookr-config** — verdict `unsupported` (claims: cf-dependencies-in-cookr-config-prior). Prior text, kept word for word: "Cookbooks this one links into are not listed here: they are `dependencies` in the repo's `.cookr.json` (`references/cookr-config.schema.json`)." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **cf-uuid-format** — verdict `contradicted` (claims: cf-uuid-format-prior, rfc9562-obsoletes-rfc4122, rfc9562-hex-and-dash, rfc9562-treat-uuids-opaquely). Prior text, kept word for word: "The `id` field MUST be a valid UUID (RFC 4122). It is the cookbook's identity: a foreign link names it (`<cookbook-uuid>/<artifact-uuid>`), and it stays stable even if the cookbook directory is renamed."
  - against: RFC 9562 obsoletes RFC 4122 as the UUID specification.
  - against: RFC 9562 represents a UUID as the hex-and-dash string, 8-4-4-4-12 hex digits.
  - against: RFC 9562 recommends treating UUIDs as opaque, so a manifest's identity UUID should be compared, never parsed for meaning.
- **cf-semver-fields** — verdict `contradicted` (claims: cf-semver-fields-prior, semver-normal-version-form, semver-no-leading-zeroes, semver-prerelease-allowed, semver-build-metadata-allowed, semver-suggested-regex, npm-version-node-semver). Prior text, kept word for word: "The `version` field MUST be a valid semver string matching the pattern `^\d+\.\d+\.\d+$`."
  - against: Semantic Versioning 2.0.0's normal version is X.Y.Z of non-negative integers.
  - against: Semantic Versioning 2.0.0 forbids leading zeroes in X, Y and Z, which the pattern ^\d+\.\d+\.\d+$ accepts (e.g. 01.2.3).
  - against: Semantic Versioning 2.0.0 allows a pre-release suffix after the patch version, which ^\d+\.\d+\.\d+$ rejects.
  - against: Semantic Versioning 2.0.0 allows build metadata after a plus sign, which ^\d+\.\d+\.\d+$ rejects.
  - against: semver.org publishes a suggested ECMAScript/PCRE/Python-compatible regular expression whose core excludes leading zeroes.
  - against: npm requires the manifest version to parse as semver by its node-semver library.
- **cf-structure-present** — verdict `unsupported` (claims: cf-structure-present-prior). Prior text, kept word for word: "The `structure` field MUST be present and contain at least a `description` field. The structure is the root of the element tree — without it, the cookbook defines nothing to build."
- **cf-source-domains** — verdict `unsupported` (claims: cf-source-domains-prior, rfc9562-hex-and-dash). Prior text, kept word for word: "Every `source.id` field MUST be the UUID of an ingredient or recipe, written `<cookbook-uuid>/<artifact-uuid>` when it is another cookbook's, and MUST resolve in that cookbook's `index.json`. Source provenance ties forked specs back to their cookbook origin."
  - against: RFC 9562 represents a UUID as the hex-and-dash string, 8-4-4-4-12 hex digits.
- **cf-structure-kind** — verdict `unsupported` (claims: cf-structure-kind-prior, jsonschema-enum-keyword). Prior text, kept word for word: "When present, `structure.kind` MUST be one of `app`, `library`, `plugin`, `widget`. It names what the cookbook assembles. A `library` cookbook specifies a set of reusable components rather than one product."
  - against: JSON Schema's enum keyword restricts a field to a closed list of values.
- **cf-library-tree-is-arrangement** — verdict `unsupported` (claims: cf-library-tree-is-arrangement-prior). Prior text, kept word for word: "In a `library` cookbook the directory tree under the cookbook directory is the arrangement: each directory is a group of components and each ingredient or recipe file is one component, named by its file name." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **cf-library-tree-mirrors-code** — verdict `unsupported` (claims: cf-library-tree-mirrors-code-prior). Prior text, kept word for word: "The tree SHOULD mirror the arrangement of the code its implementations (in `index.json`) point at."
- **cf-library-elements-consistent** — verdict `unsupported` (claims: cf-library-elements-consistent-prior). Prior text, kept word for word: "`structural-elements` MAY be omitted; when present it MUST NOT contradict the directory tree."
- **cf-code-roots** — verdict `unsupported` (claims: cf-code-roots-prior). Prior text, kept word for word: "`cookbook.json` MUST NOT carry a `code` block: code roots are tool configuration and live in the repo's `.cookr.json` (`references/cookr-config.schema.json`)."
- **cf-code-root-fields** — verdict `unsupported` (claims: cf-code-root-fields-prior). Prior text, kept word for word: "There, each root MUST name an existing directory (`path`, relative to the repository root) and a `platform` (`macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`), and MAY give a `kind` (`ui` or `logic`), a `group` (the cookbook folder its recipes belong in) and an `ignore` list of globs; top-level `ignore` globs apply to every root."
- **cf-code-root-coverage** — verdict `unsupported` (claims: cf-code-root-coverage-prior). Prior text, kept word for word: "Every source file under a root MUST be covered by some artifact's implementations; `cookr coverage` reports the files that are not."
- **schema-version-pattern** — verdict `contradicted` (claims: schema-version-pattern-prior, semver-no-leading-zeroes, semver-prerelease-allowed, semver-build-metadata-allowed, semver-suggested-regex). Prior text, kept word for word: ""version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$", "description": "Cookbook version (semver)" }" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Semantic Versioning 2.0.0 forbids leading zeroes in X, Y and Z, which the pattern ^\d+\.\d+\.\d+$ accepts (e.g. 01.2.3).
  - against: Semantic Versioning 2.0.0 allows a pre-release suffix after the patch version, which ^\d+\.\d+\.\d+$ rejects.
  - against: Semantic Versioning 2.0.0 allows build metadata after a plus sign, which ^\d+\.\d+\.\d+$ rejects.
  - against: semver.org publishes a suggested ECMAScript/PCRE/Python-compatible regular expression whose core excludes leading zeroes.
- **schema-structure-kind-enum** — verdict `unsupported` (claims: schema-structure-kind-enum-prior, jsonschema-enum-keyword). Prior text, kept word for word: ""kind": { "type": "string", "enum": [ "app", "library", "plugin", "widget" ], "description": "What the element is. Set on the top-level structure; a library's directory tree is its arrangement and its elements MAY be omitted" }"
  - against: JSON Schema's enum keyword restricts a field to a closed list of values.
- **schema-depends-on-dot-paths** — verdict `unsupported` (claims: schema-depends-on-dot-paths-prior). Prior text, kept word for word: ""depends-on": { "type": "array", "items": { "type": "string" }, "description": "Dot-path structural element keys this element depends on" }" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.

## Open questions

- Whether the manifest's version field should accept full Semantic Versioning 2.0.0 (pre-release and build metadata, no leading zeroes, using semver.org's suggested regular expression) or deliberately accept only a plain X.Y.Z core; either way the pattern should forbid leading zeroes if the description keeps the word semver.
- Whether cookr should enable a JSON Schema format checker so `format: date` (and a `format: uuid` if added) assert, or whether those fields should carry an explicit pattern instead; at the base commit the schema relies on format for created and modified.
- Whether `additionalProperties: false` stays on every object or the manifest gains an extension point (as Cargo's ignored `package.metadata` table), given SchemaStore's advice that new properties from a newer tool version should not error.
- Whether the schema's `$id` (http://agenticdevelopercookbook.com/schemas/cookbook.schema.json at the base commit) should move to https and carry the format version, so a schema for format 3 can sit beside format 2.
- Whether a cookbook.json should name its schema in the instance (a `$schema` member, as VS Code supports for editor association); the schema at the base commit already permits an optional top-level `$schema` string, so the question is whether naming it becomes a rule.
- Whether UUIDs in the manifest should be written in lowercase (RFC 4122's output rule) or accepted in any case (RFC 9562 allows all upper, all lower or mixed), and whether cookr normalises them.
- Whether the rdid pattern ^[a-z][a-z0-9-]*$ should be tightened to true kebab-case (no trailing or doubled hyphens) to match cf-rdid-format's wording.
- Whether created <= modified is a rule, and whether license must be a single SPDX identifier or may be an SPDX license expression as npm and Cargo accept.
- The project-specific rules no outside source requires (cf-type-field, cf-required-project-fields, cf-dependencies-in-cookr-config, cf-structure-present, cf-source-domains, cf-structure-kind, cf-library-tree-is-arrangement, cf-library-tree-mirrors-code, cf-library-elements-consistent, cf-code-roots, cf-code-root-fields, cf-code-root-coverage, schema-structure-kind-enum, schema-depends-on-dot-paths): keep each as the owner's design ruling, change it, or drop it.
