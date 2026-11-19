---
id: 39931D07-F23F-4980-A055-6916E722A01F
title: "Guideline Formatting Compliance"
type: compliance
version: 2.1.2
status: draft
language: en
created: 2026-04-04
modified: 2026-11-16
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Structural formatting checks for guideline artifacts — frontmatter, summary, structured guidance, RFC keywords, roled parts, named rules cited to their research, and change history."
platforms: []
tags:
  - compliance
  - artifact-formatting
  - guideline
depends-on:
  - guide/introduction/conventions.md
related:
  - tbd/compliance/artifact-formatting/principle-formatting.md
  - tbd/compliance/artifact-formatting/recipe-formatting.md
references: []
---

# Guideline Formatting Compliance

Guidelines are topic-oriented rules that apply during planning and implementation. They are more detailed than principles but less prescriptive than recipes — structured guidance with clear requirements.

## Applicability

This category applies to any file with `type: guideline` in its frontmatter. All files in `guidelines/` (and its subdirectories) MUST have this type.

## Checks

### gf-frontmatter-complete

All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. There is no `domain` field.

The artifact's `id` is its identity: every link to it stores that UUID. Its rdid and folder path are held in the cookbook's `index.json`, never in the artifact; `cookr validate` fails when the index and the folders disagree.

**Applies when:** always.

**Required fields:** id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

---

### gf-type-field

The `type` field MUST be `guideline`.

**Applies when:** always.

---

### gf-title-heading

The first H1 heading MUST match the frontmatter `title` field exactly.

**Applies when:** always.

---

### gf-summary-statement

A summary statement MUST appear immediately after the H1 heading. This is the guideline's core message — typically 1-3 sentences that a reader can act on without reading further.

**Applies when:** always.

---

### gf-structured-guidance

The guideline MUST include structured guidance in the form of bullet points, tables, subsections, or a combination. Unstructured prose without actionable items is not sufficient.

**Applies when:** always.

---

### gf-rfc-keywords

Requirements within the guideline MUST use RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) to indicate obligation levels. Keywords MUST be bold or uppercase when used normatively.

**Applies when:** the guideline contains requirements or rules (not purely informational content).

---

### gf-change-history

The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

**Applies when:** always.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

---

### gf-compliance-section

The guideline MAY include a `## Compliance` section listing evaluated compliance checks and their status. This is recommended when the guideline is referenced by compliance checks in other categories.

**Applies when:** the guideline is referenced by one or more compliance check definitions.

---

### gf-triggers-field

The `triggers` field SHOULD be present in guideline frontmatter. It MUST be a YAML list of trigger names from the canonical taxonomy defined in `introduction/trigger-guide.md`. Empty list `[]` is acceptable for guidelines not yet classified.

**Applies when:** always.

**Guidelines:**
- [Trigger Guide](../../../guide/introduction/trigger-guide.md)
- [Conventions](../../../guide/introduction/conventions.md)

---

### gf-roled-parts

A roled guideline MUST give every part but the intro and the history a `role` in `artifact.json`, one of `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`, and MUST have at least one part of each of `rules`, `review-focus`, `review-bar` and `build-bar`. It sets no `routes` and no `hosts/`, and does not live under `guidelines/reviewing/`.

What each role holds (`guidelines/implementing/data/indexing` is a worked example; its parts are `rules`, `look-for`, `a-complete-review-must-establish` and `a-build-must-establish`, among others):

| Role | Holds | Goes to |
|---|---|---|
| none (`intro`) | the summary statement | every skill |
| `rules` | the named rules | builder, reviewer |
| `how-to`, `examples` | how to keep the rules | builder |
| `review-focus` | what a reviewer looks for | reviewer |
| `review-bar` | what a complete review must establish | review-verifier |
| `build-bar` | what a complete build must establish: exactly one line per named rule, `` - `rule-name`: … ``, and no line naming anything else | build-verifier |
| `rationale`, `references` | why, and the sources | each skill's references |
| none (`history`) | the change history | none |

**Applies when:** any part of the guideline carries a `role`.

**Guidelines:**
- [Conventions: Roles](../../../guide/introduction/conventions.md)

---

### gf-named-rules

Every bullet in a `rules` part MUST be a named rule: `- **kebab-name**: … MUST|SHOULD|MAY …`, its name unique in the guideline and its obligation an RFC 2119 keyword.

**Applies when:** the guideline is roled.

---

### gf-research-folder

The guideline MUST keep the research it was written from in `research/` in its folder: `research/research.json`, in the shape of the research-results document (`guidelines/researching/evidence/research-results-document`), and `research/research.md`, the same, readable, under the four question headings in this order: `## Best practices`, `## Known solutions`, `## Platform guidelines`, `## The expert's view`.

Each claim in `research.json`'s `claims` list is the per-claim record: `id` (kebab-case, unique), `question` (`best-practices`, `known-solutions`, `platform-guidelines` or `experts-view`), `claim`, `citations` (each with `title`, `author`, `publisher`, `date`, `url`, `accessed`), `source_type`, `quote`, `generated_by`, `query`, `trust` (`{"score": 0-100, "basis"}`) and `independence` (`multi-independent`, `single` or `uncorroborated`). The `verdicts` list gives each rule checked a verdict, `supported`, `contradicted`, `unsupported` or `new`, and the claims it rests on, at least one; every claim a rule cites MUST be named by a verdict. A rule the research cannot support is recorded as a claim itself, its source the cookbook's own text at the topic's base commit, with an `unsupported` verdict (`contradicted` when the research finds against it) naming that claim; a rule kept for the owner cites it, and `cookr validate` passes it with an `owner-decides` warning naming the rule and the claim.

**Applies when:** the guideline is roled, or has a `research/` folder. Until Task 8b of the finish-the-cookbook-roles plan, other guidelines are not checked; a roled topic still to be researched is listed in `cookbook/research-exempt.json`.

**Guidelines:**
- [Conventions: Research](../../../guide/introduction/conventions.md)

---

### gf-rule-cites-research

Each named rule MUST cite the claims of its research it stands on, once, at the end of its bullet: `(claim: <id>)`, or `(claims: <id>, <id>)` for several. Nothing follows the citation. Every id cited MUST be a claim in `research/research.json`. The citation names the claim, never the document (`cite-the-claim-not-the-document`), so a reader can follow a rule to the quote and source behind it.

```markdown
- **index-foreign-keys**: Every foreign-key column MUST have an index. (claims: fk-index-postgres, fk-index-sqlite)
```

**Applies when:** the guideline has a `research/` folder. In a roled guideline the named rules are its `rules` parts' bullets; in an unroled one, every named bullet that states MUST, SHOULD or MAY outside the intro and the history.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.1.2 | 2026-11-16 | Mike Fullerton | gf-research-folder: every verdict names a claim; a rule the research cannot support cites itself as a claim, for the owner; gf-roled-parts: one build-bar line per named rule |
| 2.1.1 | 2026-11-16 | Mike Fullerton | gf-research-folder: every cited claim has a verdict; gf-rule-cites-research: one citation, ending the rule |
| 2.1.0 | 2026-11-16 | Mike Fullerton | Roled guidelines: gf-roled-parts, gf-named-rules, gf-research-folder and gf-rule-cites-research |
| 2.0.0 | 2026-11-09 | Mike Fullerton | cookr format 2: UUID identity and rdids replace `domain`; implementations live in index.json |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Add triggers field compliance check |
| 1.0.0 | 2026-04-04 | Mike Fullerton | Initial creation |
