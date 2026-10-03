#!/usr/bin/env bash
# Install the cookr skill globally for the current user, without the adh plugin.
#
# - Installs the CLIs the skill drives via the repo's install.sh --no-plugin:
#   ~/.local/bin/cookr and ~/.local/bin/cookbook (cookr imports the cookbook
#   package, and the skill runs `cookbook update/validate/lint/bump`).
# - Copies SKILL.md to ~/.claude/skills/cookr/, so the skill is /cookr in every
#   project.
#
# Idempotent. Re-run to refresh after edits. Reverse with ./uninstall.sh.
set -euo pipefail

SKILL_SRC="$(cd -- "$(dirname -- "$0")/.." && pwd)"
REPO_ROOT="$(cd -- "${SKILL_SRC}/../.." && pwd)"
SKILL_DST="${HOME}/.claude/skills/cookr"

color() { printf '\033[1;%sm%s\033[0m\n' "$1" "$2"; }
title() { printf '\n'; color 36 "› $*"; }
ok()    { color 32 "✓ $*"; }

"${REPO_ROOT}/install.sh" --no-plugin

title "Installing cookr skill"
rm -rf "${SKILL_DST}"
mkdir -p "${SKILL_DST}"
cp "${SKILL_SRC}/SKILL.md" "${SKILL_DST}/SKILL.md"
ok "skill → ${SKILL_DST}"

title "Done"
ok "Run: cookr --help"
ok "Restart your Claude Code session to pick up /cookr."
