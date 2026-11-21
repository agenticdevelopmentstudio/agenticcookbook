# Research: guideline-formatting

Researched 2026-11-21 at base commit `071e52f9572bf4b7c534cfcf95fb111282abc423`, for the topic `cookbook/guidelines/cookbook/authoring/guideline-formatting` (area `cookbook/authoring`). The research covers how a cookbook guideline is structured: its meta (frontmatter), title, summary statement, structured guidance, roled parts, named rules, the research each rule cites, its compliance section, its `triggers` field and its change history. Two things are left to sibling topics. Keyword case and lint severity belong to `requirement-keywords`, and the `triggers` vocabulary belongs to `activity-triggers`.

**Summary.** The standards that govern rule-bearing documents agree on most of the shape the draft describes:

- a required summary up front;
- required metadata, enforced by a schema;
- requirements written in one consistent style that a reader can tell apart from other text;
- each requirement uniquely referenceable and stating one thought;
- rationale kept with the requirement but apart from it;
- a record of the changes in each version.

Linking evidence to each recommendation is a standard for trustworthy guidelines. The sources state it at SHOULD strength, though, so the draft's MUSTs for the research folder and for per-rule citations are unsupported at the strength they state. No outside source speaks to the cookbook's own machinery: its role vocabulary, how parts compile to skills, the triggers field, the compliance section and the legacy exemption. Those rules are recorded as prior-text claims for the owner to decide.

## Best practices

**Requirements engineering (NASA).**
- A good requirement expresses one thought, with one subject and one predicate (`nasa-one-thought-per-requirement`).
- Each requirement can be uniquely referenced, for example by a unique number (`nasa-uniquely-referenced`).
- Each requirement comes with an intelligible rationale, including its assumptions (`nasa-rationale-accompanies-requirement`).
- Each requirement is verifiable: it can be tested, demonstrated, inspected or analysed (`nasa-requirements-verifiable`).

**Guideline-development standards (IOM, AGREE II).** These come from clinical guidelines. They are the closest standards for documents that carry recommendations backed by evidence.
- For each recommendation, a guideline should provide a summary of the relevant evidence and of the gaps in it (`iom-evidence-per-recommendation`).
- Recommendations should be written in a standard form that states precisely what action is recommended and when it applies (`iom-standardized-form-and-circumstances`).
- Strong recommendations should be worded so that compliance with them can be evaluated (`iom-compliance-evaluable`).
- A trustworthy guideline comes from an explicit and transparent process (`iom-transparent-process`).
- AGREE II appraises a guideline on four points that apply here:
  - whether there is an explicit link between each recommendation and its evidence (`agree-explicit-link-to-evidence`);
  - whether key recommendations are easy to identify (`agree-key-recommendations-identifiable`);
  - whether recommendations are specific and unambiguous (`agree-specific-unambiguous`).

Both sources state these at SHOULD or appraisal strength, never as MUST.

**Change records.**
- A changelog has an entry for every version (`keepachangelog-entry-per-version`).
- The latest version comes first (`keepachangelog-latest-first`).
- Each version's release date is shown (`keepachangelog-date-displayed`).

**Docs as code.**
- Documentation is written and checked with the same tools as code, automated tests among them (`writethedocs-docs-as-code`).
- Documentation does not duplicate what existing documentation already says (`govuk-dont-duplicate`). This supports one source per topic.

**Rules with no outside support.**
- `gf-compliance-section` (`gf-compliance-section-prior`): no source speaks to a section that lists evaluated compliance checks. The W3C's conformance clause is a different element: it says what conformance requires, not which checks have been run.
- `gf-roled-parts` (`gf-roled-parts-prior`): the sources support labelling sections and separating kinds of content at SHOULD or good-practice strength (see Platform guidelines). The eight role values and the four required roles are the cookbook's own design.
- `gf-research-folder` (`gf-research-folder-prior`) and `gf-rule-cites-research` (`gf-rule-cites-research-prior`): the evidence-linking standards support the practice at SHOULD strength (`iom-evidence-per-recommendation`, `agree-explicit-link-to-evidence`), not at the MUST the rules state. The folder layout and the `(claims: …)` syntax are the cookbook's own.

## Known solutions

**What a tool can check.** Each of the draft's 13 checks, mapped to a tool that can decide it:

| Check | Tool that decides it |
|---|---|
| `gf-frontmatter-complete` | A JSON Schema with `required` (`json-schema-required`). `additionalProperties: false` refuses a forbidden field such as `domain` (`json-schema-no-additional-properties`). Applied to Markdown by remark-lint-frontmatter-schema (`remark-lint-frontmatter-schema`) or by Astro's content-collection schemas (`astro-schema-enforces-frontmatter`). Fully decidable. |
| `gf-type-field` | A schema `enum` or `const` (`json-schema-enum`). Fully decidable. |
| `gf-title-heading` | markdownlint MD041 checks that a title exists (`markdownlint-md041-first-line-heading`), and MD025 checks that there is only one top-level heading (`markdownlint-md025-front-matter-title`). Neither compares the H1 with the front-matter title; a custom rule can, because it receives `frontMatterLines` (`markdownlint-custom-rules`). By default, MD025 treats a front-matter `title` as the H1, so a title plus an H1 is reported unless `front_matter_title` is set to `""`. |
| `gf-summary-statement` | A custom rule can check that a paragraph follows the H1. Whether that paragraph is the guideline's "core message" is a judgement no tool decides. Partly decidable. |
| `gf-structured-guidance` | A custom markdownlint rule, or Vale's `list` and `heading` scopes (`vale-markup-aware-scopes`), can check that lists, tables or subsections are present. Whether the items are "actionable" is a judgement. Partly decidable. |
| `gf-rfc-keywords` | Vale's existence check can find keywords in list items (`vale-existence-check`, `vale-markup-aware-scopes`). Keyword case and severity are cited from `requirement-keywords`. |
| `gf-change-history` | markdownlint MD043 enforces a required heading list, with wildcards (`markdownlint-md043-required-headings`). A custom rule checks the table's columns. Fully decidable. |
| `gf-compliance-section` | MD043 can require the heading when the condition holds. The condition ("referenced by compliance checks") needs a cross-file index. |
| `gf-triggers-field` | A schema with `type: array` and an `enum` for the items (`json-schema-enum`). The vocabulary belongs to `activity-triggers`. |
| `gf-roled-parts`, `gf-research-folder` | A JSON Schema over `artifact.json` and `research.json` (`json-schema-required`, `json-schema-enum`). Fully decidable. |
| `gf-named-rules` | A Vale rule scoped to `list` with a token pattern, or a custom markdownlint rule (`vale-markup-aware-scopes`, `markdownlint-custom-rules`). Name uniqueness needs a whole-file custom rule. |
| `gf-rule-cites-research` | A custom rule that reads the bullets and `research.json` (`markdownlint-custom-rules`). Fully decidable. |

**Identifiers and versions.**
- OWASP ASVS uses positional identifiers (chapter.section.requirement). It warns that these "may change between versions" and has references carry the version (`asvs-versioned-identifiers`).
- Semantic Versioning: once a version is released, its contents MUST NOT be modified (`semver-released-immutable`).

**Rules with no outside support (`conv-*` tool behaviour).** These rules state what `cookr` compiles or validates, not a writing practice that an outside source could address. Each is recorded with its prior claim, and under owner ruling Q12 it is the owner's to keep as a design statement:
- `conv-legacy-keeps-working` (`conv-legacy-keeps-working-prior`)
- `conv-role-values` (`conv-role-values-prior`)
- `conv-no-roles-under-reviewing` (`conv-no-roles-under-reviewing-prior`)
- `conv-roled-artifact-complete` (`conv-roled-artifact-complete-prior`)
- `conv-four-skills` (`conv-four-skills-prior`)
- `conv-skill-names` (`conv-skill-names-prior`)

`gf-triggers-field` (`gf-triggers-field-prior`) is likewise unsupported. The sources support only the shape of the field, a closed-vocabulary list (`json-schema-enum`). Whether a guideline should carry the field at all is the cookbook's own decision.

## Platform guidelines

**IETF.**
- Every RFC must have an Abstract (`rfc7322-abstract-required`). The Abstract should be complete in itself (`rfc7322-abstract-complete-in-itself`).
- The style guide marks the first-page header, the title, the Abstract and the copyright notice as required. Outside the body, their order is required too (`rfc7322-required-elements`).
- Reference lists must say whether each reference is normative or informative (`rfc7322-references-normative-informative`).
- A document that uses the RFC 2119 key words must cite RFC 2119 as a normative reference (`rfc7322-requirements-language`). This applies only when a document chooses those key words; it does not require them.
- The xml2rfc v3 vocabulary is defined from a RELAX NG schema. It holds a document's metadata in `<front>` (`rfc7991-front-matter-metadata`) and gives block elements anchors that cross-references can link to (`rfc7991-anchor-attribute`).
- RFC 2119's imperatives must be used with care and sparingly: only where they are required for interoperation or to limit harm (`rfc2119-use-sparingly`).

**W3C.**
- The QA Framework *requires* three things of a specification:
  - a conformance clause (`w3c-qa-conformance-clause`);
  - a defined scope (`w3c-qa-define-scope`), which contains no requirements (`w3c-qa-no-requirements-in-scope`);
  - conformance requirements written in one consistent style, with an explanation of how to tell them apart from other text (`w3c-qa-consistent-requirement-style`).
- RFC 2119 key words are one *technique* for meeting that last requirement (`w3c-qa-rfc2119-technique`). Requirements are usually set off with distinctive formatting (`w3c-qa-distinctive-formatting`); keyword case belongs to `requirement-keywords`.
- Its Good Practices (SHOULD strength) ask a specification to say how normative content is told from informative content (`w3c-qa-distinguish-normative`) and to write test assertions (`w3c-qa-test-assertions`).
- The W3C Manual of Style:
  - informative material is clearly distinguished from normative material (`w3c-mos-distinguish-informative`);
  - an informative section says so at its start (`w3c-mos-label-each-section`);
  - editors must not make any figure, example or note normative (`w3c-mos-examples-never-normative`);
  - revisions must not break links into the document (`w3c-mos-dont-break-links`).
- WCAG 2.2:
  - its examples and notes are declared informative (`wcag-examples-notes-informative`);
  - each guideline carries testable success criteria (`wcag-success-criteria-testable`);
  - each criterion has a number and a short name (`wcag-sc-number-and-short-name`).
- The W3C Process:
  - a revised Working Draft must document its substantive changes publicly (`w3c-process-document-substantive-changes`);
  - a report's status section should explain or link to its significant changes (`w3c-process-status-explains-changes`).

**Diátaxis.**
- Documentation takes four forms: tutorials, how-to guides, reference and explanation (`diataxis-four-forms`).
- Reference is neutral description that links out to how-to guides and explanation (`diataxis-reference-link-out`). It is useful when it is consistent (`diataxis-reference-consistent`).
- A how-to guide links to explanation instead of stopping for it (`diataxis-how-to-link-out`).
- Explanation is kept closely bounded (`diataxis-explanation-bounded`).

This is the closest outside parallel to the cookbook's split into `rules`, `how-to` and `rationale`.

**Google and Microsoft style guides.**
- Google:
  - use one unique H1 per page (`google-unique-h1`);
  - don't skip heading levels (`google-no-skipped-heading-levels`);
  - give every item in a bulleted list the same structure (`google-bulleted-lists`).
- Microsoft:
  - organise text into discrete components that can be scanned (`ms-discrete-components`);
  - lead with what matters most (`ms-lead-with-most-important`);
  - keep a list to between two and, if possible, seven items (`ms-list-length`).

**Rules with no outside support.**
- `gf-title-heading` (`gf-title-heading-prior`): the sources support exactly one H1 per page (`google-unique-h1`, `markdownlint-md025-front-matter-title`). None requires the H1 to match the front-matter `title`. markdownlint's default treats a front-matter title *as* the H1, so the draft's pattern of a title plus a matching H1 is reported unless the option is turned off.
- `gf-rfc-keywords` (`gf-rfc-keywords-prior`): the sources require a consistent style for requirements that readers can tell apart (`w3c-qa-consistent-requirement-style`, a W3C Requirement). They offer RFC 2119 key words only as one technique for it (`w3c-qa-rfc2119-technique`, `rfc7322-requirements-language`). So the structural part, that requirements carry a normative keyword, is supported at SHOULD strength, not MUST. The clause "bold or uppercase" is about keyword case, which belongs to `requirement-keywords` and is not judged here.

## The expert's view

**What people get wrong.**
- **Mixing requirement and rationale.** NASA names "a paragraph that contains both requirements and rationale" as a failure (`nasa-requirements-and-rationale-mixed`). The fix is one thought per statement, with the rationale stated alongside it (`nasa-rationale-accompanies-requirement`).
- **Normative-sounding informative text.** W3C editors warn against informative sections whose language sounds normative (`w3c-qa-avoid-normative-sounding-informative`).
- **Overusing keywords.** RFC 2119 says its key words must not be used to impose a method that is not actually required (`rfc2119-no-method-imposition`). A rule should carry an obligation only where the obligation matters (`rfc2119-use-sparingly`).
- **Positional rule numbers.** The ASVS maintainers report that positional identifiers become problematic as a standard grows and changes (`asvs-positional-ids-problematic`). Stable names avoid that.
- **Commit logs as change history.** Using commit-log diffs as a changelog is a mistake, because they are full of noise; a change history is curated for humans (`keepachangelog-commit-diffs-bad`).
- **How a reader sees a standard.** A practitioner reads normative text as the standard itself, and everything else as background (`fowler-normative-part-of-standard`). That is why the difference must be visible on the page.

**Verdict notes.** The following is written for the owner and for stage 3.

*Supported rules.*
- `gf-frontmatter-complete`, `gf-type-field`, `gf-summary-statement`, `gf-structured-guidance` and `gf-named-rules` are supported at their stated strength.
- `gf-change-history` is supported for the practice of documenting each version's changes, which the W3C Process requires and Keep a Changelog recommends. Its form, a table placed at the end with these four columns, is the cookbook's own.
- `conv-roled-parts`, `conv-named-rules`, `conv-one-source-per-topic`, `conv-research-cited` and `conv-rationale-to-references` state no keyword. They are supported as practices: label each part, write one rule to a bullet, link instead of duplicating, link evidence to each rule, and keep rationale apart from the rule.

*Unsupported rules, with the strength the sources do support.*
- `gf-title-heading`: the sources support one H1 per page at SHOULD strength. Nothing supports matching it to the title.
- `gf-rfc-keywords`: SHOULD for a consistent, distinguishable requirement style using normative keywords. Keyword case belongs to `requirement-keywords`.
- `gf-roled-parts`: SHOULD for labelling normative and informative parts and separating reference, how-to and explanation.
- `gf-research-folder` and `gf-rule-cites-research`: SHOULD for linking evidence to each recommendation.

*Rules no source speaks to.* `gf-compliance-section`, `gf-triggers-field` and the six `conv-*` rules about tool behaviour. Owner ruling Q12 applies to the `conv-*` findings: `conventions.md` changes in stage 5, not now.

**New rules the research supports.** No current rule covers these. Each is listed with the strength its sources support:
- `conformance-and-scope-statement` (MUST): a conformance clause and a scope section, with no requirements inside the scope (`w3c-qa-conformance-clause`, `w3c-qa-define-scope`, `w3c-qa-no-requirements-in-scope`).
- `mark-normative-and-informative` (SHOULD): `w3c-qa-distinguish-normative`, `w3c-mos-distinguish-informative`, `w3c-qa-avoid-normative-sounding-informative`, `rfc7322-references-normative-informative`, `fowler-normative-part-of-standard`.
- `examples-are-non-normative` (MUST NOT make an example normative): `w3c-mos-examples-never-normative`, `wcag-examples-notes-informative`. The Manual of Style says it holds no formal requirements, but WCAG applies the practice in its own normative text.
- `one-requirement-per-rule` (SHOULD): `nasa-one-thought-per-requirement`, `agree-specific-unambiguous`, `nasa-requirements-and-rationale-mixed`.
- `rules-are-verifiable` (SHOULD): `nasa-requirements-verifiable`, `iom-compliance-evaluable`, `w3c-qa-test-assertions`, `wcag-success-criteria-testable`.
- `rule-states-when-it-applies` (SHOULD): `iom-standardized-form-and-circumstances`.
- `rule-has-rationale` (SHOULD): `nasa-rationale-accompanies-requirement`, `iom-evidence-per-recommendation`.
- `stable-rule-identifiers` (SHOULD): `w3c-mos-dont-break-links`, `asvs-versioned-identifiers`, `asvs-positional-ids-problematic`.
- `normative-keywords-only-where-required` (MUST, per RFC 2119): `rfc2119-use-sparingly`, `rfc2119-no-method-imposition`. This may belong to `requirement-keywords`.
- `single-h1` (SHOULD): `google-unique-h1`, `markdownlint-md025-front-matter-title`.
- `no-skipped-heading-levels` (SHOULD): `google-no-skipped-heading-levels`.
- `keep-rule-lists-short` (SHOULD, if possible): `ms-list-length`. The source is about lists in general.
- `change-history-newest-first` (SHOULD): `keepachangelog-latest-first`, `keepachangelog-commit-diffs-bad`.
- `released-versions-immutable` (MUST NOT modify a released version): `semver-released-immutable`.
- `check-guidelines-automatically` (SHOULD): `writethedocs-docs-as-code`, `astro-schema-enforces-frontmatter`, `markdownlint-md043-required-headings`, `vale-existence-check`.
