
- **should-name-rule-files-lowercase-kebab-case**: The file name SHOULD be descriptive and lowercase kebab-case (e.g., `testing.md`, `api-design.md`).
- **may-include-a-title-or-version-in-frontmatter**: Optional frontmatter MAY include a title or version, but there is no enforced schema.

### Structure

- **should-have-a-clear-title**: A rule SHOULD have a clear title/heading identifying the rule's purpose.
- **should-number-procedural-steps**: A rule SHOULD have numbered or clearly separated steps if procedural.
- **should-give-distinct-concerns-their-own-sections**: A rule SHOULD have sections with headings for distinct concerns.

### Content

- **should-use-an-imperative-tone**: A rule SHOULD use an imperative tone: MUST, MUST NOT, SHOULD, MAY (RFC 2119).
- **should-be-deterministic**: A rule SHOULD be deterministic: the LLM SHOULD be able to follow the rule without ambiguity.
- **should-list-every-referenced-file**: A rule SHOULD have explicit file references: if the rule says "read the principles," it lists every file path.
- **should-be-self-contained-or-clearly-scoped**: A rule SHOULD be self-contained or clearly scoped: either contains all needed information or explicitly references where to find it.
- **should-not-use-vague-directives**: A rule SHOULD NOT use vague directives: "Handle errors appropriately" is bad. "Validate user input at the API boundary, return HTTP 400 with a message for invalid input" is good.

### Anti-patterns

- **should-avoid-vague-rules**: Vague rules SHOULD be avoided: "Write good code" — not actionable.
- **should-avoid-contradictory-rules**: Contradictory rules SHOULD be avoided: "Always do X" then later "Never do X".
- **should-avoid-unbounded-scope**: Unbounded scope SHOULD be avoided: a rule tries to govern everything instead of a specific concern.
- **should-avoid-missing-file-paths**: Missing file paths SHOULD be avoided: a rule says "read the guidelines" without listing which files.
- **should-avoid-duplicating-claude-md**: Duplicating CLAUDE.md SHOULD be avoided: rule content that belongs in project instructions, not a standalone rule.
- **should-avoid-rules-with-no-enforcement-mechanism**: A rule with no enforcement mechanism SHOULD be avoided: it states preferences but provides no steps to verify compliance.
- **should-keep-per-turn-content-minimal**: You SHOULD keep per-turn content, the content in the rule file itself, minimal.
- **should-put-large-reference-material-on-demand**: You SHOULD use per-session external files read on demand for large reference material.

### Key Guidelines

- **should-keep-rule-files-under-200-lines**: The target per rule file SHOULD be under 200 lines / ~8KB. If larger, its content SHOULD move to skills or external references.
- **should-inline-small-and-reference-large**: Small content SHOULD be inlined and large content referenced. A 5-line summary table belongs in the rule. A 200-line guideline belongs in an external file read on demand.
- **should-not-duplicate-across-rules**: Rules SHOULD NOT duplicate content across rules.
- **should-use-globs-for-file-specific-rules**: Rules that only apply to specific file patterns SHOULD use `globs` frontmatter (e.g., `globs: .claude/**`).
- **should-deduplicate-must-nots**: MUST NOTs SHOULD be deduplicated. Each item SHOULD add a unique constraint not stated elsewhere in the body.
- **should-avoid-mandatory-multi-file-reads**: Mandatory multi-file reads SHOULD be avoided. You SHOULD prefer summaries, on-demand reads, or iterative approaches.
- **should-inline-mostly-metadata-files**: Frontmatter ratios in referenced files SHOULD be watched. If an external file is >50% YAML metadata, its content SHOULD be inlined instead.

