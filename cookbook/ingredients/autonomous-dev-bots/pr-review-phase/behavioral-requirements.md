
- **structural-validation**: Phase 1 MUST run all applicable checks from `/validate-cookbook` (frontmatter integrity, content structure, cross-references, indexes, file placement).
- **markdownlint**: Phase 1 MUST run markdownlint-cli2 and auto-fix fixable issues.
- **vale-cookbook-style**: Phase 1 MUST run Vale with the custom Cookbook style checking for: vague terms, ambiguous quantifiers, hedging, implicit references, casual RFC 2119 keywords, double negatives, ambiguous pronouns.
- **llm-clarity-pass**: Phase 1 MUST run an LLM-based clarity analysis checking for: ambiguous antecedents, implicit assumptions, terminology inconsistency across sections, self-containment of sections, unresolved references.
- **content-completeness**: Phase 1 MUST verify all required sections are present and non-empty (or explicitly N/A with reason), MUST requirements have test vectors, appearance values are concrete, logging messages are exact strings, platform notes cover all declared platforms.
- **convention-compliance**: Phase 1 MUST verify named requirements use kebab-case, RFC 2119 keywords are used correctly, domain identifiers match file paths, template variables are used where appropriate.
- **fix-loop**: Phase 1 MUST attempt to fix issues in a loop, max 3 iterations. Each iteration: fix auto-fixable issues (markdownlint, frontmatter), attempt LLM fixes (prose rewrites, inferrable values), re-validate. After 3 iterations, remaining issues are flagged as unfixable.
- **fix-categorization**: Each issue MUST be categorized as: auto-fixable (deterministic tool fix), LLM-fixable (LLM can infer the correction), or human-required (needs contributor or reviewer decision).

