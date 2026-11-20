
- A skill is a directory with a `SKILL.md` whose frontmatter has a `name` and a `description`.
- Skills are discovered in these places: repository skills in `.agents/skills`, scanned from the working directory up to the repository root; user skills in `$HOME/.agents/skills`; administrator skills in `/etc/codex/skills`; and bundled system skills.
- An optional `agents/openai.yaml` in the skill directory sets invocation policy.

