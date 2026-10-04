---
name: add-artifact
version: "1.1.0"
description: "Integrate a new or modified cookbook artifact — lint, approve, update indexes, sync documentation and website. Implements the after-adding-an-artifact rule."
argument-hint: "[path-or-name]"
allowed-tools: Read, Glob, Grep, Edit, Write, Bash(rsync *), Bash(wc *), Bash(date *), Bash(cookr *), AskUserQuestion
context: fork
---

# Add Artifact v1.0.0

Post-creation integration for cookbook artifacts. Takes a path to an artifact that already exists and executes the full `after-adding-an-artifact` rule: lint, approve, update indexes, update documentation, sync to website.

## Startup

add-artifact v1.1.0

**Version check**: Read `${CLAUDE_SKILL_DIR}/SKILL.md` from disk and extract the `version:` field from frontmatter. Compare to this skill's version (1.1.0). If they differ, print:

> Warning: This skill is running v1.1.0 but vA.B.C is installed. Restart the session to use the latest version.

Then continue running.

If `$ARGUMENTS` is `--version`, respond with exactly:
> add-artifact v1.1.0

Then stop.

## Argument Resolution

Use the same argument resolution flow as `/lint-artifact`:

1. If `$ARGUMENTS` is a path or ends with `.md`, treat as file path.
2. If `$ARGUMENTS` is a search string, search `cookbook/principles/`, `cookbook/guidelines/`, `cookbook/recipes/` for matching `.md` files.
3. If `$ARGUMENTS` is empty, check session context or prompt the user.

See `/lint-artifact` for the full resolution flow.

## Step 1: Approve

If the artifact has no source folder yet (no `<name>/artifact.json` beside it), run
`cookr convert <path>` first. Then run `/approve-artifact` on the resolved file.

- If approval **fails** (lint has FAIL results), print the lint report and stop. The artifact must be fixed before it can be added.
- If approval **succeeds**, proceed to Step 2.

## Step 2: Update Indexes

### Main index

Read `cookbook/index.md`. Check whether the artifact is listed.

- If the artifact is **new** (not in the index), add an entry in the correct section based on the artifact's path:
  - `cookbook/principles/` artifacts go in the Principles section
  - `cookbook/guidelines/` artifacts go in the Guidelines section (under the correct topic subsection)
  - `cookbook/recipes/` artifacts go in the Recipes section (under the correct category subsection)
- If the artifact is **already listed**, verify the entry is correct (title, path). Update if stale.

### Section-level indexes

Check for `INDEX.md` files in the artifact's parent directory and ancestor directories. Update them if they exist.

Print what was updated:

```
Index updates:
  [UPDATED] cookbook/index.md — added <artifact-title>
  [OK] cookbook/guidelines/testing/INDEX.md — already listed
```

## Step 3: Update Documentation

### Artifact counts

Read `README.md` and `.claude/CLAUDE.md`. Check the artifact counts:

| Type | README pattern | CLAUDE.md pattern |
|------|---------------|-------------------|
| Principle | `Principles (NN files)` or `NN` in the table | Count in Cookbook Artifacts table |
| Guideline | `Guidelines (NN files)` or `NN` in the table | Count in Cookbook Artifacts table |
| Recipe | `Recipes (NN files)` or `NN` in the table | Count in Cookbook Artifacts table |

Count the actual number of artifacts of each type using Glob (excluding `_template.md` and `INDEX.md`). If the counts in README.md or CLAUDE.md are stale, update them.

### Cross-references

If the new artifact is referenced by or references other artifacts (via `depends-on` or `related` fields), verify those references resolve. Print warnings for any that don't.

Print what was updated:

```
Documentation updates:
  [UPDATED] README.md — principle count 18 -> 19
  [UPDATED] .claude/CLAUDE.md — principle count 18 -> 19
  [OK] No broken cross-references
```

## Step 4: Summary

Print:

```
=== ADD ARTIFACT COMPLETE ===
Artifact: <filename>
Type: <type>
Approved: yes (approve-artifact v<version>)
Index updates: <n> files updated
Documentation updates: <n> files updated

All integration steps complete.
```

## Guards

- **Approval required** — never proceed past Step 1 if the artifact fails lint.
- **Accurate counts** — always count actual files, never hardcode or guess artifact counts.
