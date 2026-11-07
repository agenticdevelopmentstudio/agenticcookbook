
- A reusable task is a `.github/prompts/NAME.prompt.md` file. Frontmatter keys are `description`, `agent`, `model`, `tools`, `name` and `argument-hint`. The key for the agent MUST be `agent`, not the older `mode`.
- In the body, a prompt SHOULD use `${input:name}` or `${input:name:placeholder}` for values the user supplies and `${selection}` for the selected text.
- Run a prompt with `/<name>` in chat or with the Chat: Run Prompt command.
- A prompt file MUST NOT take the name of a user's own prompt. See [Never overwrite a user's files](agenticdevelopercookbook://guidelines/implementing/skills-and-agents/never-clobber-user-files).

