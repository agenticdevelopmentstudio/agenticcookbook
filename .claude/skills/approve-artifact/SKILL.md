---
name: approve-artifact
version: "1.1.0"
description: "Approve a cookbook artifact by running lint checks and stamping the frontmatter with approval metadata."
argument-hint: "[path-or-name]"
allowed-tools: Read, Glob, Grep, Edit, Bash(wc *), Bash(cookr *), AskUserQuestion
context: fork
---

# Approve Artifact v1.0.0

Run `/lint-artifact` on a cookbook artifact. If it passes (zero FAIL), stamp the frontmatter with approval metadata. If it fails, report the issues and do not approve.

## Startup

approve-artifact v1.1.0

**Version check**: Read `${CLAUDE_SKILL_DIR}/SKILL.md` from disk and extract the `version:` field from frontmatter. Compare to this skill's version (1.1.0). If they differ, print:

> Warning: This skill is running v1.1.0 but vA.B.C is installed. Restart the session to use the latest version.

Then continue running.

If `$ARGUMENTS` is `--version`, respond with exactly:
> approve-artifact v1.1.0

Then stop.

## Argument Resolution

Use the same argument resolution flow as `/lint-artifact`:

1. If `$ARGUMENTS` is a path or ends with `.md`, treat as file path.
2. If `$ARGUMENTS` is a search string, search `cookbook/principles/`, `cookbook/guidelines/`, `cookbook/recipes/` for matching `.md` files.
3. If `$ARGUMENTS` is empty, check session context or prompt the user.

See `/lint-artifact` for the full resolution flow.

## Step 1: Lint

Run the full `/lint-artifact` check suite on the resolved file. Capture the result.

- If there are **any FAIL** results, print the full lint report and then:

```
RESULT: NOT APPROVED — <n> failing checks must be fixed first.
```

Then stop. Do not modify the file.

- If there are **zero FAIL** results (PASS and WARN only), proceed to Step 2.

## Step 2: Stamp Frontmatter

Read the current skill version from `${CLAUDE_SKILL_DIR}/SKILL.md` frontmatter.

Update the artifact file's YAML frontmatter:

| Field | Value |
|-------|-------|
| `approved-by` | `"approve-artifact v<version>"` (e.g., `"approve-artifact v1.1.0"`) |
| `approved-date` | Today's date in ISO 8601 format (e.g., `2026-04-04`) |

Use the Edit tool to update these two fields in place. Do not modify any other fields or content.

If the artifact has a source folder (`<name>/artifact.json` beside `<name>.md`), run
`cookr convert --update <path>` next, so the stamp lands in the folder the `.md` is compiled from.

## Step 3: Report

Print:

```
=== APPROVAL ===
Artifact: <filename>
Type: <type>
Approved by: approve-artifact v<version>
Approved date: <date>
Warnings: <n>

RESULT: APPROVED
```

If there were warnings, list them below the result:

```
Warnings (non-blocking):
  [WARN] <ID>: <title>
         -> <recommendation>
```

## Guards

- **Lint must pass** — never stamp approval on an artifact with FAIL results.
- **Frontmatter only** — only modify `approved-by` and `approved-date` fields. Do not touch any other content.
- **Version accuracy** — always read the current skill version from disk, do not hardcode it in the stamp.
