# Research brief: cookbook-formatting

- **Topic:** cookbook-formatting, area `cookbook/authoring`.
- **Artifact:** `cookbook/guidelines/cookbook/authoring/cookbook-formatting` (new; its folder holds only `research/` until stage 3).
- **What it rules:** the `cookbook.json` manifest, a cookbook's identity and, for a project cookbook, the application, plugin, widget or library it assembles from recipes and ingredients.
- **Base commit:** `071e52f9572bf4b7c534cfcf95fb111282abc423` (`base.txt`).
- **Research type:** Technology / software (intent Do; domain data-format validation; method specification and tool documentation).
- **Research bar:** *Technology / software*, no escalation (owner ruling, Owner question 5: "no escalation for any topic. Each keeps its proposed bar.").
- **Sibling topic cited, never restated:** `cookbook/guidelines/cookbook/authoring/requirement-keywords` rules RFC 2119 keyword case and the severity a rule's keyword gives a lint finding (owner ruling Q10 + Q11). This topic's research does not decide keyword case or lint severity; it cites requirement-keywords for both.
- **Overlap (plan, Overlaps):** `references/cookbook.schema.json` is a reference file, not an artifact, so it is no survivor; the draft's cf-schema-valid check defers to it.

## The four questions

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

## Research questions (from the area plan)

1. Best practice: how should a manifest that assembles components into an application be validated: required fields, identifiers, semantic versions, relative paths, dependency graphs without cycles?
2. Known solutions: how do JSON Schema validators (draft 2020-12, ajv, python-jsonschema) and manifest linters (package.json, Cargo.toml, npm and Cargo's own checks) validate a manifest's schema, UUIDs, semver fields, paths and cycles, and which of the draft's 13 checks belong in `references/cookbook.schema.json` rather than in prose?
3. Platform guidelines: what do the JSON Schema specification, RFC 9562 (UUIDs), Semantic Versioning 2.0.0 and RFC 3986 (URI references) require of the fields the manifest holds?
4. The expert's view: what do schema authors say about keeping a manifest's rules in its schema versus in a written guideline, and how the two stay in step?

## Method

- Research to `cookbook/guidelines/researching/process/research-methodology-and-sources`, using its source catalogue for the domain (data-format validation: specifications, standards and tool documentation). Primary sources (the JSON Schema specification, RFC 9562, RFC 4122, Semantic Versioning 2.0.0, RFC 3986, RFC 8259, the validators' and package managers' own documentation) come before secondary ones.
- Verify every rule below. Each is quoted **verbatim** from its file at the base commit, as a claim to check, never as a source. There is no devteam text for this topic: the area has no speciality (`run_gaps.py` `why_empty` "area has no speciality").
- Score each claim 0–100 per `cookbook/guidelines/researching/evidence/verification-and-trust-scoring`, applying `cite-the-claim-not-the-document`, `independence-before-corroboration`, `domain-stratified-trust`, `suppress-unsupported-confidence` and `provenance-at-generation-time`.
- `supported` means supported at the rule's stated strength. Keyword case and the lint severity of each keyword are requirement-keywords' (cite it; never restate it).
- Find what the topic is missing: practice the research finds that no rule below covers, each as a `new` verdict.

## Rules to verify

Each rule has one fixed name; research verdicts key on it, and stage 3 keeps it. A rule whose text has no MUST, SHOULD or MAY is marked **no RFC keyword**.

### From `tbd/compliance/artifact-formatting/cookbook-formatting.md` (base `071e52f9572bf4b7c534cfcf95fb111282abc423`), all 13 checks

The draft's preamble, for context (not a rule): "Cookbooks are JSON manifests that assemble recipes and ingredients into complete applications, plugins, widgets, or libraries. Each cookbook defines a structure tree of structural elements, context for LLM consumption, and resource declarations — all validated against `references/cookbook.schema.json`. Every cookbook, including a source repository like this one, carries its identity in `cookbook.json` (`format`, `id`, `rdid`) and lists its artifacts in `index.json` (`references/index.schema.json`)." Its *Applicability*: "This category applies to any `cookbook.json` file. The manifest sits at the root of its cookbook directory; every spec path is relative to that directory."

1. **cf-valid-json** (check `cf-valid-json`; applies always): "The file MUST be valid JSON. A cookbook that fails JSON parsing cannot be processed by any tooling."
2. **cf-schema-valid** (check `cf-schema-valid`; applies always): "The file MUST validate against `references/cookbook.schema.json`. Schema validation catches structural errors — missing fields, wrong types, unknown properties — before any semantic checks run."
3. **cf-type-field** (check `cf-type-field`; applies when "the manifest describes a project (it has a `structure`)"): "The `type` field MUST be `\"cookbook\"`. This distinguishes project cookbook manifests from other JSON files in the repository."
4. **cf-required-identity-fields** (check `cf-required-fields`, first sentence; applies always): "The identity fields MUST be present in every manifest: `format` (`2`), `id` and `rdid`."
5. **cf-required-project-fields** (check `cf-required-fields`, second sentence; applies "the project fields when the manifest has a `structure`"): "A project cookbook MUST also have `type`, `name`, `version`, `description`, `author`, `license`, `created`, `modified` and `platforms`."
6. **cf-dependencies-in-cookr-config** (check `cf-required-fields`, third sentence; **no RFC keyword**): "Cookbooks this one links into are not listed here: they are `dependencies` in the repo's `.cookr.json` (`references/cookr-config.schema.json`)."
7. **cf-uuid-format** (check `cf-uuid-format`, first and second sentences; applies always): "The `id` field MUST be a valid UUID (RFC 4122). It is the cookbook's identity: a foreign link names it (`<cookbook-uuid>/<artifact-uuid>`), and it stays stable even if the cookbook directory is renamed."
8. **cf-rdid-format** (check `cf-uuid-format`, third sentence; applies always): "The `rdid` MUST be one lowercase kebab-case segment (`adc`); it is the first segment of every rdid in the cookbook's index."
9. **cf-semver-fields** (check `cf-semver-fields`, first sentence; applies when "`version` is present"): "The `version` field MUST be a valid semver string matching the pattern `^\d+\.\d+\.\d+$`."
10. **cf-format-is-integer** (check `cf-semver-fields`, second sentence; **no RFC keyword**): "The manifest format is the whole number `format`, not a semver string."
11. **cf-structure-present** (check `cf-structure-present`; applies when "the manifest describes a project. A source cookbook of principles, guidelines, ingredients and recipes has no `structure`."): "The `structure` field MUST be present and contain at least a `description` field. The structure is the root of the element tree — without it, the cookbook defines nothing to build."
12. **cf-spec-paths-valid** (check `cf-spec-paths-valid`; applies when "any structural element contains a `spec` field"): "Every `spec` field in the structure tree MUST reference an existing markdown file (relative to the cookbook directory). Broken spec paths mean the agent cannot find the spec to implement."
13. **cf-source-domains** (check `cf-source-domains`; applies when "any structural element contains a `source` object"): "Every `source.id` field MUST be the UUID of an ingredient or recipe, written `<cookbook-uuid>/<artifact-uuid>` when it is another cookbook's, and MUST resolve in that cookbook's `index.json`. Source provenance ties forked specs back to their cookbook origin."
14. **cf-structure-kind** (check `cf-structure-kind`; applies when "`structure.kind` is present"): "When present, `structure.kind` MUST be one of `app`, `library`, `plugin`, `widget`. It names what the cookbook assembles. A `library` cookbook specifies a set of reusable components rather than one product."
15. **cf-library-tree-is-arrangement** (check `cf-library-layout`, first sentence; applies when "`structure.kind` is `library`"; **no RFC keyword**): "In a `library` cookbook the directory tree under the cookbook directory is the arrangement: each directory is a group of components and each ingredient or recipe file is one component, named by its file name."
16. **cf-library-tree-mirrors-code** (check `cf-library-layout`, second sentence; applies when "`structure.kind` is `library`"): "The tree SHOULD mirror the arrangement of the code its implementations (in `index.json`) point at."
17. **cf-library-elements-consistent** (check `cf-library-layout`, third sentence; applies when "`structure.kind` is `library`"): "`structural-elements` MAY be omitted; when present it MUST NOT contradict the directory tree."
18. **cf-code-roots** (check `cf-code-roots`, first sentence; applies when "the repo has a `.cookr.json` with `roots`"): "`cookbook.json` MUST NOT carry a `code` block: code roots are tool configuration and live in the repo's `.cookr.json` (`references/cookr-config.schema.json`)."
19. **cf-code-root-fields** (check `cf-code-roots`, second sentence; same condition): "There, each root MUST name an existing directory (`path`, relative to the repository root) and a `platform` (`macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`), and MAY give a `kind` (`ui` or `logic`), a `group` (the cookbook folder its recipes belong in) and an `ignore` list of globs; top-level `ignore` globs apply to every root."
20. **cf-code-root-coverage** (check `cf-code-roots`, third sentence; same condition): "Every source file under a root MUST be covered by some artifact's implementations; `cookr coverage` reports the files that are not."
21. **cf-no-circular-deps** (check `cf-no-circular-deps`; applies when "any structural element contains a `depends-on` array"): "The `depends-on` dot-paths in the structure tree MUST NOT form circular dependencies. Circular dependencies make build ordering impossible."

### From `references/cookbook.schema.json` (base `071e52f9572bf4b7c534cfcf95fb111282abc423`)

Each schema statement below is quoted verbatim (JSON fragments as they stand in the file) as a claim to check; each is a rule of the schema, **no RFC keyword** unless its text holds one.

22. **schema-dialect-2020-12** (no RFC keyword): `"$schema": "https://json-schema.org/draft/2020-12/schema"`
23. **schema-required-identity** (no RFC keyword): `"required": [ "format", "id", "rdid" ]` (top level)
24. **schema-format-const-2** (no RFC keyword): `"format": { "const": 2, "description": "Manifest format version. cookr reads only format 2; `cookr upgrade` converts older manifests." }`
25. **schema-id-uuid-pattern** (no RFC keyword): `"id": { "type": "string", "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", "description": "UUID — the cookbook's identity. Foreign links name it: `<cookbook-uuid>/<artifact-uuid>`." }`
26. **schema-rdid-pattern** (no RFC keyword): `"rdid": { "type": "string", "pattern": "^[a-z][a-z0-9-]*$", "description": "The cookbook's readable name (`adc`, `adhsdk`); the first segment of every rdid in its index." }`
27. **schema-version-pattern** (no RFC keyword): `"version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$", "description": "Cookbook version (semver)" }`, and the same pattern on `source.version` (`"description": "Artifact version that was forked"`).
28. **schema-license-spdx** (no RFC keyword): `"license": { "type": "string", "description": "SPDX license identifier" }`
29. **schema-date-format** (no RFC keyword): `"created": { "type": "string", "format": "date", "description": "ISO 8601 date, immutable" }` and `"modified": { "type": "string", "format": "date", "description": "ISO 8601 date, updated on changes" }`
30. **schema-closed-objects** (no RFC keyword): `"additionalProperties": false` on the top-level object, `context`, `structural-element`, `source`, `resource` and `context-entry`.
31. **schema-source-id-pattern** (no RFC keyword): `"source": { "type": "object", "required": [ "id", "version" ], ... "id": { "type": "string", "pattern": "^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/)?[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", "description": "The source ingredient or recipe: its UUID, or `<cookbook-uuid>/<artifact-uuid>` when it is another cookbook's" } ..., "description": "Cookbook provenance — only present on forked artifacts" }`
32. **schema-structure-kind-enum** (the description holds MAY): `"kind": { "type": "string", "enum": [ "app", "library", "plugin", "widget" ], "description": "What the element is. Set on the top-level structure; a library's directory tree is its arrangement and its elements MAY be omitted" }`
33. **schema-paths-are-strings** (no RFC keyword): `"spec": { "type": "string", "description": "Relative path to the markdown spec file (ingredient or recipe)" }`, `"path": { "type": "string", "description": "Relative path to the resource definition file" }` (resource) and `"path": { "type": "string", "description": "Relative path to the markdown file" }` (context-entry).
34. **schema-depends-on-dot-paths** (no RFC keyword): `"depends-on": { "type": "array", "items": { "type": "string" }, "description": "Dot-path structural element keys this element depends on" }`

## What to find that no rule covers

For example (each only if the research finds it): whether the manifest's schema should be versioned and published at a stable `$id`; how a `cookbook.json` declares which schema it is validated against; how `created` ≤ `modified` and other cross-field constraints are checked; uniqueness of identifiers; how semantic checks the schema cannot express (path existence, cycles, cross-file resolution) are reported; how the schema and a written guideline are kept in step (a schema test suite, generated docs). Record each as a `new` verdict with the strength its sources support.
