
| ID  | Criterion | How to check | Severity |
|-----|-----------|-------------|----------|
| S01 | YAML frontmatter present | File starts with `---`, has closing `---` | FAIL |
| S02 | `name` field present | Frontmatter contains `name:` | WARN |
| S03 | `name` is kebab-case, lowercase, ≤64 chars | Regex: `^[a-z][a-z0-9-]{0,63}$` | FAIL |
| S04 | `description` field present | Frontmatter contains `description:` | FAIL |
| S05 | Description uses natural trigger keywords | Description includes phrases users would say; not too vague ("does stuff") or too narrow ("only for X on Tuesdays") | WARN |
| S06 | SKILL.md ≤ 500 lines | `wc -l SKILL.md` | WARN |
| S07 | Supporting files in subdirectories | Loose files (non-SKILL.md) at skill root → should be in references/, scripts/, examples/ | WARN |
| S08 | SKILL.md references its supporting files | If references/ exists, SKILL.md mentions those files or uses `${CLAUDE_SKILL_DIR}` to load them | WARN |
| S09 | Directory name matches `name` field | Compare directory basename to frontmatter `name` | WARN |
| S10 | `argument-hint` present if `$ARGUMENTS` used | SKILL.md uses `$ARGUMENTS` or `$1`, `$2` but frontmatter lacks `argument-hint:` | WARN |
| S11 | Correct file location | Skill is in `.claude/skills/` or `~/.claude/skills/` | WARN |
| S12 | Only recognized frontmatter fields | Check against known fields: name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model, effort, context, agent, hooks, paths, shell | WARN |
| S13 | Main file named `SKILL.md` (uppercase stem) | Filename is exactly `SKILL.md`, not `skill.md` or `Skill.md` — Claude Code looks for this exact name | FAIL |
| S14 | Supporting files use lowercase descriptive names | Files in references/, scripts/, examples/ match `^[a-z][a-z0-9-]*(\.[a-z]+)+$`; names describe content (not `doc1.md`) | WARN |

---

