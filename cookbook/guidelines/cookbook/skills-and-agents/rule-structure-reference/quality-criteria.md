
### Structure
- Clear title/heading identifying the rule's purpose
- Numbered or clearly separated steps if procedural
- Sections with headings for distinct concerns

### Content
- **Imperative tone**: Uses MUST, MUST NOT, SHOULD, MAY (RFC 2119)
- **Deterministic**: The LLM should be able to follow the rule without ambiguity
- **Explicit file references**: If the rule says "read the principles," it lists every file path
- **Self-contained or clearly scoped**: Either contains all needed information or explicitly references where to find it
- **No vague directives**: "Handle errors appropriately" is bad. "Validate user input at the API boundary, return HTTP 400 with a message for invalid input" is good.

### Anti-patterns
- **Vague rules**: "Write good code" — not actionable
- **Contradictory rules**: "Always do X" then later "Never do X"
- **Unbounded scope**: Rule tries to govern everything instead of a specific concern
- **Missing file paths**: Rule says "read the guidelines" without listing which files
- **Duplicating CLAUDE.md**: Rule content that belongs in project instructions, not a standalone rule
- **No enforcement mechanism**: Rule states preferences but provides no steps to verify compliance

