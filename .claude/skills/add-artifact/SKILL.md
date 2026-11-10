---
name: add-artifact
version: "2.0.0"
description: "Integrate a new or modified cookbook artifact — lint, approve, update the index and indexes, sync documentation. Implements the after-adding-an-artifact rule."
argument-hint: "[path-or-name]"
allowed-tools: Read, Glob, Grep, Edit, Write, Bash(rsync *), Bash(wc *), Bash(date *), Bash(cookr *), AskUserQuestion
context: fork
---

# Add Artifact v2.0.0

Post-creation integration for cookbook artifacts. Takes a path to an artifact that already exists and executes the full `after-adding-an-artifact` rule: lint, approve, update the cookbook index and INDEX pages, update documentation.

## Startup

add-artifact v2.0.0

**Version check**: Read `${CLAUDE_SKILL_DIR}/SKILL.md` from disk and extract the `version:` field from frontmatter. Compare to this skill's version (2.0.0). If they differ, print:

> Warning: This skill is running v2.0.0 but vA.B.C is installed. Restart the session to use the latest version.

Then continue running.

If `$ARGUMENTS` is `--version`, respond with exactly:
> add-artifact v2.0.0

Then stop.

## Argument Resolution

Use the same argument resolution flow as `/lint-artifact`:

1. If `$ARGUMENTS` is a path (a source folder, or a `.md` not yet converted), use it.
2. If `$ARGUMENTS` is a UUID or rdid, resolve it with `cookr id <arg>`, which prints the folder path.
3. If `$ARGUMENTS` is a search string, search `cookbook/principles/`, `cookbook/guidelines/`, `cookbook/ingredients/`, `cookbook/recipes/` for matching source folders (`<name>/artifact.json`).
4. If `$ARGUMENTS` is empty, check session context or prompt the user.

See `/lint-artifact` for the full resolution flow.

## Step 1: Approve

If the artifact has no source folder yet (a `<name>.md` with no `<name>/artifact.json`), run
`cookr convert <path>` first, then delete the `.md`: the folder is the only committed form.
Then run `/approve-artifact` on the resolved folder.

- If approval **fails** (lint has FAIL results), print the lint report and stop. The artifact must be fixed before it can be added.
- If approval **succeeds**, proceed to Step 2.

## Step 2: Update Indexes

### Cookbook index

Run `cookr update`. It adds or moves the artifact's entry in `cookbook/index.json` (UUID, rdid,
path), stores any rdids written in `depends-on`, `related` and `ingredients` as UUIDs, and
regenerates the generated INDEX pages. Never edit `index.json` by hand. Print the artifact's
rdid with `cookr id <uuid>`.

### Main index

Read `cookbook/index.md`. Check whether the artifact is listed.

- If the artifact is **new** (not in the index), add an entry in the correct section based on the artifact's path:
  - `cookbook/principles/` artifacts go in the Principles section
  - `cookbook/guidelines/` artifacts go in the Guidelines section (under the correct topic subsection)
  - `cookbook/recipes/` artifacts go in the Recipes section (under the correct category subsection)
- If the artifact is **already listed**, verify the entry is correct (title, path). Update if stale.
- Entries link the source folder (`principles/simplicity/`), never a compiled `.md`.

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

Count the actual number of artifacts of each type: the entries of each `kind` in `cookbook/index.json`, which match the source folders (`<name>/artifact.json`) under each type directory. If the counts in README.md or CLAUDE.md are stale, update them.

### Cross-references

Run `cookr validate`. It fails on any link (`depends-on`, `related`, `ingredients`, or an in-text `[<rdid>](cookbook:<uuid>)`) that does not resolve in the index, and on index drift. Fix every failure before continuing.

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
Artifact: <rdid> (<folder>/)
Type: <type>
Approved: yes (approve-artifact v<version>)
Index updates: <n> files updated
Documentation updates: <n> files updated

All integration steps complete.
```

## Guards

- **Approval required** — never proceed past Step 1 if the artifact fails lint.
- **Accurate counts** — always count actual files, never hardcode or guess artifact counts.
