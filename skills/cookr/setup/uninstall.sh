#!/usr/bin/env bash
# Remove what ./install.sh placed for cookr.
# - Removes the ~/.claude/skills/cookr/ skill
# - Removes the cookr CLI shim and package from ~/.local/bin
#
# Leaves the cookbook CLI installed: it is shared with the cookbook skill and
# the adh plugin. The repo's root uninstall.sh removes it. Also leaves the
# pip-installed deps (rich, questionary, pyyaml), which other tools may use.
set -euo pipefail

BIN_DIR="${HOME}/.local/bin"
SKILL_DST="${HOME}/.claude/skills/cookr"

color() { printf '\033[1;%sm%s\033[0m\n' "$1" "$2"; }
title() { printf '\n'; color 36 "› $*"; }
ok()    { color 32 "✓ $*"; }
skip()  { color 90 "· $*"; }

remove() {
    if [ -e "$1" ]; then
        rm -rf "$1"
        ok "removed $1"
    else
        skip "$1 (not present)"
    fi
}

title "Removing cookr skill"
remove "${SKILL_DST}"

title "Removing cookr CLI"
remove "${BIN_DIR}/cookr"
remove "${BIN_DIR}/_cookr_pkg"

title "Done"
ok "cookbook CLI and Python deps left installed (shared; the repo's uninstall.sh removes the CLI)"
