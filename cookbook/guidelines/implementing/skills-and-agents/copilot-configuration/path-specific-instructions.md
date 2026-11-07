
- Narrower guidance SHOULD go in `.github/instructions/NAME.instructions.md`. Its frontmatter has an `applyTo` glob (several globs are comma-separated) that selects the files it covers.
- A file MAY add `excludeAgent: "code-review"` or `excludeAgent: "cloud-agent"` to keep a file away from one of those agents. Without it both use the file.
- Path-specific and repository-wide files are both applied when a file matches, so a path file MUST NOT repeat repository-wide rules.

