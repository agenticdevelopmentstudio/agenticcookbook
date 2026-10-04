# Agentic Developer Cookbook

A structured cookbook of principles, guidelines, recipes, and workflows for AI-assisted multi-platform development. All content is markdown consumed directly by AI agents.

## Repository Structure

```
cookbook/                # cookbook content root
  introduction/          # getting started, conventions, glossary
  principles/            # engineering principles
  guidelines/            # use-case-organized guidelines
  ingredients/           # atomic component specs (building blocks)
  recipes/               # compositions of ingredients into features
  compliance/            # compliance categories
  workflows/             # workflow specs (plan, implement, verify, review)
  reference/             # external best-practices links, schemas, examples
  appendix/              # research materials
  index.md               # table of contents
README.md                # human-facing documentation
.claude/
  CLAUDE.md              # this file
  rules/                 # repo-specific rules
  skills/                # repo-specific skills
```

## Cookbook Artifacts

A **cookbook artifact** is any content item in the cookbook: a principle, guideline, ingredient, or recipe. Each artifact is a standalone markdown file with YAML frontmatter, named requirements, and a change history. See `cookbook/introduction/glossary.md` for the full definition.

| Type | Count | Path | Description |
|------|-------|------|-------------|
| Principle | 33 | `cookbook/principles/` | Foundational engineering ideas that guide design decisions |
| Guideline | 258 (341 with duplicates) | `cookbook/guidelines/` | Use-case-organized rules: planning, implementing, testing, reviewing, shipping, cookbook, researching |
| Ingredient | 19 | `cookbook/ingredients/` | Atomic component specs — the building blocks of recipes |
| Recipe | 13 | `cookbook/recipes/` | Compositions of configured ingredients into coherent features |

A **cookbook** (`cookbook.json`) assembles recipes and ingredients into a complete application, plugin, or widget. See `cookbook/reference/cookbook.schema.json` for the JSON Schema.

Supporting content (not artifacts): compliance checks, workflows, reference material.

## Sibling Projects

### dev-team

Multi-agent development system, distributed as a Claude Code plugin. Orchestrates teams of specialist agents (13 domain + 6 platform) for product discovery, code generation, and linting. All user-facing cookbook skills live here: `/install-cookbook`, `/configure-cookbook`, `/contribute-to-cookbook`, `/validate-cookbook`, `/cookbook-help`, `/dev-team lint`, and others.

Repo: [agenticdevelopercookbook/dev-team](https://github.com/agenticdevelopercookbook/dev-team)

### agenticcookbookweb (moved to the adh monorepo)

The cookbook's public-facing website (React 19, TypeScript, Tailwind CSS 4) and the `update-website` sync skill have **moved into the `adh` monorepo** at `adh/websites/cookbook/`. The standalone `agenticcookbookweb` repo is deprecated, and this repo no longer ships an `update-website` skill or an automatic website-sync step.

## Conventions

Read `cookbook/introduction/conventions.md` for the full format reference. See `cookbook/introduction/glossary.md` for term definitions.

Key rules:
- All `.md` files have YAML frontmatter (id, title, domain, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references)
- URL-based domain identifiers: `agenticdevelopercookbook://guidelines/testing/test-pyramid`
- Fragment references for within-document sections: `#requirements/ordered-list`
- Named requirements (kebab-case, not REQ-NNN): `**ordered-list**: The control MUST...`
- Version is semver, immutable once on main
- MIT license on all files
- Cross-reference with full URL or short-form `#fragment`

## Git Workflow

**Owner edits** go direct to main. **Claude Code sessions** go through a branch + PR via worktree.

| Change type | Branch pattern | Example |
|---|---|---|
| New content | `feature/<description>` | `feature/auth-guidelines` |
| Content revision | `revise/<description>` | `revise/testing-guidelines` |

### Worktree flow

1. Create a worktree with `EnterWorktree` (Claude Code) or `git worktree add <path> -b <branch>`
2. Do all work in the worktree
3. Update `cookbook/index.md` if adding new content
4. Commit, push, create PR with `gh pr create`
5. Squash merge: `gh pr merge --squash`
6. Clean up: `ExitWorktree action:remove` (Claude Code) or `git worktree remove <path>`
7. Pull main: `git pull`

**Fork-based contributions**: External contributors who don't have push access use a fork. The workflow is the same (worktree, branch, commit, push, PR), but `origin` points to the fork and the PR targets `agenticdevelopercookbook/cookbook` via `--head <user>:<branch>`. The `/contribute-to-cookbook` skill (in dev-team) detects this automatically.

## Writing New Content

Use `cookbook/ingredients/_template.md` for new ingredients and `cookbook/recipes/_template.md` for new recipes. Follow `cookbook/introduction/conventions.md` for the frontmatter format. Every cookbook artifact needs a UUID, domain matching its path, and a Change History section.

**Source folders.** Every principle, guideline, ingredient and recipe is a source folder
(`<name>/artifact.json` plus one `.md` per section), and `<name>.md` beside it is compiled from
the folder. Edit `<name>.md` as usual, then run `cookr convert --update <path>` to fold the edit into the
folder; `cookr validate` fails while a `.md` and its folder disagree.
