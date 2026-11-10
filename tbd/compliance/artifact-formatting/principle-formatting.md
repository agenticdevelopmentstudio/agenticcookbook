---
id: 4814B42B-B202-41C5-A3C8-FCEF6F99F39D
title: "Principle Formatting Compliance"
type: compliance
version: 2.0.0
status: draft
language: en
created: 2026-04-04
modified: 2026-11-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Structural formatting checks for principle artifacts — frontmatter, statement, guidance, and change history."
platforms: []
tags:
  - compliance
  - artifact-formatting
  - principle
depends-on:
  - guide/introduction/conventions.md
related:
  - tbd/compliance/artifact-formatting/guideline-formatting.md
  - tbd/compliance/artifact-formatting/recipe-formatting.md
references: []
---

# Principle Formatting Compliance

Principles are concise, philosophical statements that guide engineering decisions. They are the most lightweight artifact type — a clear statement, practical guidance, and nothing more.

## Applicability

This category applies to any file with `type: principle` in its frontmatter. All files in `principles/` MUST have this type.

## Checks

### pf-frontmatter-complete

All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. There is no `domain` field.

The artifact's `id` is its identity: every link to it stores that UUID. Its rdid and folder path are held in the cookbook's `index.json`, never in the artifact; `cookr validate` fails when the index and the folders disagree.

**Applies when:** always.

**Required fields:** id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

---

### pf-type-field

The `type` field MUST be `principle`.

**Applies when:** always.

---

### pf-title-heading

The first H1 heading MUST match the frontmatter `title` field exactly.

**Applies when:** always.

---

### pf-statement

A concise statement paragraph MUST appear immediately after the H1 heading. This is the principle's core idea — typically 1-3 sentences.

**Applies when:** always.

---

### pf-actionable-guidance

The principle SHOULD include bullet points with practical applications of the idea. These translate the philosophical statement into concrete actions.

**Applies when:** the statement alone is not self-evident in practice.

---

### pf-change-history

The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.

**Applies when:** always.

**Guidelines:**
- [Conventions](../../../guide/introduction/conventions.md)

---

### pf-brevity

Principles SHOULD be concise. The body (excluding frontmatter and Change History) SHOULD NOT exceed ~50 lines. Principles are philosophical anchors, not exhaustive guides — detailed guidance belongs in guidelines.

**Applies when:** always.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-11-09 | Mike Fullerton | cookr format 2: UUID identity and rdids replace `domain`; implementations live in index.json |
| 1.0.0 | 2026-04-04 | Mike Fullerton | Initial creation |
