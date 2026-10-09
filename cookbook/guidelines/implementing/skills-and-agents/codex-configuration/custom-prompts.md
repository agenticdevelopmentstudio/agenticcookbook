
- Custom prompts are deprecated in favor of skills. Do not write new ones unless a skill cannot express the need.
- Existing prompts are Markdown files directly in `~/.codex/prompts/` (subdirectories are not scanned). They are per-user, so they cannot be shared through the repository. Frontmatter supports `description` and `argument-hint`, and a prompt runs as `/prompts:<name>`.
- Migrate a prompt that the team uses to a repository skill so it is versioned with the code.

