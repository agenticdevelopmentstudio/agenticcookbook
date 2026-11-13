# Session: concise compiled skills, skill-router 0.6/0.7, and recompiling every skill set

- **Date:** 2026-11-13
- **Session:** `8f2233df-4273-407c-8377-e02b8527be2a`
- **Branch:** `skill-based-cookbook` (merged as PR #78), `docs-update-hurly`

## Orientation

The session took the `skill-based-cookbook` branch from a rebase through to merge. Along the way it
taught skill-router about platforms (0.6.0) and progressive disclosure (0.7.0), made cookr's compiled
skills concise with linked `references/`, removed a duplicate `cookr skills build` path and the
unused `rules.py`, and fixed `cookr validate` on a fresh checkout. PR #78 is merged, skill-router is
merged and installed, cookr 0.13.1 is installed, and all three routed sets (`adc`, `adhsdk`,
`cookbook`) are recompiled and registered. The state is recorded in
[STATUS](../project/STATUS.md#concise-compiled-skills-and-the-recompile-pr-78-2026-11-13).

## Decisions

- **Progressive disclosure in compiled skills.** SKILL.md has to be enough to do the task, so it
  keeps the rules, edge cases and accessibility. Rationale moves to `references/`, linked under
  `## More` with a line saying when to read each file. History is dropped. *Why:* skills were too
  long to load cheaply. On adhsdk the median went from 214 to 139 lines, and skills over 500 lines
  went from 75 to 12.
- **Platforms ride in `metadata.platforms`**, and skill-router 0.6.0 filters on them. A malformed
  (mapping) value is rejected rather than coerced, which needed the frontmatter parser fix in
  skill-router `cb1207a`.
- **Reviewing and implementing stay separate routing pathways.** The user confirmed this; nothing
  merges them.
- **The triggers index is committed** (`63522f3f`). It is deterministic, and gitignoring it made
  `cookr validate` fail on a fresh checkout. It is cheaper to commit it than to make validate
  regenerate it.
- **`--library cookbook` must beat the rdid** (cookr 0.13.1, `52df843b`). The parser had collapsed
  the literal default to None, so the rdid fallback won and the unprefixed set could not be rebuilt.
  The fix keeps the parsed value as given and lets the Installer normalize it.
- **Squash mode for PR #78 was `squash`.** squashr left three logical commits (summaries, feature,
  triggers index).

## Considered and rejected

- **`cookr skills build`, which generated routed rule-skill plugins.** It was built on the branch and
  removed before merge, because skill-router already routes skills and the command duplicated it.
- **A skill manifest.** It was removed, for the same duplication reason.
- **Shrinking long skills in the compiler.** The 12 adhsdk skills over 500 lines are long because of
  their Behavioral Requirements, which is core content. Moving it to references would break the
  "SKILL.md is enough on its own" rule, so the fix is splitting those artifacts in adhsdk.

## Research / findings

- Skills over 500 lines on 2026-11-13: 12 of 1678 routed skills, all adhsdk. The longest is
  hierarchical-topic-detail at 856. Nine skills installed directly in `~/.claude/skills` are over
  500 lines (slack-bot 1234, humanize 1093, webinitor 1057, feishu-lark 959, ship 887, discord-bot
  703, telegram-bot 663, release 548, extract-to-new-repo 518), plus three in `~/.codex/skills`.
  None of them comes from a cookbook.
- The `adc` and `cookbook` routed sets are the same 486 artifacts: `adc` is prefixed and scoped to
  adhsdk, and `cookbook` is unprefixed and routed everywhere.

## Open threads

- **Whether the duplicate `cookbook` set should keep existing beside `adc`.** The user has not ruled
  on it.
- **Splitting the 12 long adhsdk artifacts.** This is adhsdk's content and happens in that repo.
- **The always-on `general-principles` receipt** still names the old `adh/agenticcookbook` path
  (hand-edited skill, not overwritten).

## Pointers

- [STATUS](../project/STATUS.md) is the resume point.
- PR #78: `48d460aa`, `40c02a7f`, `63522f3f`. Fix: `52df843b`.
- skill-router main: `a7a9177`, `262439a`, `cb1207a`.
- Code: `skills/cookr/cli/cookr/core/skill.py`, `skills/cookr/cli/cookr/modules/install.py`, and
  skill-router's `src/skill_router/core/skill_meta.py`.
