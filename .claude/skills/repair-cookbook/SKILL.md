---
name: repair-cookbook
version: "2.1.0"
description: "Scan and repair cookbook integrity — broken cross-references, stale frontmatter, dead index links. Finds breaks, fuzzy-matches fixes, batch confirms."
argument-hint: "[--dry-run] [--category <name>] [--version]"
allowed-tools: Read, Glob, Grep, Edit, Write, Agent, Bash(find *), Bash(wc *), Bash(diff *), Bash(date *), Bash(cookr *), AskUserQuestion
context: fork
---

## Version Check

If `$ARGUMENTS` is `--version`, respond with exactly:

> repair-cookbook v2.1.0

Then stop.

Otherwise, print `repair-cookbook v2.1.0` as the first line of output, then proceed.

## Test Mode

If `$ARGUMENTS` contains `--test-mode`:
1. Print `[TEST MODE]` at startup.
2. Auto-approve all AskUserQuestion prompts to the first/default option (e.g., "yes" for batch fixes, option "a" for ambiguous fixes).

---

# Repair Cookbook

Scan the cookbook for integrity issues — broken `agenticdevelopercookbook://` cross-references, stale frontmatter, dead index links, structural problems — then repair what can be fixed automatically and ask about the rest.

You are a librarian auditing every shelf, cross-reference card, and index entry. You find what's broken, figure out what the correct target should be, and fix it — but you always show your work before writing.

## Usage

```
/repair-cookbook                          # full scan and repair
/repair-cookbook --dry-run                # scan only, no fixes
/repair-cookbook --category references    # scan one category only
```

## Step 1: Detect Cookbook Root

The cookbook content lives under a `cookbook/` subdirectory of the repo:

```
cookbook/
  introduction/     # conventions, glossary, getting started
  principles/       # engineering principles
  guidelines/       # topic-organized guidelines
  recipes/          # concrete specs (ui/, infrastructure/, app/, web/, etc.)
  workflows/        # development process specs
  compliance/       # verification checklists
  reference/        # external best-practices links
  appendix/         # contributing, decisions, research
  index.md          # master table of contents
```

1. If `cookbook/principles/` and `cookbook/guidelines/` exist relative to the current working directory, set `$ROOT` to `./cookbook`.
2. Otherwise, if `principles/` and `guidelines/` exist directly in the current working directory (already inside the cookbook content root), set `$ROOT` to the current directory.
3. Otherwise, if `../agenticcookbook/cookbook/` exists and contains `principles/`, set `$ROOT` to `../agenticcookbook/cookbook`.
4. Otherwise, print an error and **STOP**:
   ```
   ERROR: Cannot find cookbook. Run from the cookbook repo root or an adjacent project.
   ```

Print: `Cookbook root: $ROOT`

Count all `.md` files under `$ROOT` (excluding `.git/`, `.claude/`, `.superpowers/`) using Glob. Print: `Files to scan: <N>`

---

## Step 2: Parse Arguments

| Flag | Effect |
|------|--------|
| `--dry-run` | Scan and report only. Do not apply any fixes. |
| `--category <name>` | Run only the named category. Valid: `frontmatter`, `content`, `references`, `indexes`, `placement` |
| (none) | Run all categories, then repair |

---

## Step 3: Scan (Parallel Agents)

Read the full checklist from `${CLAUDE_SKILL_DIR}/references/validation-checks.md`.

Launch up to 3 agents in parallel. Each agent reads the checklist, receives `$ROOT`, and runs its assigned categories. Each agent is **read-only** — no edits.

**Agent 1 — Frontmatter & Content**
- Category 1: Frontmatter Integrity (F01-F15)
- Category 2: Content Structure (C01-C10)

**Agent 2 — Cross-References**
- Category 3: Cross-References (X01-X08)
- Category 4: Indexes and Documentation (I01-I04)

This agent does the most critical work. For every broken `agenticdevelopercookbook://` URI it finds, it must also:
1. Record the source file and line
2. Record the broken URI
3. Attempt fuzzy-match resolution per the strategy in the checklist
4. Report: `{source_file, line, broken_uri, match_confidence, suggested_fix, candidates[]}`

**Agent 3 — File Placement**
- Category 5: File Placement (P01-P07)

If `--category` was specified, launch only the relevant agent.

Each agent returns results in this format:

```
[PASS] <ID> <check-name>: <brief summary>
[FAIL] <ID> <check-name>: <description>
       -> <file>:<line>: <specific issue>
       -> suggested fix: <repair description> (confidence: high|low|none)
[WARN] <ID> <check-name>: <description>
       -> <file>:<line>: <specific issue>
```

---

## Step 4: Compile Report

Combine all agent results into a unified report:

```
=== COOKBOOK REPAIR SCAN ===
Path: <$ROOT>
Files scanned: <N>

--- CATEGORY 1: FRONTMATTER ---
<results>

--- CATEGORY 2: CONTENT ---
<results>

--- CATEGORY 3: CROSS-REFERENCES ---
<results>

--- CATEGORY 4: INDEXES ---
<results>

--- CATEGORY 5: FILE PLACEMENT ---
<results>

=== SUMMARY ===
Pass: <n> | Warn: <n> | Fail: <n>
Auto-fixable: <n> | Need guidance: <n> | Report only: <n>
```

If `--dry-run`, print the report and **STOP** here.

---

## Step 5: Repair

### 5a. Batch auto-fixes (high confidence)

Collect all issues where the repair strategy is `auto-fix` or where fuzzy-match found a single high-confidence match.

Present them as a batch:

```
=== PROPOSED FIXES (<N> total) ===

 1. [F05] principles/foo.md — domain field mismatch
    Fix: Update domain to "agenticdevelopercookbook://principles/foo"

 2. [X01] compliance/security.md:47 — broken ref "agenticdevelopercookbook://guidelines/general#post-gen"
    Fix: Update to "agenticdevelopercookbook://guidelines/testing/post-generation-verification"

 3. [I03] index.md:23 — dead link to "guidelines/old-file.md"
    Fix: Remove stale entry

 4. [C02] principles/new-one.md — missing Change History
    Fix: Append Change History template

...

Apply all <N> fixes? (yes / no / review individually)
```

- **yes**: Apply all fixes using Edit tool. Print each fix as applied.
- **no**: Skip to step 5b (unresolvable issues) without applying anything.
- **review individually**: Present each fix one at a time for yes/no/modify.

### 5b. Ask for guidance (low confidence or no match)

For each issue that couldn't be auto-resolved, present individually:

```
Cannot resolve: agenticdevelopercookbook://guidelines/general#post-generation-verification
Referenced from: compliance/best-practices.md (line 47)
Context: "See [post-gen verification](agenticdevelopercookbook://guidelines/general#post-generation-verification)"

Closest matches:
  a) guidelines/testing/post-generation-verification.md
  b) guidelines/code-quality/scope-discipline.md

Choose: (a/b/enter path/remove/skip)
```

Apply chosen fixes immediately.

### 5c. Structural auto-fixes

These are always safe:
- **F05 domain mismatch**: Derive correct domain from file path, update frontmatter
- **C02 missing Change History**: Append template section
- **C01 heading mismatch**: Update H1 to match frontmatter title
- **X06 self-references**: Remove the self-referencing entry from `depends-on`/`related`
- **X08 internal URI in references**: Move the entry to `related` field
- **I01 missing from index**: Add entry to `index.md` in correct section
- **I03 stale index entry**: Remove dead link from index
- **P07 temp files**: Delete `.bak`, `.tmp`, `.orig`, `~`, `.DS_Store` files

After applying fixes, run `cookr convert --update <file>...` on every artifact `.md` you
edited that has a source folder, so each fix lands in the folder it is compiled from.
Never edit or scan the part files inside a source folder; the `.md` beside it is the artifact.

---

## Step 6: Verify

After all fixes are applied, re-scan **only the previously-failing checks** to verify they now pass.

Print:
```
=== VERIFICATION ===
Re-checked <N> previously-failing items:
  Fixed: <n>
  Still failing: <n>
  New issues: <n>

<details of any remaining failures>
```

---

## Step 7: Done

Print final summary:

```
=== REPAIR COMPLETE ===
Files modified: <N>
Issues fixed: <N>
Issues remaining: <N> (report-only or skipped)
```

---

## Error Handling

- **Cookbook not found**: Print error with expected paths. Stop.
- **Agent fails**: Log failure, continue with other agents. Note in report.
- **Edit fails**: Print the failure, continue with remaining fixes. Note in summary.
- **YAML parse error**: Report the file as F01 FAIL, skip remaining frontmatter checks for that file.
