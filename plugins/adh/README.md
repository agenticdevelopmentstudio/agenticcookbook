# adh plugin

Claude Code plugin shell for the Agentic Developer Hub.

## Layout

```
plugins/adh/
  .claude-plugin/
    plugin.json    # plugin metadata
  skills/          # assembled at install time from ../../skills/ (gitignored)
```

## How it ships

The repo root contains `.claude-plugin/marketplace.json`, which registers this
plugin under the `agenticcookbook` local directory marketplace.

`./install` from the repo root:
1. Assembles `plugins/adh/skills/` by copying every directory under
   `../../skills/` into it, except standalone skills: those with their own
   `skills/<name>/setup/install` (e.g. `cookr`), which install themselves to
   `~/.claude/skills/<name>/` instead.
2. Registers the marketplace with Claude Code and enables the plugin.

Each skill ships as a plugin-namespaced skill: invokable by Claude via the
`Skill` tool as `adh:<name>` and by the user as the `/adh:<name>` slash
command.

## Adding a skill

1. Create `./skills/<name>/SKILL.md` at the repo root with YAML frontmatter.
2. Re-run `./install` (or `cookbook self update`) — it gets picked up
   automatically.
