
- Put narrower guidance in `.github/instructions/NAME.instructions.md`. Its frontmatter has an `applyTo` glob (several globs are comma-separated) that selects the files it covers.
- Add `excludeAgent: "code-review"` or `excludeAgent: "cloud-agent"` to keep a file away from one of those agents. Without it both use the file.
- Path-specific and repository-wide files are both applied when a file matches, so do not repeat repository-wide rules in a path file.

