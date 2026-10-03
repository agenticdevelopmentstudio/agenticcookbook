---
name: cookbook
version: "1.1.0"
description: "Create and maintain a cookbook (recipes, reference, indexes). Wraps the `cookbook` CLI installed at ~/.local/bin/cookbook. Use when the user asks to create, update, lint, validate, plan, or self-update a cookbook-shaped repo."
argument-hint: "[--help] [-p <path>] <create|update|lint|validate|plan|self> [...]"
allowed-tools: Bash(cookbook *), Bash(command -v cookbook), Bash(pre-commit *)
model: sonnet
---

# Cookbook v1.1.0

Thin wrapper around the `cookbook` CLI at `~/.local/bin/cookbook`. All work goes
through the CLI — never duplicate its logic in this skill.

## Startup

Verify the CLI is installed before doing anything else:

```bash
command -v cookbook
```

If it is missing, tell the user:

> The `cookbook` CLI is not installed. Run `./install` from the agenticcookbook repo to install it, then re-invoke me.

…and stop.

## Routing

- **No args / `help` / `--help`** → run `cookbook --help` and present the module table verbatim.
- **`<module> ...`** → run `cookbook <module> ...` (forwarding all flags including `-p` / `--path`).
- **`prompt <module> <action> ...`** → run `cookbook prompt <module> <action> ...`
  and treat the printed prompt as your working brief for this turn. The
  CLI does not call an LLM; it emits the assembled prompt for you to act
  on.
- For interactive modules (`plan`, occasionally `update --author`) — let the CLI handle the prompts. Do not wrap them.

## Modules at a glance

| Module | What it does |
|--------|--------------|
| `create` | Scaffolds a new client cookbook in cwd (`cookbook/`, `index.md`, `description.md`, `recipes/`, `reference/`). Idempotent. |
| `update` | Fills missing frontmatter and regenerates indexes. Deterministic; no LLM. |
| `lint` | Phase A deterministic checks + Phase B `claude -p` quality pass. `--no-llm` skips Phase B. `--since <ref>` scopes Phase B to git-changed files. |
| `validate` | Read-only: Phase A checks + index drift detection. Exit non-zero on failure (CI-friendly). |
| `plan` | Drafts a plan for a new recipe or small project via `claude -p`. `--goal "..."` skips the interactive prompt. |
| `self` | `cookbook self update` re-runs `./install` from the source path stamped at install time. |
| `prompt` | Assembles an expert prompt (role + module preamble + bundled cookbook references + action template + free-text task) and prints it to stdout. `prompt <module> <action> [--formal-flags ...] [task ...]`. |

## Interpreting failures

`validate` and `lint --no-llm` print an issue table with columns
`file | rule | issue | fix`. The `fix` column is the authoritative
suggestion — quote it verbatim or paraphrase tightly. The most common cases:

- **`required-field:...`, `frontmatter-present`** → run `cookbook update -p <root> --author "<user>"`.
- **`drift` / `missing` (validate only)** → run `cookbook update -p <root>`.
- **`link-resolves`, `domain-matches-path`** → manual fix on the offending file; the issue cell names the bad value.

When a mutating fix is available (above), offer to run it as the next step.
Do not re-walk the directory after `update` — read the printed summary table.

## Workflow recipes

**New recipe end-to-end**:
```
cookbook plan --goal "<one-line goal>"        # drafts a plan
# user edits cookbook/recipes/<name>.md
cookbook update -p cookbook --author <user>   # fills frontmatter, regenerates indexes
cookbook validate -p cookbook                 # confirm green
cookbook lint -p cookbook                     # optional LLM quality pass
```

**CI-style local check (no LLM)**:
```
cookbook validate -p cookbook
cookbook lint -p cookbook --no-llm
```

**Pre-PR review of just-changed files**:
```
cookbook lint -p cookbook --since main
```

## Behavior notes

- Never `pip install` anything from inside this skill — `./install` handles deps.
- Never edit files in `~/.local/bin/_cookbook_pkg/`. To change CLI behavior, edit the source under `skills/cookbook/cli/` in the agenticcookbook repo and run `cookbook self update` (or re-run `./install`).
- Pass `cwd` as-is; only use `-p <path>` when the user explicitly supplies one.
- `cookbook --version` reports the installed version. If it doesn't match the source the user is editing, run `cookbook self update`.
