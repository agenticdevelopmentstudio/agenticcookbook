# Research fallback run: guideline-formatting

`team_probe.py researchteam`: ok false, "missing distributions: PyYAML, aiohttp, mcp, websockets". The research ran as one fresh Opus Agent (general-purpose) with the `research` prompt exactly as `write_brief.py prompt research` printed it. Its reply, verbatim:

---

I wrote both research files, but the exact validate line does not print `Research passed.` It stops before checking anything:

```
✗ .../cookbook/guidelines/cookbook/authoring/guideline-formatting: not an artifact source folder (no artifact.json)
```

The topic is new, so its folder holds only `research/`, and `research_only` refuses any folder without an `artifact.json`. I didn't create one because the task allows only the two files. To check the content anyway, I ran cookr's own `research._findings` on the folder in an inline `python -c`, with no rules attached. It reported no findings: claim fields, citations, independence values, ids, verdicts and the research.md headings all pass. The exact line will pass only once stage 3 adds `artifact.json`, or the validator accepts a research-only folder.

The two files are not committed; that is left to whoever integrates the topic.

**Files**
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/guideline-formatting/research/research.json`
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/guideline-formatting/research/research.md`

**Claims per question (84 total, 33 sources)**
- best-practices: 20 (3 of them `-prior`)
- known-solutions: 20 (7 `-prior`)
- platform-guidelines: 38 (2 `-prior`)
- experts-view: 6

Every claim is `single`, because no two independent pages hold the same quoted words. Corroboration is named in each trust basis instead.

**Verdicts**
- gf-frontmatter-complete: supported (rfc7322-required-elements, rfc7991-front-matter-metadata, json-schema-required, json-schema-no-additional-properties, astro-schema-enforces-frontmatter, remark-lint-frontmatter-schema)
- gf-type-field: supported (json-schema-enum, diataxis-four-forms)
- gf-title-heading: unsupported (gf-title-heading-prior, google-unique-h1, markdownlint-md025-front-matter-title, markdownlint-md041-first-line-heading, markdownlint-custom-rules)
- gf-summary-statement: supported (rfc7322-abstract-required, rfc7322-abstract-complete-in-itself, ms-lead-with-most-important)
- gf-structured-guidance: supported (w3c-qa-consistent-requirement-style, ms-discrete-components, google-bulleted-lists, agree-key-recommendations-identifiable, diataxis-reference-consistent)
- gf-rfc-keywords: unsupported (gf-rfc-keywords-prior, w3c-qa-rfc2119-technique, w3c-qa-consistent-requirement-style, w3c-qa-distinctive-formatting, rfc7322-requirements-language, rfc2119-use-sparingly)
- gf-change-history: supported (w3c-process-document-substantive-changes, w3c-process-status-explains-changes, keepachangelog-entry-per-version, keepachangelog-date-displayed, markdownlint-md043-required-headings)
- gf-compliance-section: unsupported (gf-compliance-section-prior)
- gf-triggers-field: unsupported (gf-triggers-field-prior, json-schema-enum)
- gf-roled-parts: unsupported (gf-roled-parts-prior, w3c-qa-distinguish-normative, w3c-mos-label-each-section, diataxis-four-forms, diataxis-reference-link-out, diataxis-how-to-link-out, diataxis-explanation-bounded)
- gf-named-rules: supported (w3c-qa-consistent-requirement-style, nasa-uniquely-referenced, nasa-one-thought-per-requirement, wcag-sc-number-and-short-name, rfc7991-anchor-attribute, vale-markup-aware-scopes)
- gf-research-folder: unsupported (gf-research-folder-prior, iom-evidence-per-recommendation, agree-explicit-link-to-evidence, iom-transparent-process)
- gf-rule-cites-research: unsupported (gf-rule-cites-research-prior, iom-evidence-per-recommendation, agree-explicit-link-to-evidence)
- conv-roled-parts: supported (w3c-qa-distinguish-normative, w3c-mos-label-each-section, diataxis-four-forms)
- conv-named-rules: supported (nasa-one-thought-per-requirement, nasa-uniquely-referenced, w3c-qa-consistent-requirement-style)
- conv-one-source-per-topic: supported (govuk-dont-duplicate, diataxis-how-to-link-out)
- conv-research-cited: supported (iom-evidence-per-recommendation, agree-explicit-link-to-evidence)
- conv-legacy-keeps-working: unsupported (conv-legacy-keeps-working-prior)
- conv-role-values: unsupported (conv-role-values-prior)
- conv-no-roles-under-reviewing: unsupported (conv-no-roles-under-reviewing-prior)
- conv-roled-artifact-complete: unsupported (conv-roled-artifact-complete-prior)
- conv-four-skills: unsupported (conv-four-skills-prior)
- conv-skill-names: unsupported (conv-skill-names-prior)
- conv-rationale-to-references: supported (nasa-rationale-accompanies-requirement, nasa-requirements-and-rationale-mixed, diataxis-explanation-bounded, fowler-normative-part-of-standard)
- conformance-and-scope-statement: new, MUST (w3c-qa-conformance-clause, w3c-qa-define-scope, w3c-qa-no-requirements-in-scope)
- mark-normative-and-informative: new, SHOULD (w3c-qa-distinguish-normative, w3c-mos-distinguish-informative, w3c-qa-avoid-normative-sounding-informative, rfc7322-references-normative-informative, fowler-normative-part-of-standard)
- examples-are-non-normative: new, MUST NOT (w3c-mos-examples-never-normative, wcag-examples-notes-informative)
- one-requirement-per-rule: new, SHOULD (nasa-one-thought-per-requirement, agree-specific-unambiguous, nasa-requirements-and-rationale-mixed)
- rules-are-verifiable: new, SHOULD (nasa-requirements-verifiable, iom-compliance-evaluable, w3c-qa-test-assertions, wcag-success-criteria-testable)
- rule-states-when-it-applies: new, SHOULD (iom-standardized-form-and-circumstances)
- rule-has-rationale: new, SHOULD (nasa-rationale-accompanies-requirement, iom-evidence-per-recommendation)
- stable-rule-identifiers: new, SHOULD (w3c-mos-dont-break-links, asvs-versioned-identifiers, asvs-positional-ids-problematic)
- normative-keywords-only-where-required: new, MUST (rfc2119-use-sparingly, rfc2119-no-method-imposition)
- single-h1: new, SHOULD (google-unique-h1, markdownlint-md025-front-matter-title)
- no-skipped-heading-levels: new, SHOULD (google-no-skipped-heading-levels)
- keep-rule-lists-short: new, SHOULD (ms-list-length)
- change-history-newest-first: new, SHOULD (keepachangelog-latest-first, keepachangelog-commit-diffs-bad)
- released-versions-immutable: new, MUST NOT (semver-released-immutable)
- check-guidelines-automatically: new, SHOULD (writethedocs-docs-as-code, astro-schema-enforces-frontmatter, markdownlint-md043-required-headings, vale-existence-check)

**Findings that change what stage 3 writes**
- **Weaker than stated:** sources support gf-rfc-keywords, gf-roled-parts, gf-research-folder and gf-rule-cites-research only at SHOULD, not the MUST they state. research.md notes the supported strength for each.
- **No outside source:** gf-compliance-section, gf-triggers-field and the six `conv-*` rules that describe tool behaviour have no outside support. Under ruling Q12, the `conv-*` findings are recorded now and `conventions.md` changes in stage 5.
- **Title against the lint default:** gf-title-heading conflicts with markdownlint's default, which treats a front-matter title as the H1. A title plus a matching H1 is therefore reported as two top-level headings.
- **Open questions and limitations:** each owner decision is a separate entry under `open_questions`, including whether to keep each MUST and whether to adopt each new rule. Under `limitations`:
  - Keyword case and severity were left to the `requirement-keywords` topic.
  - The ISO Directives and the ACM Queue article could not be fetched (HTTP 403).
  - The clinical guideline standards (IOM, AGREE II) are applied to software guidelines by inference.
