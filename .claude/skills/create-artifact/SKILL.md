---
name: create-artifact
version: "1.1.0"
description: "Guided creation of a new cookbook artifact. Walks through type selection, content authoring, and integration via /add-artifact."
argument-hint: "[principle|guideline|recipe] [--title <title>]"
allowed-tools: Read, Glob, Grep, Edit, Write, Bash(uuidgen), Bash(date *), Bash(wc *), Bash(rsync *), Bash(cookr *), AskUserQuestion
context: fork
---

# Create Artifact v1.0.0

Guided wizard for creating a new cookbook artifact from scratch. Asks which type (principle, guideline, recipe), walks through content authoring using the formatting compliance spec for that type, then invokes `/add-artifact` to integrate.

## Startup

create-artifact v1.1.0

**Version check**: Read `${CLAUDE_SKILL_DIR}/SKILL.md` from disk and extract the `version:` field from frontmatter. Compare to this skill's version (1.1.0). If they differ, print:

> Warning: This skill is running v1.1.0 but vA.B.C is installed. Restart the session to use the latest version.

Then continue running.

If `$ARGUMENTS` is `--version`, respond with exactly:
> create-artifact v1.1.0

Then stop.

## Test Mode

If `$ARGUMENTS` contains `--test-mode`:
1. Print `[TEST MODE]` at startup.
2. Auto-approve all AskUserQuestion prompts to the first/default option.
3. For title: use the `--title` argument value if provided, otherwise use "Test Artifact".
4. For location: accept the proposed default path.
5. For summary: use "Test artifact created in test mode."
6. For platforms: use empty list.
7. For section content: generate minimal valid content that passes lint.

## Step 1: Determine Type

If `$ARGUMENTS` starts with `principle`, `guideline`, or `recipe`, use that type.

Otherwise, ask:

Use AskUserQuestion: "What type of artifact?" with options:
- **Principle** — Foundational engineering idea (~1 page, philosophical)
- **Guideline** — Topic-oriented rule for planning and implementation
- **Recipe** — Concrete spec for a component, pattern, or infrastructure

## Step 2: Gather Basic Info

Ask the user (one question at a time):

1. **Title**: If `--title` was provided in `$ARGUMENTS`, use it. Otherwise ask: "What's the title?" (short, descriptive, e.g., "Test Pyramid", "Empty State", "Idempotency")

2. **Location**: Propose a file path based on the type and title:
   - Principles: `cookbook/principles/<kebab-case-title>.md`
   - Guidelines: Ask which topic subdirectory (list existing ones from `cookbook/guidelines/`), then `cookbook/guidelines/<topic>/<kebab-case-title>.md`
   - Recipes: Ask which category (list existing ones from `cookbook/recipes/`), then `cookbook/recipes/<category>/<kebab-case-title>.md`

   Use AskUserQuestion to confirm or override the proposed path.

3. **Summary**: Ask: "One-line summary (~120 chars) for search and tooltips?"

4. **Platforms**: Ask: "Which platforms? (empty for universal)" with multi-select options: swift, kotlin, typescript, csharp, python, windows, macos, ios, web.

## Step 3: Generate Frontmatter

Generate the YAML frontmatter:

```yaml
---
id: <generate with uuidgen>
title: "<title>"
domain: agenticdevelopercookbook://<path-without-.md>
type: <type>
version: 1.0.0
status: draft
language: en
created: <today ISO 8601>
modified: <today ISO 8601>
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "<summary>"
platforms: <platforms list or []>
tags: <derive 1-3 tags from title and topic>
depends-on: []
related: []
references: []
approved-by: ""
approved-date: ""
---
```

## Step 4: Author Content

Read the compliance file for the artifact type:

| Type | Compliance File |
|------|----------------|
| Principle | `cookbook/compliance/artifact-formatting/principle-formatting.md` |
| Guideline | `cookbook/compliance/artifact-formatting/guideline-formatting.md` |
| Recipe | `cookbook/compliance/artifact-formatting/recipe-formatting.md` |

Walk through each required section defined in the compliance file, asking the user for content. For each section:

1. Explain what the section needs (based on the compliance check description).
2. Ask the user to provide the content or describe what they want.
3. Draft the section and confirm with the user before moving on.

### Type-specific guidance:

**Principles:**
- Ask for the core statement (1-3 sentences).
- Ask for practical bullet points (actions that follow from the principle).
- Keep it concise — under ~50 lines of body content.

**Guidelines:**
- Ask for the summary statement.
- Ask for structured guidance (rules, recommendations, patterns).
- Ask about RFC 2119 keywords — which items are MUST vs SHOULD vs MAY.

**Recipes:**
- Follow the section order from `recipe-formatting.md` strictly.
- For each section, explain what's needed and draft collaboratively.
- For Appearance: ask for concrete values (colors, spacing, fonts).
- For Behavioral Requirements: name each requirement in kebab-case with RFC 2119 keywords.
- For Test Vectors: create entries that reference the named requirements.
- For infrastructure recipes: confirm which UI-specific sections to omit (Appearance, States).

## Step 5: Write the File

Assemble the complete artifact and write it to the resolved path using the Write tool.

Then run `cookr convert <path>`. It creates the artifact's source folder (`<name>/`) and
rewrites `<path>` as the folder's compiled output. If it refuses the file, fix what it
reports and run it again.

Print:

```
Artifact written to: <path>
```

## Step 6: Integrate

Run `/add-artifact <path>` to execute the full integration flow:
- Lint and approve
- Update indexes
- Update documentation counts
- Sync to website

If `/add-artifact` reports failures, help the user fix them and re-run.

## Step 7: Done

Print:

```
=== ARTIFACT CREATED ===
Title: <title>
Type: <type>
Path: <path>
Status: draft (approved)
```

## Guards

- **One question at a time** — do not ask multiple questions in a single message.
- **Compliance-driven** — every section authored must satisfy the compliance checks for the artifact type.
- **User confirms each section** — do not write the file until all sections are confirmed.
- **Integration required** — always run `/add-artifact` at the end. Do not skip integration.
