
- A skill is a directory with a `SKILL.md` whose frontmatter has a `name` and a `description`. The description is what Codex uses to decide when the skill applies, so it SHOULD be written as a trigger.
- Skills are discovered in these places: repository skills in `.agents/skills`, scanned from the working directory up to the repository root; user skills in `$HOME/.agents/skills`; administrator skills in `/etc/codex/skills`; and bundled system skills.
- An optional `agents/openai.yaml` in the skill directory sets invocation policy. `allow_implicit_invocation: false` stops Codex from choosing the skill on its own; a skill meant to run only on request SHOULD set it.
- Disable a skill without deleting it with a `[[skills.config]]` entry in `~/.codex/config.toml`, and restart Codex.
- Skills MUST follow Skill structure reference ([adc.guideline.implementing.skills-and-agents.skill-structure-reference](cookbook:fe0daac0-1ba7-4c93-a47e-e42e75612cf6)) for the contents of `SKILL.md`, and installing one MUST follow Never overwrite a user's files ([adc.guideline.implementing.skills-and-agents.never-clobber-user-files](cookbook:5358bc26-ea8f-4dd0-94d1-22dc1c6ad291)).

