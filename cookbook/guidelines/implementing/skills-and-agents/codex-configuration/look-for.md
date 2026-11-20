
Review Codex configuration against the rules above.

- `should-put-config-where-codex-looks`, `should-keep-shared-config-in-repo`: Each setting is in the layer that reaches the people who need it: shared settings in `.codex/config.toml`, personal ones in `~/.codex/config.toml`.
- `must-not-depend-on-untrusted-checkout`: a setting that must apply on every machine but loads only from a project's `.codex/config.toml`, which an untrusted checkout never loads.
- `must-check-keys-against-reference`: Every key exists in the configuration reference.
- `must-not-copy-keys-from-other-tools`: a key in `config.toml` that belongs to another tool's configuration.
- `must-not-check-in-secrets`: No secret is checked in.
- `should-write-agents-md-for-any-agent`, `should-keep-agents-md-files-short`: Instructions are agent-neutral and short enough that the combined files stay under `project_doc_max_bytes`.
- `should-move-reference-material-into-skills`: reference material held in `AGENTS.md` that a skill could load on demand.
- `should-not-repeat-parent-in-nested-agents-md`: Nested files add to the parent rather than repeat it.
- `should-give-agents-override-a-reason`: An `AGENTS.override.md` has a reason.
- `should-put-repository-skills-under-agents-skills`: Repository skills live under `.agents/skills`.
- `should-write-skill-description-as-trigger`: `SKILL.md` has a `name` and a trigger-style `description`.
- `should-set-allow-implicit-invocation-false`: `allow_implicit_invocation: false` is set for skills that must run only on request.
- `should-disable-skills-via-skills-config`: a skill deleted, or disabled some other way, where a `[[skills.config]]` entry in `~/.codex/config.toml` would disable it.
- `must-follow-skill-structure-reference`: a `SKILL.md` whose contents depart from the skill structure reference.
- `must-follow-never-clobber-on-install`: a skill install that overwrites a user's files.
- `must-not-write-new-custom-prompts`: No new custom prompt.
- `should-migrate-team-prompts-to-skills`: A prompt the team relies on is converted to a skill.

