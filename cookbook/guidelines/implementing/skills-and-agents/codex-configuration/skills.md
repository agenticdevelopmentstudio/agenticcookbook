
- A skill is a directory with a `SKILL.md` whose frontmatter has a `name` and a `description`. The description is what Codex uses to decide when the skill applies, so write it as a trigger.
- Skills are discovered in these places: repository skills in `.agents/skills`, scanned from the working directory up to the repository root; user skills in `$HOME/.agents/skills`; administrator skills in `/etc/codex/skills`; and bundled system skills.
- An optional `agents/openai.yaml` in the skill directory sets invocation policy. `allow_implicit_invocation: false` stops Codex from choosing the skill on its own.
- Disable a skill without deleting it with a `[[skills.config]]` entry in `~/.codex/config.toml`, and restart Codex.
- Follow [Skill structure reference](agenticdevelopercookbook://guidelines/implementing/skills-and-agents/skill-structure-reference) for the contents of `SKILL.md`, and [Never overwrite a user's files](agenticdevelopercookbook://guidelines/implementing/skills-and-agents/never-clobber-user-files) when installing one.

