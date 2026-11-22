# Integrate: cookbook-formatting

## For the owner

Rules standing as they were until you decide each (`cookr validate` owner-decides):

- rule 'cf-uuid-format' cites 'cf-uuid-format-prior', which the research rules contradicted
- rule 'cf-type-field' cites 'cf-type-field-prior', which the research rules unsupported
- rule 'cf-required-project-fields' cites 'cf-required-project-fields-prior', which the research rules unsupported
- rule 'cf-dependencies-in-cookr-config' cites 'cf-dependencies-in-cookr-config-prior', which the research rules unsupported
- rule 'cf-semver-fields' cites 'cf-semver-fields-prior', which the research rules contradicted
- rule 'cf-structure-present' cites 'cf-structure-present-prior', which the research rules unsupported
- rule 'cf-structure-kind' cites 'cf-structure-kind-prior', which the research rules unsupported
- rule 'cf-library-tree-is-arrangement' cites 'cf-library-tree-is-arrangement-prior', which the research rules unsupported
- rule 'cf-library-tree-mirrors-code' cites 'cf-library-tree-mirrors-code-prior', which the research rules unsupported
- rule 'cf-library-elements-consistent' cites 'cf-library-elements-consistent-prior', which the research rules unsupported
- rule 'cf-source-domains' cites 'cf-source-domains-prior', which the research rules unsupported
- rule 'cf-code-roots' cites 'cf-code-roots-prior', which the research rules unsupported
- rule 'cf-code-root-fields' cites 'cf-code-root-fields-prior', which the research rules unsupported
- rule 'cf-code-root-coverage' cites 'cf-code-root-coverage-prior', which the research rules unsupported
- rule 'schema-version-pattern' cites 'schema-version-pattern-prior', which the research rules contradicted
- rule 'schema-structure-kind-enum' cites 'schema-structure-kind-enum-prior', which the research rules unsupported
- rule 'schema-depends-on-dot-paths' cites 'schema-depends-on-dot-paths-prior', which the research rules unsupported

Open questions from the owner list:

- Whether the manifest's version field should accept full Semantic Versioning 2.0.0 (pre-release and build metadata, no leading zeroes, using semver.org's suggested regular expression) or deliberately accept only a plain X.Y.Z core; either way the pattern should forbid leading zeroes if the description keeps the word semver.
- Whether cookr should enable a JSON Schema format checker so `format: date` (and a `format: uuid` if added) assert, or whether those fields should carry an explicit pattern instead; at the base commit the schema relies on format for created and modified.
- Whether `additionalProperties: false` stays on every object or the manifest gains an extension point (as Cargo's ignored `package.metadata` table), given SchemaStore's advice that new properties from a newer tool version should not error.
- Whether the schema's `$id` (http://agenticdevelopercookbook.com/schemas/cookbook.schema.json at the base commit) should move to https and carry the format version, so a schema for format 3 can sit beside format 2.
- Whether a cookbook.json should name its schema in the instance (a `$schema` member, as VS Code supports for editor association); the schema at the base commit already permits an optional top-level `$schema` string, so the question is whether naming it becomes a rule.
- Whether UUIDs in the manifest should be written in lowercase (RFC 4122's output rule) or accepted in any case (RFC 9562 allows all upper, all lower or mixed), and whether cookr normalises them.
- Whether the rdid pattern ^[a-z][a-z0-9-]*$ should be tightened to true kebab-case (no trailing or doubled hyphens) to match cf-rdid-format's wording.
- Whether created <= modified is a rule, and whether license must be a single SPDX identifier or may be an SPDX license expression as npm and Cargo accept.
- The project-specific rules no outside source requires (cf-type-field, cf-required-project-fields, cf-dependencies-in-cookr-config, cf-structure-present, cf-source-domains, cf-structure-kind, cf-library-tree-is-arrangement, cf-library-tree-mirrors-code, cf-library-elements-consistent, cf-code-roots, cf-code-root-fields, cf-code-root-coverage, schema-structure-kind-enum, schema-depends-on-dot-paths): keep each as the owner's design ruling, change it, or drop it.

Notes:

- Round 3's first review read the folder before the round-3 draft was folded into it, and failed on that; it is kept in run-3-void/ and round 3 was redone on the folded text (pass, lint clean).
- The cf-type-field style warning (the backslash in \"cookbook\") stays, because the prior text is kept word for word.

## Lossless

New topic, no base text (`cookr roles lossless`: not in the base commit).

## Validate

`cookr validate` passed; bumped 1.0.0 → 1.0.1.

integrated: 2026-11-22
