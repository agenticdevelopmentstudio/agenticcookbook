
A verifier MUST check each of the following items. The recipe PASSES template conformance only if every item is satisfied.

- [ ] Frontmatter opens and closes with `---` on its own line.
- [ ] All required frontmatter fields are present: `id`, `title`, `domain`, `type`, `version`, `status`, `language`, `created`, `modified`, `author`, `summary`, `platforms`, `tags`, `depends-on`, `related`, `references`.
- [ ] `id` is a valid UUID v4 and is unique within the cookbook.
- [ ] `domain`'s scheme names the repo the file lives in (`agenticdevelopercookbook://` for this cookbook's own content) and its path ends with the file's stem.
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

