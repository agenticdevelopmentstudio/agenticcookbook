
### Content Quality

- **should-have-single-responsibility**: The rule SHOULD address one coherent concern, not a grab-bag of unrelated instructions. (C01, WARN)
- **should-give-actionable-specific-instructions**: Every instruction SHOULD tell the LLM concretely what to do, not give vague directives like "handle errors appropriately". (C07, WARN)
- **must-not-conflict-with-itself**: The rule MUST NOT contradict itself (e.g., "always do X" then later "never do X"). (C08, FAIL)
- **should-use-well-structured-markdown**: The rule SHOULD use headings, lists and code blocks, not a wall of unstructured text. (C09, WARN)

### Best Practices

- **should-not-replicate-native-capabilities**: The rule SHOULD NOT teach Claude things it already knows (basic git, standard coding, etc.). (B02, WARN)
- **must-not-be-kitchen-sink**: The rule MUST NOT try to govern everything; it stays focused on its stated concern. (B06, FAIL)
- **should-not-be-claude-md-dump**: Content SHOULD be rule-appropriate, not project configuration that belongs in CLAUDE.md. (B08, WARN)

### Rule-Specific

- **should-have-clear-title-heading**: The file SHOULD start with a heading that identifies the rule's purpose. (R01, WARN)
- **should-use-imperative-tone**: The rule SHOULD use an imperative tone throughout, with RFC 2119 keywords (`MUST`, `MUST NOT`, `SHOULD`, `MAY`), not advisory or suggestive wording. (R02, WARN)
- **should-number-or-separate-steps**: If the rule is procedural, its steps SHOULD be in a clear sequence with headings or a numbered list. (R03, WARN)
- **must-not-use-vague-directives**: Every instruction MUST be concrete and actionable; no "handle appropriately" or "write good code". (R04, FAIL)
- **must-list-file-references-explicitly**: If the rule says to read files, every file path MUST be listed explicitly; no "read the principles" without paths. (R05, FAIL)
- **must-not-give-contradictory-instructions**: The rule MUST NOT say "always do X" then later "never do X" or otherwise conflict with itself. (R06, FAIL)
- **should-address-single-concern**: The rule SHOULD address one coherent concern (planning, implementing, reviewing), not a grab-bag. (R07, WARN)
- **should-include-enforcement-mechanism**: The rule SHOULD include steps to verify compliance: not just "do X" but "verify X was done". (R08, WARN)
- **should-not-be-claude-md-dump-rule-specific**: Content SHOULD be rule-appropriate, not project configuration that belongs in CLAUDE.md. (R09, WARN)
- **should-have-reasonable-length**: The rule SHOULD be long enough to be complete but not so long it gets ignored: under ~300 lines for a single rule file. (R10, WARN)
- **should-have-must-not-section**: The rule SHOULD have a `MUST NOT` section explicitly stating what the LLM must not do: common mistakes and anti-patterns. (R11, WARN)
- **should-be-deterministic**: The rule SHOULD be unambiguous: an LLM following it would produce consistent behavior across sessions, with no room for interpretation on critical steps. (R12, WARN)
- **should-use-lowercase-kebab-case-filename**: The filename SHOULD be lowercase kebab-case, matching `^[a-z][a-z0-9-]*\.md$` (e.g., `testing.md`, `api-design.md`); UPPERCASE stems are reserved for identity files like `SKILL.md` and `CLAUDE.md`. (R13, WARN)

### Optimization

- **should-stay-under-200-lines-8kb**: The rule file SHOULD be under 200 lines / ~8KB; larger rules should move content to on-demand skills or external references. (O01, WARN)
- **should-not-duplicate-another-rule**: The rule SHOULD NOT duplicate content from another `.md` file in the same `.claude/rules/` directory; overlapping instructions are processed twice per turn. (O02, WARN)
- **should-have-globs-when-scoped**: If the rule only applies to specific file patterns (e.g., `.claude/**`, `site/**`), it SHOULD have `globs` frontmatter to prevent loading on unrelated work. (O03, WARN)
- **should-keep-must-not-items-unique**: Each `MUST NOT` item SHOULD add a constraint not already expressed imperatively in the body text. (O04, WARN)
- **may-inline-low-ratio-external-refs**: If an external file reference points to a file where frontmatter exceeds 50% of total lines, the review MAY suggest inlining the useful content instead. (O05, INFO)
- **should-limit-unconditional-external-reads**: The rule SHOULD mandate no more than 5 unconditional external reads before any work; 6+ create high entry cost. (O06, WARN)
