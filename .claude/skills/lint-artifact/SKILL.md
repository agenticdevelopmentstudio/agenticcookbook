---
name: lint-artifact
version: "2.0.2"
description: "Lint a cookbook artifact (principle, guideline, or recipe) against its type's formatting compliance checks. Auto-detects type from frontmatter."
argument-hint: "[path-or-name]"
allowed-tools: Read, Glob, Grep, Bash(wc *), Bash(git rev-parse *), Bash(PYTHONPATH=*), AskUserQuestion
context: fork
model: sonnet
---

# Lint Artifact v2.0.2

Validate a cookbook artifact for structural completeness, frontmatter correctness, and convention compliance. Auto-detects the artifact type from the `type` frontmatter field and runs the corresponding checks: the named rules of its type's formatting guideline (`cookbook/guidelines/cookbook/authoring/<type>-formatting/rules.md`), or, for a recipe, `tbd/compliance/artifact-formatting/recipe-formatting.md` until it folds into template-conformance.

## Startup

lint-artifact v2.0.2

**Version check**: Read `${CLAUDE_SKILL_DIR}/SKILL.md` from disk and extract the `version:` field from frontmatter. Compare to this skill's version (2.0.2). If they differ, print:

> Warning: This skill is running v2.0.2 but vA.B.C is installed. Restart the session to use the latest version.

Then continue running.

If `$ARGUMENTS` is `--version`, respond with exactly:
> lint-artifact v2.0.2

Then stop.

## Running cookr

`cookr` below always means this checkout's own cookr, run exactly as:

```
PYTHONPATH=<repo>/skills/cookr/cli $COOKR_PY -m cookr -p <repo> <command>
```

`<repo>` is this checkout's root (`git rev-parse --show-toplevel`). `$COOKR_PY`
is a Python 3.11 or later that imports `rich`, `questionary` and `yaml`:
`python3` when `python3 -c "import rich, questionary, yaml"` exits 0, else
`~/.cache/grow-cookbook/cookr-venv/bin/python` (see `/grow-cookbook`, *COOKR_PY*);
a caller that names one, such as `/grow-cookbook`, passes its own. Write the
path itself into each command. Never an installed `cookr` on PATH, and never
the `skills/cookr/bin/cookr` shim.

## Argument Resolution

Resolve `$ARGUMENTS` to an artifact. An artifact is a source folder (`<name>/artifact.json` plus
one `.md` per section); lint its compiled doc, written to the scratchpad with
`cookr compile <folder> --out <scratch>`, never committed. Resolve using this flow:

### If `$ARGUMENTS` is provided:

1. **Path check**: If `$ARGUMENTS` contains `/` or ends with `.md`, treat it as a path.
   - If it is a source folder (or a `.md` whose folder exists), use that folder.
   - If not, print "File not found: <path>" and stop.

2. **UUID or rdid**: If `$ARGUMENTS` is a UUID or an rdid (`adc.guideline.testing.test-pyramid`), run `cookr id <arg>`, which prints the folder path.

3. **Search string**: Otherwise, treat `$ARGUMENTS` as a search string. Use Glob to find all source folders (`*/artifact.json`) under `cookbook/principles/`, `cookbook/guidelines/`, `cookbook/ingredients/` and `cookbook/recipes/`. Filter to files whose name contains the search string (case-insensitive).
   - **1 match** -> Use it. Print: "Found: <path>"
   - **Multiple matches** -> Show up to 4 matches with AskUserQuestion. Each option label is the filename, description is the relative path. The user picks one.
   - **0 matches** -> Print "No artifacts matching '<string>'" and stop.

### If `$ARGUMENTS` is empty:

1. **Session context**: Check if an artifact file was recently created, edited, or read in this conversation. If so, offer it:
   - Use AskUserQuestion: "Lint <filename>?" with options "Yes" and "No, choose another".
   - If "Yes", use that file.

2. **Prompt**: If no recent artifact or user declined, use AskUserQuestion: "Which artifact? Enter a name or path." The user's response re-enters the search string flow above.

## Type Detection

Read the target file's YAML frontmatter. Extract the `type` field.

| Type | Compliance File |
|------|----------------|
| `principle` | `cookbook/guidelines/cookbook/authoring/principle-formatting/rules.md` |
| `guideline` | `cookbook/guidelines/cookbook/authoring/guideline-formatting/rules.md` |
| `recipe` | `tbd/compliance/artifact-formatting/recipe-formatting.md` |

If the `type` field is missing or not one of the three artifact types, print:

> FAIL: File has type '<value>' — not a lintable artifact type. Expected: principle, guideline, or recipe.

Then stop.

Print: `Type: <type> | Compliance: <compliance-file>`

## References

Before running checks, read:
1. The compliance file for the detected type (from table above)
2. `guide/introduction/conventions.md` — format and frontmatter rules

If either is missing, warn but continue with what's available.

## Checks

Read the target artifact file completely. Run all checks defined in the compliance file for the detected type. Each check in the compliance file has a check ID (e.g., `pf-frontmatter-complete`, `gf-type-field`, `rf-overview`).

For each check, emit one of:

```
[PASS] <ID>: <title>
[WARN] <ID>: <title>
       -> <recommendation>
[FAIL] <ID>: <title>
       -> <what's wrong>
```

### Shared Checks (All Types)

These checks apply to every artifact regardless of type:

| ID | Check | PASS | FAIL |
|----|-------|------|------|
| FM-01 | YAML frontmatter block present | `---` delimiters found | No frontmatter |
| FM-02 | `id` field is a valid UUID | UUID format | Missing or malformed |
| FM-03 | Index entry matches folder | `cookbook/index.json` has an entry for `id` whose `path` is this folder and whose rdid is `<cookbook-rdid>.<type>.<path, dotted>` (`cookr validate` reports drift) | Missing entry, wrong path, or a `domain:` field present |
| FM-04 | `type` matches expected type | Matches the detected type | Wrong value |
| FM-05 | `version` is valid semver | Matches `X.Y.Z` pattern | Missing or malformed |
| FM-06 | All required fields present | id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references: the guideline compliance file's gf-frontmatter-complete list. `approved-by` and `approved-date` are `/approve-artifact`'s stamp, written after lint, and are not checked here | A field of that list missing; never fail on a field that is present |
| FM-07 | `license` is `MIT` | Exactly `MIT` | Other value |
| FM-08 | `copyright` includes year and name | Contains 4-digit year and a name | Missing or malformed |
| FM-09 | `created` and `modified` are valid dates | ISO 8601 date format | Invalid format |
| FM-10 | `summary` is non-empty | At least 10 characters | Empty or too short |
| FM-11 | H1 heading matches `title` | First `# ` heading matches frontmatter `title` | Mismatch |
| FM-11a | Links resolve | Every `depends-on`, `related`, `ingredients` value is a UUID (or `<cookbook-uuid>/<uuid>`) and every in-text `[<rdid>](cookbook:<uuid>)` resolves (`cookr validate`) | Unresolved link, or a format-1 URI link |
| FM-12 | Change History section present | `## Change History` exists with at least one table row | Missing or empty |
| FM-13 | No TODO/placeholder text | No `TODO`, `TBD`, `FIXME`, `placeholder`, `fill in` | Found placeholder text |

### Type-Specific Checks

After shared checks, run the checks specific to the detected type. Read the compliance file and evaluate each check defined there that is not already covered by the shared checks above.

**Principles** (from `principle-formatting.md`):

| ID | Check | PASS | WARN/FAIL |
|----|-------|------|-----------|
| PF-01 | Statement paragraph after H1 | Concise statement (1-3 sentences) immediately follows H1 | FAIL if missing |
| PF-02 | Actionable guidance | Bullet points with practical applications present | WARN if missing |
| PF-03 | Brevity | Body (excluding frontmatter and Change History) is under ~50 lines | WARN if exceeds |

**Guidelines** (from `guideline-formatting.md`):

| ID | Check | PASS | WARN/FAIL |
|----|-------|------|-----------|
| GF-01 | Summary statement after H1 | Summary statement (1-3 sentences) immediately follows H1 | FAIL if missing |
| GF-02 | Structured guidance | Contains bullet points, tables, or subsections | FAIL if unstructured prose only |
| GF-03 | RFC 2119 keywords in requirements | Requirements use MUST, SHOULD, MAY | WARN if missing |
| GF-04 | Compliance section | `## Compliance` section present | WARN if missing when referenced by compliance checks |

**Recipes** (from `recipe-formatting.md`):

| ID | Check | PASS | WARN/FAIL |
|----|-------|------|-----------|
| RF-01 | Overview section | `## Overview` present with content | FAIL if missing |
| RF-02 | Behavioral Requirements section | `## Behavioral Requirements` present with named requirements using RFC 2119 keywords | FAIL if missing |
| RF-03 | Requirements use kebab-case names | All names match `[a-z0-9]+(-[a-z0-9]+)*` | FAIL if not |
| RF-04 | No duplicate requirement names | All names unique within file | FAIL if duplicates |
| RF-05 | Appearance section | `## Appearance` present (FAIL for UI recipes, WARN if omitted for infrastructure) | Context-dependent |
| RF-06 | States table | `## States` with at least 2 states (FAIL for UI recipes, WARN if omitted for infrastructure) | Context-dependent |
| RF-07 | Accessibility section | `## Accessibility` present with content | FAIL if missing |
| RF-08 | Test vectors | `## Conformance Test Vectors` table with at least one row referencing a valid requirement name | FAIL if missing |
| RF-09 | Edge cases | `## Edge Cases` with at least 2 items | WARN if fewer |
| RF-10 | Logging section | `## Logging` present with at least 1 event or "Not applicable" with reason | FAIL if empty |
| RF-11 | Platform notes | `## Platform Notes` present | FAIL if missing |
| RF-12 | Design decisions | `## Design Decisions` present | WARN if empty |
| RF-13 | Compliance table | `## Compliance` with at least one row | WARN if missing |
| RF-14 | Section order | Sections appear in the order defined in `recipe-formatting.md` | WARN if out of order |

## Summary

After all checks, print:

```
=== LINT SUMMARY ===
Artifact: <filename>
Type: <type>
Pass: <n> | Warn: <n> | Fail: <n>
```

If there are any FAIL items, print:

```
RESULT: NOT CLEAN — <n> failing checks. Fix these before the artifact can be approved.
```

If all checks pass (zero FAIL, zero or more WARN):

```
RESULT: CLEAN — artifact passes all checks.
```

## Guards

- **Read-only** — do not modify the artifact file or any other file.
- **No version flagging** — never flag the `version` frontmatter field value as a warning or error.
- **Console only** — print the report to stdout; do not write report files.
