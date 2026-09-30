<!-- leaf: compliance/artifact-formatting-guideline-formatting · source: compliance/artifact-formatting/guideline-formatting.md -->

**Rules** (cite as `compliance/artifact-formatting-guideline-formatting#<slug>`):

- `files-guidelines-subdirectories-have-type` MUST — This category applies to any file with type: guideline in its frontmatter. All files in guidelines/ (and its …
- `yaml-frontmatter-fields-present-per-introduction-conventions` MUST — All required YAML frontmatter fields MUST be present per introduction/conventions.md.
- `type-field-guideline` MUST — The type field MUST be guideline.
- `first-h1-heading-match-frontmatter-title-field` MUST — The first H1 heading MUST match the frontmatter title field exactly.
- `summary-statement-appear-immediately-after-h1` MUST — A summary statement MUST appear immediately after the H1 heading. This is the guideline's core message — typically 1-3 …
- `guideline-include-structured-guidance-form` MUST — The guideline MUST include structured guidance in the form of bullet points, tables, subsections, or a combination. …
- `requirements-within-guideline-use-rfc-2119-keywords` MUST — Requirements within the guideline MUST use RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) to indicate …
- `file-end-change-history-section` MUST — The file MUST end with a ## Change History section containing a table with columns: Version, Date, Author, Summary.
- `guideline-include-compliance-section-listing` MAY — The guideline MAY include a ## Compliance section listing evaluated compliance checks and their status. This is …
- `triggers-field-present-guideline-frontmatter-yaml` MUST — The triggers field SHOULD be present in guideline frontmatter. It MUST be a YAML list of trigger names from the …

# Guideline Formatting Compliance

Guidelines are topic-oriented rules that apply during planning and implementation. They are more detailed than principles but less prescriptive than recipes — structured guidance with clear requirements.

## Applicability

This category applies to any file with `type: guideline` in its frontmatter. All files in `guidelines/` (and its subdirectories) MUST have this type.

## Checks

### gf-frontmatter-complete

All required YAML frontmatter fields MUST be present per `introduction/conventions.md`.

**Applies when:** always.

**Required fields:** id, title, domain, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references.

**Guidelines:**
- Conventions

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
- Conventions

---

### gf-compliance-section

The guideline MAY include a `## Compliance` section listing evaluated compliance checks and their status. This is recommended when the guideline is referenced by compliance checks in other categories.

**Applies when:** the guideline is referenced by one or more compliance check definitions.

---

### gf-triggers-field

The `triggers` field SHOULD be present in guideline frontmatter. It MUST be a YAML list of trigger names from the canonical taxonomy defined in `introduction/trigger-guide.md`. Empty list `[]` is acceptable for guidelines not yet classified.

**Applies when:** always.

**Guidelines:**
- Trigger Guide
- Conventions
