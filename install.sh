#!/usr/bin/env bash
# Install every CLI skill (skills/<name>/{bin,cli}/<name>) and the Claude Code plugin globally for the current user.
#
# - Materializes skills/cookbook/cli/references/ from reference-manifest.json
#   (bundles cookbook content into the script so it's self-contained at runtime).
# - Copies each CLI skill's Python package to ~/.local/bin/_<name>_pkg/ and
#   writes a shim at ~/.local/bin/<name>
# - Assembles ./plugins/adh/skills/ from ./skills/ (every top-level
#   skill directory becomes a plugin-namespaced skill: invokable by Claude
#   via the Skill tool as adh:<name> and by the user as /adh:<name>).
# - Registers the repo as a local directory marketplace ("agenticcookbook")
#   with Claude Code and enables the adh plugin.
# - Installs any missing Python deps (rich, questionary, pyyaml), falling
#   back to --break-system-packages on PEP 668 externally-managed pythons
#
# Idempotent. Re-run to refresh after edits.
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
LEGACY_SKILL_DIR="${HOME}/.claude/skills/cookbook"
PLUGIN_DIR="${REPO_ROOT}/plugins/adh"
PLUGIN_SKILLS_DIR="${PLUGIN_DIR}/skills"
SKILLS_SRC="${REPO_ROOT}/skills"
MARKETPLACE_NAME="agenticcookbook"
PLUGIN_NAME="adh"
CLAUDE_DIR="${HOME}/.claude"
KNOWN_MARKETPLACES="${CLAUDE_DIR}/plugins/known_marketplaces.json"
CLAUDE_SETTINGS="${CLAUDE_DIR}/settings.json"
MANIFEST="${REPO_ROOT}/skills/cookbook/cli/reference-manifest.json"
# Skills that carry a CLI: each ships as ~/.local/bin/<name> + ~/.local/bin/_<name>_pkg
# and has its cli/ and bin/ kept out of the plugin bundle. The layout is the one
# table: a skill carries a CLI when it has skills/<name>/bin/<name> and a
# skills/<name>/cli/<name>/ package. uninstall.sh reads the same layout, plus the
# record written below of what was actually installed.
CLI_SKILLS=()
for bin in "${SKILLS_SRC}"/*/bin/*; do
    skill="$(basename -- "$(dirname -- "$(dirname -- "${bin}")")")"
    if [ "$(basename -- "${bin}")" = "${skill}" ] && [ -d "${SKILLS_SRC}/${skill}/cli/${skill}" ]; then
        CLI_SKILLS+=("${skill}")
    fi
done
CLI_RECORD="${BIN_DIR}/.adh-cli-skills"

color() { printf '\033[1;%sm%s\033[0m\n' "$1" "$2"; }
title() { printf '\n'; color 36 "› $*"; }
ok()    { color 32 "✓ $*"; }
warn()  { color 33 "! $*"; }
err()   { color 31 "✗ $*" >&2; }

# 1. Python ≥ 3.9
title "Checking Python"
if ! command -v python3 >/dev/null 2>&1; then
    err "python3 not found on PATH. Install Python 3.9+ and retry."
    exit 1
fi
python3 - <<'PY' || { err "Python 3.9+ required."; exit 1; }
import sys
sys.exit(0 if sys.version_info >= (3, 9) else 1)
PY
ok "$(python3 --version)"

# 2. Ensure ~/.local/bin exists and warn if not on PATH
mkdir -p "${BIN_DIR}"
case ":${PATH}:" in
    *":${BIN_DIR}:"*) ;;
    *) warn "${BIN_DIR} is not on \$PATH. Add it to your shell profile." ;;
esac

# 3. Materialize references/ from manifest (cookbook.core.manifest, stdlib only)
title "Materializing references"
PYTHONPATH="${REPO_ROOT}/skills/cookbook/cli" python3 -m cookbook.core.manifest "$REPO_ROOT" "$MANIFEST"
ok "references materialized"

# 3b. Materialize each prompt-module's reference-manifest.json
title "Materializing prompt-module references"
PYTHONPATH="${REPO_ROOT}/skills/cookbook/cli" python3 -m cookbook.core.manifest "$REPO_ROOT" --prompts "${CLI_SKILLS[@]}"
ok "prompt-module references materialized"

# 4 + 5. Install each CLI skill's package and shim
for skill in "${CLI_SKILLS[@]}"; do
    pkg_src="${REPO_ROOT}/skills/${skill}/cli"
    pkg_dir="${BIN_DIR}/_${skill}_pkg"
    title "Installing ${skill} package"
    rm -rf "${pkg_dir}"
    mkdir -p "${pkg_dir}"
    cp -R "${pkg_src}/${skill}" "${pkg_dir}/"
    if [ -d "${pkg_src}/references" ]; then
        cp -R "${pkg_src}/references" "${pkg_dir}/"
    fi
    if [ -f "${pkg_src}/reference-manifest.json" ]; then
        cp "${pkg_src}/reference-manifest.json" "${pkg_dir}/"
    fi
    # Stamp the source path so `cookbook self update` (modules/selfcmd.py, the
    # stamp's only reader) can re-run install.sh from here.
    if [ "${skill}" = "cookbook" ]; then
        printf '%s\n' "${REPO_ROOT}" > "${pkg_dir}/.install_source"
    fi
    ok "package → ${pkg_dir}"

    title "Installing ${skill} shim"
    cp "${REPO_ROOT}/skills/${skill}/bin/${skill}" "${BIN_DIR}/${skill}"
    chmod +x "${BIN_DIR}/${skill}"
    ok "shim → ${BIN_DIR}/${skill}"
done
# Record what was installed, so uninstall.sh also removes a skill that has
# since left the layout.
printf '%s\n' "${CLI_SKILLS[@]}" > "${CLI_RECORD}"

# 6. Install Python deps (user-level)
#
# The shim runs `python3 -m cookbook`, so the deps must be importable by
# whichever python3 is on PATH. Note pyyaml imports as `yaml`.
#
# Homebrew/Debian pythons are PEP 668 "externally managed" and refuse
# `pip install --user` outright, so a plain failure here is expected on a
# stock macOS dev box rather than exceptional -- retry with
# --break-system-packages, which is what --user was meant to do anyway.
title "Installing Python deps"
missing_deps() {
    python3 - <<'PYEOF'
import importlib.util, sys
pkgs = {"rich": "rich", "questionary": "questionary", "yaml": "pyyaml"}
print(" ".join(dist for mod, dist in pkgs.items()
                if importlib.util.find_spec(mod) is None))
PYEOF
}

DEPS="$(missing_deps)"
if [ -z "${DEPS}" ]; then
    ok "rich, questionary, pyyaml already present"
else
    pip_ok=0
    if python3 -m pip install --user --upgrade --quiet ${DEPS} 2>/dev/null; then
        pip_ok=1
    elif python3 -m pip install --user --upgrade --quiet --break-system-packages ${DEPS} 2>/dev/null; then
        pip_ok=1
        warn "python3 is externally managed (PEP 668); installed with --break-system-packages"
    fi

    STILL_MISSING="$(missing_deps)"
    if [ -z "${STILL_MISSING}" ]; then
        ok "${DEPS} installed"
    else
        [ "${pip_ok}" -eq 1 ] && warn "pip reported success but ${STILL_MISSING} is still not importable."
        warn "Could not install: ${STILL_MISSING}. Modules that need these will surface a clean error."
        warn "Retry manually:  python3 -m pip install --user --break-system-packages ${STILL_MISSING}"
        warn "  or with pipx:  brew install pipx && pipx install ${STILL_MISSING}"
    fi
fi

# 7. Assemble the plugin: copy ./skills/<name>/ → ./plugins/adh/skills/<name>/
title "Assembling plugin"
if [ ! -d "${SKILLS_SRC}" ]; then
    err "missing ${SKILLS_SRC} — nothing to assemble."
    exit 1
fi
rm -rf "${PLUGIN_SKILLS_DIR}"
mkdir -p "${PLUGIN_SKILLS_DIR}"
python3 - "$SKILLS_SRC" "$PLUGIN_SKILLS_DIR" "${CLI_SKILLS[*]}" <<'PY'
import shutil, sys
from pathlib import Path

# Per-skill excludes: keep CLI plumbing out of plugin-bundled skills so a
# stray `cli/` or `bin/` directory in another skill ships normally.
CLI_SKILLS = set(sys.argv[3].split())
EXCLUDE_PER_SKILL = {name: {"cli", "bin"} for name in CLI_SKILLS}

src_root = Path(sys.argv[1])
dst_root = Path(sys.argv[2])

assembled = 0
for skill_src in sorted(src_root.iterdir()):
    if not skill_src.is_dir():
        continue
    name = skill_src.name
    exclude = EXCLUDE_PER_SKILL.get(name, set())
    skill_dst = dst_root / name
    skill_dst.mkdir(parents=True, exist_ok=True)
    for child in skill_src.iterdir():
        if child.name in exclude:
            continue
        target = skill_dst / child.name
        if child.is_dir():
            shutil.copytree(child, target, symlinks=True)
        else:
            shutil.copy2(child, target)
    print(f"  + {name}")
    assembled += 1
print(f"  assembled {assembled} skill(s)")
if assembled == 0:
    print("  ! no skills assembled — check that ./skills/ contains skill directories.",
          file=sys.stderr)
    sys.exit(1)
PY

# 8. Register the marketplace + enable the plugin
title "Registering Claude Code plugin"
mkdir -p "$(dirname "${KNOWN_MARKETPLACES}")"
python3 - "$REPO_ROOT" "$KNOWN_MARKETPLACES" "$CLAUDE_SETTINGS" "$MARKETPLACE_NAME" "$PLUGIN_NAME" <<'PY'
import json, os, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

repo_root, known_path, settings_path, market_name, plugin_name = sys.argv[1:6]
repo_root = str(Path(repo_root).resolve())
plugin_id = f"{plugin_name}@{market_name}"

def load(path):
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  ! {path} is not valid JSON ({e}); refusing to overwrite.", file=sys.stderr)
        sys.exit(1)

def atomic_write(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=p.name + ".", dir=str(p.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp, p)
    except Exception:
        try: os.unlink(tmp)
        except FileNotFoundError: pass
        raise

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

# known_marketplaces.json: register / refresh the directory marketplace.
known = load(known_path)
known[market_name] = {
    "source": {"source": "directory", "path": repo_root},
    "installLocation": repo_root,
    "lastUpdated": now,
}
atomic_write(known_path, known)
print(f"  + known_marketplaces.json: {market_name} → {repo_root}")

# settings.json: persist marketplace in extraKnownMarketplaces + enable plugin.
settings = load(settings_path)
extra = settings.setdefault("extraKnownMarketplaces", {})
extra[market_name] = {"source": {"source": "directory", "path": repo_root}}
enabled = settings.setdefault("enabledPlugins", {})
enabled[plugin_id] = True
atomic_write(settings_path, settings)
print(f"  + settings.json: enabled {plugin_id}")
PY
ok "marketplace ${MARKETPLACE_NAME} registered; plugin ${PLUGIN_NAME} enabled"

# 9. Clean up legacy ~/.claude/skills/cookbook (now provided by the plugin)
if [ -d "${LEGACY_SKILL_DIR}" ]; then
    title "Cleaning up legacy skill location"
    rm -rf "${LEGACY_SKILL_DIR}"
    ok "removed ${LEGACY_SKILL_DIR} (now provided by the plugin)"
fi

# 10. Verify
title "Verifying"
for skill in "${CLI_SKILLS[@]}"; do
    if "${BIN_DIR}/${skill}" --version >/dev/null 2>&1; then
        ok "$("${BIN_DIR}/${skill}" --version)"
    else
        warn "${skill} --version did not return cleanly. Check the install log above."
    fi
done
if [ -f "${PLUGIN_DIR}/.claude-plugin/plugin.json" ]; then
    ok "plugin manifest at ${PLUGIN_DIR}/.claude-plugin/plugin.json"
else
    err "plugin manifest missing — install did not complete cleanly."
    exit 1
fi

title "Done"
ok "Run: cookbook --help"
ok "Skills available as /adh:<name> (and Skill-tool 'adh:<name>')"
warn "If you just added ${BIN_DIR} to your PATH, open a new shell."
warn "Restart your Claude Code session to pick up the plugin."
