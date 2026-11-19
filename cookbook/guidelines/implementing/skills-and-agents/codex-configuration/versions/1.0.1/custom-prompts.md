
- Custom prompts are deprecated in favor of skills. You MUST NOT write new ones unless a skill cannot express the need.
- Existing prompts are Markdown files directly in `~/.codex/prompts/` (subdirectories are not scanned). They are per-user, so they cannot be shared through the repository. Frontmatter supports `description` and `argument-hint`, and a prompt runs as `/prompts:<name>`.
- A prompt that the team uses SHOULD be migrated to a repository skill so it is versioned with the code.

