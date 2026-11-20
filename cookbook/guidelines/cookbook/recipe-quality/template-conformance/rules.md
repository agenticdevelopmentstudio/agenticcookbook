
### Frontmatter

- **must-begin-with-yaml-frontmatter**: The recipe MUST begin with a valid YAML frontmatter block delimited by `---` on the first and last lines.
- **must-include-required-frontmatter-fields**: The frontmatter MUST include all required fields: `id`, `title`, `type`, `version`, `status`, `language`, `created`, `modified`, `author`, and `summary`.
- **must-use-unique-uuid-v4-id**: The `id` field MUST be a valid UUID v4 string in canonical hyphenated format (e.g., `550e8400-e29b-41d4-a716-446655440000`). No two recipes in the cookbook MAY share the same `id`.
- **must-match-title-to-heading**: The `title` field MUST be a non-empty string that matches the `# Title` heading in the document body.
- **must-have-index-entry-and-matching-rdid**: The recipe MUST have an entry in its cookbook's `index.json`, and its rdid MUST end with the recipe's folder name (e.g., `adc.recipe.ui.button` for `recipes/ui/button/`).
- **must-use-recognized-type**: The `type` field MUST be one of the recognized cookbook artifact types: `recipe`, `guideline`, `pattern`, or `spec`.
- **must-use-semver-version**: The `version` field MUST be a valid semantic version string (MAJOR.MINOR.PATCH, e.g., `1.0.0`). Pre-release labels and build metadata are NOT permitted.
- **must-use-recognized-status**: The `status` field MUST be one of: `draft`, `review`, `accepted`, or `deprecated`.
- **must-use-bcp-47-language**: The `language` field MUST be a valid BCP 47 language tag (e.g., `en`, `fr`, `zh-Hans`).
- **must-use-iso-8601-dates**: The `created` and `modified` fields MUST be ISO 8601 calendar dates in `YYYY-MM-DD` format.
- **must-make-platforms-a-sequence**: The `platforms` field MUST be a YAML sequence (array) of one or more platform identifiers from the canonical platform list. It MUST NOT be a scalar string.
- **must-make-tags-a-sequence**: The `tags` field MUST be a YAML sequence. An empty sequence (`[]`) is permitted.
- **must-keep-summary-single-line-and-short**: The `summary` field MUST be a single-line string of no more than 160 characters. It MUST NOT be a multi-line block scalar.
- **must-make-link-fields-present-sequences**: The `depends-on`, `related`, and `references` fields MUST be YAML sequences. Each MUST be present even if empty.

### Document Structure

- **must-open-body-with-h1**: The document body MUST begin with a level-1 heading (`# Title`) immediately after the closing frontmatter delimiter.
- **must-contain-template-sections-in-order**: The recipe MUST contain all sections defined in the standard template, in the prescribed order.
  - For component recipes, the required sections in order are: **Overview**, **Behavioral Requirements**, **Appearance**, **States**, **Accessibility**, **Conformance Test Vectors**, **Edge Cases**.
- **must-use-exact-section-names**: Section headings MUST use the exact names specified in the template. Aliases (e.g., "Behavior" for "Behavioral Requirements") are NOT permitted.
- **must-use-level-2-section-headings**: Sections MUST be introduced as level-2 headings (`## Section Name`).
- **must-not-omit-required-sections**: No required section MAY be omitted, even if its content is marked `NEEDS REVIEW`.
- **may-append-extra-sections-at-end**: Additional sections MAY be appended after the final required section.
- **must-not-insert-sections-between-required**: They MUST NOT be inserted between required sections.

### Change History

- **must-end-with-change-history**: The recipe MUST include a `## Change History` section as the final section in the document.
- **may-leave-change-history-empty-initially**: The section body MAY be empty at initial creation.

