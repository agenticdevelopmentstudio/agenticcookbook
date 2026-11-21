# Owner list: cookbook-formatting

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
