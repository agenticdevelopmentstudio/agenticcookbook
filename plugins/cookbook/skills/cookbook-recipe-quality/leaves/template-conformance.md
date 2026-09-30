<!-- leaf: cookbook-recipe-quality/template-conformance · source: guidelines/cookbook/recipe-quality/template-conformance.md -->

**Rules** (cite as `cookbook-recipe-quality/template-conformance#<slug>`):

- `recipe-begin-valid-yaml-frontmatter` MUST — The recipe MUST begin with a valid YAML frontmatter block delimited by --- on the first and last lines.
- `frontmatter-include-fields-id-title` MUST — The frontmatter MUST include all required fields: id, title, domain, type, version, status, language, created, …
- `id-field-valid-uuid-v4-string` MUST — The id field MUST be a valid UUID v4 string in canonical hyphenated format (e.g., …
- `title-field-non-empty-string-matches` MUST — The title field MUST be a non-empty string that matches the # Title heading in the document body.
- `domain-field-uri-beginning-agenticdevelopercookbook-end` MUST — The domain field MUST be a URI beginning with agenticdevelopercookbook:// and MUST end with the filename stem of the …
- `type-field-one-recognized-cookbook-artifact` MUST — The type field MUST be one of the recognized cookbook artifact types: recipe, guideline, pattern, or spec.
- `version-field-valid-semantic-version-string` MUST — The version field MUST be a valid semantic version string (MAJOR.MINOR.PATCH, e.g., 1.0.0). Pre-release labels and …
- `status-field-one-draft-review-accepted` MUST — The status field MUST be one of: draft, review, accepted, or deprecated.
- `language-field-valid-bcp-47-language` MUST — The language field MUST be a valid BCP 47 language tag (e.g., en, fr, zh-Hans).
- `created-modified-fields-iso-8601-calendar-dates` MUST — The created and modified fields MUST be ISO 8601 calendar dates in YYYY-MM-DD format.
- `platforms-field-yaml-sequence-array-one` MUST — The platforms field MUST be a YAML sequence (array) of one or more platform identifiers from the canonical platform …
- `tags-field-yaml-sequence-empty-sequence` MUST — The tags field MUST be a YAML sequence. An empty sequence ([]) is permitted.
- `summary-field-single-line-string-more` MUST — The summary field MUST be a single-line string of no more than 160 characters. It MUST NOT be a multi-line block scalar.
- `related-references-fields-yaml-sequences-present-even` MUST — The depends-on, related, and references fields MUST be YAML sequences. Each MUST be present even if empty.
- `document-body-begin-level-heading-title` MUST — The document body MUST begin with a level-1 heading (# Title) immediately after the closing frontmatter delimiter.
- `recipe-contain-sections-defined-standard` MUST — The recipe MUST contain all sections defined in the standard template, in the prescribed order.
- `section-headings-use-exact-names-specified` MUST — Section headings MUST use the exact names specified in the template. Aliases (e.g., "Behavior" for "Behavioral …
- `sections-introduced-level-headings-section` MUST — Sections MUST be introduced as level-2 headings (## Section Name).
- `section-omitted-even-content-marked` MAY — No required section MAY be omitted, even if its content is marked NEEDS REVIEW.
- `additional-sections-appended-after-final-section` MUST — Additional sections MAY be appended after the final required section. They MUST NOT be inserted between required …
- `recipe-include-change-history-section` MUST — The recipe MUST include a ## Change History section as the final section in the document.
- `section-body-empty-initial-creation` MAY — The section body MAY be empty at initial creation.
- `verifier-check-following-items-recipe` MUST — A verifier MUST check each of the following items. The recipe PASSES template conformance only if every item is …

# Template Conformance

Template conformance verifies that a recipe adheres to the structural contract defined by the cookbook's standard recipe template. A conformant recipe is predictable: reviewers know where to find information, automated tooling can parse it reliably, and consumers can apply it without hunting for context. Structural deviations — missing sections, wrong field types, broken frontmatter — undermine trust in the recipe system as a whole.

## Requirements

### Frontmatter

- The recipe MUST begin with a valid YAML frontmatter block delimited by `---` on the first and last lines.
- The frontmatter MUST include all required fields: `id`, `title`, `domain`, `type`, `version`, `status`, `language`, `created`, `modified`, `author`, and `summary`.
- The `id` field MUST be a valid UUID v4 string in canonical hyphenated format (e.g., `550e8400-e29b-41d4-a716-446655440000`). No two recipes in the cookbook MAY share the same `id`.
- The `title` field MUST be a non-empty string that matches the `# Title` heading in the document body.
- The `domain` field MUST be a URI beginning with `agenticdevelopercookbook://` and MUST end with the filename stem of the recipe file (e.g., `agenticdevelopercookbook://recipes/ui/button` for `button.md`).
- The `type` field MUST be one of the recognized cookbook artifact types: `recipe`, `guideline`, `pattern`, or `spec`.
- The `version` field MUST be a valid semantic version string (MAJOR.MINOR.PATCH, e.g., `1.0.0`). Pre-release labels and build metadata are NOT permitted.
- The `status` field MUST be one of: `draft`, `review`, `accepted`, or `deprecated`.
- The `language` field MUST be a valid BCP 47 language tag (e.g., `en`, `fr`, `zh-Hans`).
- The `created` and `modified` fields MUST be ISO 8601 calendar dates in `YYYY-MM-DD` format.
- The `platforms` field MUST be a YAML sequence (array) of one or more platform identifiers from the canonical platform list. It MUST NOT be a scalar string.
- The `tags` field MUST be a YAML sequence. An empty sequence (`[]`) is permitted.
- The `summary` field MUST be a single-line string of no more than 160 characters. It MUST NOT be a multi-line block scalar.
- The `depends-on`, `related`, and `references` fields MUST be YAML sequences. Each MUST be present even if empty.

### Document Structure

- The document body MUST begin with a level-1 heading (`# Title`) immediately after the closing frontmatter delimiter.
- The recipe MUST contain all sections defined in the standard template, in the prescribed order.
- For component recipes, the required sections in order are: **Overview**, **Behavioral Requirements**, **Appearance**, **States**, **Accessibility**, **Conformance Test Vectors**, **Edge Cases**.
- Section headings MUST use the exact names specified in the template. Aliases (e.g., "Behavior" for "Behavioral Requirements") are NOT permitted.
- Sections MUST be introduced as level-2 headings (`## Section Name`).
- No required section MAY be omitted, even if its content is marked `NEEDS REVIEW`.
- Additional sections MAY be appended after the final required section. They MUST NOT be inserted between required sections.

### Change History

- The recipe MUST include a `## Change History` section as the final section in the document.
- The section body MAY be empty at initial creation.

## Common Violations

- **Missing frontmatter fields.** A recipe omits `summary` or `platforms` because the author considered them optional. The parser fails validation with a missing-key error.
- **Scalar platforms field.** `platforms: ios` instead of `platforms:\n  - ios`. The YAML type is wrong; tooling that iterates platforms breaks.
- **Invalid semver.** `version: 1.0` or `version: v1.0.0` — neither is valid semver. The correct form is `1.0.0`.
- **Empty required sections.** A recipe contains `## Accessibility` with no content and no `NEEDS REVIEW` marker. This silently passes structural checks while hiding an unfilled gap.
- **Wrong section order.** "Edge Cases" appears before "Conformance Test Vectors." Automated diffing tools and reviewers expect a fixed order; misordering signals the recipe was authored without consulting the template.
- **Title mismatch.** The frontmatter `title` is `"Submit Button"` but the document heading reads `# Primary Action Button`. These must be identical.
- **Multi-line summary.** The `summary` field uses a YAML literal block scalar (`summary: |`) and spans two lines. Parsers that expect a string scalar may coerce or truncate it unexpectedly.
- **Duplicate `id`.** A recipe is copy-pasted from an existing one and the `id` is never regenerated. The cookbook now has two artifacts with the same identity.

## Verification Checklist

A verifier MUST check each of the following items. The recipe PASSES template conformance only if every item is satisfied.

- [ ] Frontmatter opens and closes with `---` on its own line.
- [ ] All required frontmatter fields are present: `id`, `title`, `domain`, `type`, `version`, `status`, `language`, `created`, `modified`, `author`, `summary`, `platforms`, `tags`, `depends-on`, `related`, `references`.
- [ ] `id` is a valid UUID v4 and is unique within the cookbook.
- [ ] `domain` starts with `agenticdevelopercookbook://` and ends with the file's stem.
- [ ] `type` is one of the recognized artifact types.
- [ ] `version` is a valid `MAJOR.MINOR.PATCH` semver string with no prefix.
- [ ] `status` is one of `draft`, `review`, `accepted`, `deprecated`.
- [ ] `created` and `modified` are `YYYY-MM-DD` dates.
- [ ] `platforms` is a YAML sequence with at least one entry.
- [ ] `summary` is a single-line string of 160 characters or fewer.
- [ ] `tags`, `depends-on`, `related`, and `references` are YAML sequences.
- [ ] Document body opens with `# <title>` matching the frontmatter `title` exactly.
- [ ] All required sections are present, in the correct order, as level-2 headings.
- [ ] No required section is absent, even if content is `NEEDS REVIEW`.
- [ ] `## Change History` is the final section.
- [ ] No required sections are reordered or renamed.
