<!-- leaf: compliance/artifact-formatting-principle-formatting · source: compliance/artifact-formatting/principle-formatting.md -->

**Rules** (cite as `compliance/artifact-formatting-principle-formatting#<slug>`):

- `frontmatter-files-principles-have-type` MUST — This category applies to any file with type: principle in its frontmatter. All files in principles/ MUST have this type.
- `yaml-frontmatter-fields-present-per-introduction-conventions` MUST — All required YAML frontmatter fields MUST be present per introduction/conventions.md.
- `type-field-principle` MUST — The type field MUST be principle.
- `first-h1-heading-match-frontmatter-title-field` MUST — The first H1 heading MUST match the frontmatter title field exactly.
- `concise-statement-paragraph-appear-immediately-after-h1` MUST — A concise statement paragraph MUST appear immediately after the H1 heading. This is the principle's core idea — …
- `principle-include-bullet-points-practical` SHOULD — The principle SHOULD include bullet points with practical applications of the idea. These translate the philosophical …
- `file-end-change-history-section` MUST — The file MUST end with a ## Change History section containing a table with columns: Version, Date, Author, Summary.
- `principles-concise-body-excluding-frontmatter` SHOULD — Principles SHOULD be concise. The body (excluding frontmatter and Change History) SHOULD NOT exceed ~50 lines. …

# Principle Formatting Compliance

Principles are concise, philosophical statements that guide engineering decisions. They are the most lightweight artifact type — a clear statement, practical guidance, and nothing more.

## Applicability

This category applies to any file with `type: principle` in its frontmatter. All files in `principles/` MUST have this type.

## Checks

### pf-frontmatter-complete

All required YAML frontmatter fields MUST be present per `introduction/conventions.md`.

**Applies when:** always.

**Required fields:** id, title, domain, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references.

**Guidelines:**
- Conventions

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
- Conventions

---

### pf-brevity

Principles SHOULD be concise. The body (excluding frontmatter and Change History) SHOULD NOT exceed ~50 lines. Principles are philosophical anchors, not exhaustive guides — detailed guidance belongs in guidelines.

**Applies when:** always.
