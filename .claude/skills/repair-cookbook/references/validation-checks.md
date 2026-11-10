# Validation Checks

Complete checklist for validating and repairing cookbook integrity. Each check has an ID, description, verification method, severity, and repair strategy.

Severities:
- **FAIL**: Must be fixed. Broken content, missing required data, invalid references.
- **WARN**: Should be fixed. Style issues, missing optional content, potential problems.
- **PASS**: Check passed successfully.

Repair strategies:
- **auto-fix**: Can be fixed automatically with high confidence.
- **fuzzy-match**: Attempt to find the correct target via filename similarity, then confirm.
- **ask**: Cannot be resolved automatically — ask the user.
- **report**: Report only, no automated fix available.

---

## Category 1: Frontmatter Integrity

Applies to all `.md` files with YAML frontmatter under content directories (`principles/`, `guidelines/`, `recipes/`, `workflows/`, `compliance/`, `reference/`, `introduction/`). Skip `_template.md` and `INDEX.md` files without frontmatter.

| ID | Check | How to verify | Severity | Repair |
|----|-------|---------------|----------|--------|
| F01 | All required fields present | Parse YAML frontmatter between `---` delimiters. Verify these fields exist: `id`, `title`, `type`, `version`, `status`, `language`, `created`, `modified`, `author`, `copyright`, `license`, `summary`, `platforms`, `tags`, `depends-on`, `related`, `references`. Report each missing field. | FAIL | report |
| F02 | No empty required fields | Check that `id`, `title`, `type`, `version`, `status`, `language`, `created`, `modified`, `author`, `copyright`, `license`, `summary` are non-empty strings (not `""`, not `null`, not `~`). List fields `platforms`, `tags`, `depends-on`, `related`, `references` may be empty arrays `[]`. | FAIL | report |
| F03 | ID is valid UUID | Check that the `id` field matches the UUID pattern: `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` (case-insensitive). | FAIL | report |
| F04 | No duplicate IDs | Collect all `id` values across every file. Report any duplicates with both file paths. | FAIL | report |
| F05 | Index entry matches folder | Every source folder's `id` has an entry in `cookbook/index.json` whose `path` is the folder and whose rdid is `<cookbook-rdid>.<type>.<path, dotted>`; no artifact carries a `domain` field. Example: `principles/simplicity/` is `adc.principle.simplicity`. `cookr validate` reports drift. | FAIL | auto-fix (`cookr update`) |
| F06 | Type field is valid | Check that `type` is one of: `principle`, `guideline`, `recipe`, `workflow`, `reference`. | FAIL | report |
| F07 | Status field is valid | Check that `status` is one of: `draft`, `review`, `accepted`, `deprecated`. | FAIL | report |
| F08 | Version is valid semver | Check that `version` matches the pattern `X.Y.Z` where X, Y, Z are non-negative integers. Use regex: `^\d+\.\d+\.\d+$`. | FAIL | report |
| F09 | Dates are valid ISO 8601 | Check that `created` and `modified` match the pattern `YYYY-MM-DD`. Verify `modified` is >= `created`. | WARN | report |
| F10 | License is MIT | Check that `license` field is exactly `MIT`. | WARN | auto-fix |
| F11 | Language is valid BCP 47 | Check that `language` is a valid BCP 47 tag. For this cookbook, it should be `en`. | WARN | report |
| F12 | Summary length | Check that `summary` is between 10 and 200 characters. Too short suggests a placeholder; too long is unwieldy for tooltips. | WARN | report |
| F13 | Tags are lowercase kebab-case | Check that every item in `tags` matches `^[a-z0-9]+(-[a-z0-9]+)*$`. | WARN | report |
| F14 | Copyright year matches created year | Check that the year in `copyright` (e.g., `2026 Mike Fullerton`) matches the year in the `created` field. | WARN | report |
| F15 | Platforms values are valid | Check that every item in `platforms` is one of: `swift`, `kotlin`, `typescript`, `csharp`, `python`, `windows`, `macos`, `ios`, `web`. Empty list `[]` is valid (means universal). | WARN | report |

---

## Category 2: Content Structure

Applies to all `.md` files with YAML frontmatter under content directories. Skip `_template.md` and `INDEX.md` files without frontmatter.

| ID | Check | How to verify | Severity | Repair |
|----|-------|---------------|----------|--------|
| C01 | H1 heading matches title | The first `# ` heading in the body (after frontmatter) should match the `title` field in frontmatter. Compare case-insensitively, stripping leading/trailing whitespace. | WARN | auto-fix |
| C02 | Change History section exists | Grep for `## Change History` in the file. Every non-template file must have this section. | FAIL | auto-fix |
| C03 | Change History table has rows | After `## Change History`, find a markdown table. It must have at least one data row (not just the header). The first row's version should match the frontmatter `version` or an earlier version. | WARN | report |
| C04 | Change History latest version matches frontmatter | The most recent version in the Change History table (last row) should match the frontmatter `version` field. | WARN | report |
| C05 | No empty sections | Find H2 sections (`## `) that have no content before the next heading or end of file. Sections with only whitespace count as empty. Skip `## Change History` (checked separately). | WARN | report |
| C06 | No TODO/FIXME placeholders | Grep for `TODO`, `FIXME`, `HACK`, `XXX`, `PLACEHOLDER` in the file body (case-insensitive). These suggest incomplete content. | WARN | report |
| C07 | Named requirements format | In files with a `## Requirements` section, check that requirements use the format `**<kebab-case-name>**: <description>`. Grep for `**` patterns and verify the name portion is kebab-case: `^[a-z0-9]+(-[a-z0-9]+)*$`. | WARN | report |
| C08 | No raw HTML | Grep for `<div`, `<span`, `<table`, `<br>`, `<img` tags. Cookbook content should be pure markdown. | WARN | report |
| C09 | Heading hierarchy | Check that headings follow proper hierarchy: no `### ` without a preceding `## `, no `#### ` without a preceding `### `. | WARN | report |
| C10 | No duplicate H2 sections | Check that no `## ` heading text appears more than once in the same file. | FAIL | report |

---

## Category 3: Cross-References

Applies to all `.md` files under content directories. **This is the primary repair category.**

| ID | Check | How to verify | Severity | Repair |
|----|-------|---------------|----------|--------|
| X01 | Links resolve | Run `cookr validate`. Every in-text link `[<rdid>](cookbook:<uuid>)` and every meta link (`depends-on`, `related`, `ingredients`) MUST name a UUID in `cookbook/index.json`, or `<cookbook-uuid>/<uuid>` in a dependency's index. Any leftover format-1 URI link is broken. Report each with the source file and target. | FAIL | fuzzy-match |
| X02 | Fragment references have targets | Find within-document `#fragment` references (cross-document links carry no fragment: link the artifact, or a check by its own UUID). For `#requirements/<name>`, verify that `**<name>**:` exists in the target file. For `#states/<name>`, verify a heading or bold text with that state name exists. For other fragments, verify a heading with that text exists. | WARN | report |
| X03 | External URLs are well-formed | Find all URLs starting with `http://` or `https://` in file bodies and `references:` frontmatter. Verify they are syntactically valid (no spaces, no trailing punctuation absorbed). Do NOT check if they are reachable (no HTTP requests). | WARN | report |
| X04 | Depends-on references exist | For each item in the `depends-on` frontmatter list, verify it resolves in the index (same as X01). | FAIL | fuzzy-match |
| X05 | Related references exist | For each item in the `related` frontmatter list, verify it resolves in the index (same as X01). | WARN | fuzzy-match |
| X06 | No self-references | Check that a file's `depends-on` and `related` lists do not contain its own UUID. | WARN | auto-fix |
| X07 | No circular depends-on | Build a dependency graph from all `depends-on` fields. Check for cycles. Report any cycles found with the full chain. | WARN | report |
| X08 | References field URLs are external | Check that items in the frontmatter `references:` list are external URLs (`http://` or `https://`), not internal UUID or `cookbook:` links. Internal cross-refs belong in `depends-on` or `related`. | WARN | auto-fix |

### Fuzzy-Match Repair Strategy for X01, X04, X05

When a link doesn't resolve:

1. **Extract the path segments** from the link's rdid label, or from a leftover URI (e.g., `adc.guideline.security.old-name` → directory `guidelines/security/`, folder `old-name`). Search `cookbook/index.json` rdids and paths, then replace the link with the match's UUID (in-text: `[<rdid>](cookbook:<uuid>)`).

2. **Search the target directory** for similar filenames:
   - Exact prefix match (e.g., `auth` matches `authentication.md`)
   - Common suffix patterns (e.g., `security-compliance` → `security` by stripping `-compliance`)
   - Levenshtein distance ≤ 3 characters
   - Same words in different order

3. **Search parent/sibling directories** if the directory itself doesn't exist:
   - Check for inserted path segments (e.g., `guidelines/swift/` → `guidelines/language/swift/`)
   - Check for moved directories (e.g., `guidelines/windows/` → `guidelines/platform/windows/`)

4. **Confidence scoring:**
   - **High** (auto-fix): Single match in same directory, or single match with common path pattern (language/platform insertion)
   - **Low** (ask): Multiple candidates, or match in a completely different directory tree

5. **Output per broken ref:**
   ```
   {source_file, broken_link, match_confidence, suggested_fix, candidates[]}
   ```

---

## Category 4: Indexes and Documentation

| ID | Check | How to verify | Severity | Repair |
|----|-------|---------------|----------|--------|
| I01 | All content files in index.md | Read `index.md`. For every `.md` file under content directories (excluding `index.md`, `_template.md`, and directory `INDEX.md` files), verify it is referenced in `index.md` — either as a direct link `[text](relative/path.md)` or mentioned by filename. | FAIL | auto-fix |
| I02 | Index links resolve | Read `index.md`. For every markdown link `[text](path)`, verify the target file exists relative to the repo root. | FAIL | fuzzy-match |
| I03 | No stale index entries | For every link in `index.md` that points to a `.md` file, verify the target file still exists. Report dead links. | FAIL | auto-fix |
| I04 | Compliance INDEX.md links resolve | Read `compliance/INDEX.md`. For every markdown link, verify the target exists. | FAIL | fuzzy-match |
| I05 | No orphaned files | For every `.md` file under content directories (excluding `index.md`, `_template.md`, and directory `INDEX.md` files), verify it is referenced by at least one other file — either via a `cookbook:<uuid>` link that resolves to it, a relative markdown link `[text](path)`, a `depends-on` or `related` entry, or an entry in `index.md`. A file with zero inbound references is orphaned — it exists but nothing points to it, so no workflow or agent will ever find it. | WARN | report |

### Orphan Detection Strategy for I05

1. **Build the full file inventory**: Glob all `.md` files under content directories. Exclude `index.md`, `_template.md`, and `INDEX.md` files.

2. **Build the inbound reference map**: For each file in the inventory, count how many other files reference it via:
   - `cookbook:<uuid>` in-text link naming its UUID
   - Relative markdown link `[text](path)` from any other file
   - Entry in `index.md`
   - Entry in any directory `INDEX.md`
   - `depends-on`, `related` or `ingredients` meta entry (a UUID) from any artifact

3. **Report orphans**: Files with zero inbound references. Group by directory for readability.

4. **Severity context**: An orphaned file in `principles/` or `guidelines/` is more concerning than one in `reference/examples/` — the former should be linked from INDEX files and cross-referenced by other guidelines. Report all, but flag content files (principles, guidelines, compliance, recipes, workflows) at higher severity than reference/example files.

---

## Category 5: File Placement

| ID | Check | How to verify | Severity | Repair |
|----|-------|---------------|----------|--------|
| P01 | Principles in correct directory | All files under `principles/` should have `type: principle` in frontmatter. No principle files should exist outside this directory. Grep all files for `type: principle` and verify they are under `principles/`. | FAIL | report |
| P02 | Guidelines in correct directory | All files under `guidelines/` should have `type: guideline`. No guideline files outside this directory. | FAIL | report |
| P03 | Recipes in correct directory | All files under `recipes/` should have `type: recipe`. No recipe files outside this directory. | FAIL | report |
| P04 | Workflows in correct directory | All files under `workflows/` should have `type: workflow`. No workflow files outside this directory. | FAIL | report |
| P05 | No .md files at repo root (except index) | The only `.md` file directly at the repo root should be `index.md` and `README.md`. All content should be in subdirectories. | WARN | report |
| P06 | File names are kebab-case | All `.md` filenames under content directories should match `^[a-z0-9]+(-[a-z0-9]+)*\.md$` or be `index.md`, `INDEX.md`, or `_template.md`. No spaces, no uppercase, no underscores (except `_template`). | WARN | report |
| P07 | No stale or temp files | Check for files matching: `*.bak`, `*.tmp`, `*.orig`, `*~`, `.DS_Store`, `Thumbs.db` under content directories. | WARN | auto-fix |
