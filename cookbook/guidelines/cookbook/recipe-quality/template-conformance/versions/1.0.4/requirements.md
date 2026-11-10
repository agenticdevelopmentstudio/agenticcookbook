
### Frontmatter

- The recipe MUST begin with a valid YAML frontmatter block delimited by `---` on the first and last lines.
- The frontmatter MUST include all required fields: `id`, `title`, `domain`, `type`, `version`, `status`, `language`, `created`, `modified`, `author`, and `summary`.
- The `id` field MUST be a valid UUID v4 string in canonical hyphenated format (e.g., `550e8400-e29b-41d4-a716-446655440000`). No two recipes in the cookbook MAY share the same `id`.
- The `title` field MUST be a non-empty string that matches the `# Title` heading in the document body.
- The `domain` field MUST be a URI whose scheme names the repo the file lives in (`agenticdevelopercookbook://` for this cookbook's own content) and whose path MUST end with the filename stem of the recipe file (e.g., `agenticdevelopercookbook://recipes/ui/button` for `button.md`).
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

