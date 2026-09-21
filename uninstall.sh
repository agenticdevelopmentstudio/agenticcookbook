#!/usr/bin/env bash
# Remove everything install.sh placed on the system.
# - Removes each CLI_SKILLS shim and package
# - Unregisters the local marketplace and disables the plugin
# - Wipes the assembled plugins/adh/skills/ directory
# - Removes any legacy ~/.claude/skills/cookbook/ location
#
# Does NOT uninstall pip-installed deps (rich, questionary, pyyaml) — those may
# be used by other tools.
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
CLI_SKILLS=(cookbook cookr)
LEGACY_SKILL_DIR="${HOME}/.claude/skills/cookbook"
PLUGIN_SKILLS_DIR="${REPO_ROOT}/plugins/adh/skills"
MARKETPLACE_NAME="agenticcookbook"
PLUGIN_NAME="adh"
CLAUDE_DIR="${HOME}/.claude"
KNOWN_MARKETPLACES="${CLAUDE_DIR}/plugins/known_marketplaces.json"
CLAUDE_SETTINGS="${CLAUDE_DIR}/settings.json"

color() { printf '\033[1;%sm%s\033[0m\n' "$1" "$2"; }
title() { printf '\n'; color 36 "› $*"; }
ok()    { color 32 "✓ $*"; }
skip()  { color 90 "· $*"; }

for skill in "${CLI_SKILLS[@]}"; do
    title "Removing ${skill} CLI shim"
    if [ -f "${BIN_DIR}/${skill}" ]; then
        rm -f "${BIN_DIR}/${skill}"
        ok "removed ${BIN_DIR}/${skill}"
    else
        skip "${BIN_DIR}/${skill} (not present)"
    fi

    title "Removing ${skill} package"
    if [ -d "${BIN_DIR}/_${skill}_pkg" ]; then
        rm -rf "${BIN_DIR}/_${skill}_pkg"
        ok "removed ${BIN_DIR}/_${skill}_pkg"
    else
        skip "${BIN_DIR}/_${skill}_pkg (not present)"
    fi
done

title "Unregistering plugin"
if command -v python3 >/dev/null 2>&1; then
    python3 - "$KNOWN_MARKETPLACES" "$CLAUDE_SETTINGS" "$MARKETPLACE_NAME" "$PLUGIN_NAME" <<'PY'
import json, os, sys, tempfile
from pathlib import Path

known_path, settings_path, market_name, plugin_name = sys.argv[1:5]
plugin_id = f"{plugin_name}@{market_name}"

def load(path):
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError as e:
        print(f"  ! {path} is not valid JSON ({e}); leaving unchanged.")
        return None

def atomic_write(path, data):
    p = Path(path)
    fd, tmp = tempfile.mkstemp(prefix=p.name + ".", dir=str(p.parent))
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp, p)
    except Exception:
        try: os.unlink(tmp)
        except FileNotFoundError: pass
        raise

known = load(known_path)
if known is not None and market_name in known:
    del known[market_name]
    atomic_write(known_path, known)
    print(f"  - known_marketplaces.json: removed {market_name}")
else:
    print(f"  . known_marketplaces.json: no {market_name} entry")

settings = load(settings_path)
if settings is not None:
    changed = False
    extra = settings.get("extraKnownMarketplaces")
    if isinstance(extra, dict) and market_name in extra:
        del extra[market_name]
        if not extra:
            del settings["extraKnownMarketplaces"]
        changed = True
        print(f"  - settings.json: removed extraKnownMarketplaces.{market_name}")
    enabled = settings.get("enabledPlugins")
    if isinstance(enabled, dict) and plugin_id in enabled:
        del enabled[plugin_id]
        if not enabled:
            del settings["enabledPlugins"]
        changed = True
        print(f"  - settings.json: disabled {plugin_id}")
    if changed:
        atomic_write(settings_path, settings)
    else:
        print(f"  . settings.json: nothing to change")
PY
    ok "marketplace + plugin entries cleaned"
else
    skip "python3 not on PATH — leaving Claude Code config untouched"
fi

title "Removing assembled plugin skills"
if [ -d "${PLUGIN_SKILLS_DIR}" ]; then
    rm -rf "${PLUGIN_SKILLS_DIR}"
    ok "removed ${PLUGIN_SKILLS_DIR}"
else
    skip "${PLUGIN_SKILLS_DIR} (not present)"
fi

title "Removing legacy skill location"
if [ -d "${LEGACY_SKILL_DIR}" ]; then
    rm -rf "${LEGACY_SKILL_DIR}"
    ok "removed ${LEGACY_SKILL_DIR}"
else
    skip "${LEGACY_SKILL_DIR} (not present)"
fi

title "Done"
ok "rich / questionary / pyyaml were left installed (may be used by other tools)"
