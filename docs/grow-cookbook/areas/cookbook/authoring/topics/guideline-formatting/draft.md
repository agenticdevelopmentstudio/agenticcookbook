---
id: 99eb40d3-98a6-4213-9fee-f8a62694dba4
title: "Guideline Formatting"
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-21
modified: 2026-11-21
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "How a cookbook guideline is built: frontmatter, an H1 and its summary, roled parts, named rules that cite their research, and a change history."
platforms: []
tags:
  - cookbook
  - authoring
  - guideline
  - formatting
  - research
depends-on: []
related:
  - 2795e06d-b081-43ac-97d9-20ff3d0a93b1
  - e48a04d7-c479-427d-9d8e-fe9e9b990c77
  - 456f23bd-4523-47e8-9541-073ac046f2ad
  - 1b7b83f9-3b8a-46f7-81b7-9a55291a23a2
references:
  - https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/
  - https://www.nationalacademies.org/read/13058/chapter/7
  - https://www.nationalacademies.org/read/13058/chapter/3
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3001530
  - https://keepachangelog.com/en/1.1.0/
  - https://www.writethedocs.org/guide/docs-as-code/
  - https://docs.publishing.service.gov.uk/manual/docs-style-guide.html
  - https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md
  - https://github.com/DavidAnson/markdownlint/blob/main/doc/CustomRules.md
  - https://docs.vale.sh/checks/existence
  - https://docs.vale.sh/topics/scopes
  - https://json-schema.org/understanding-json-schema/reference/object
  - https://json-schema.org/understanding-json-schema/reference/enum
  - https://github.com/JulianCataldo/remark-lint-frontmatter-schema
  - https://docs.astro.build/en/guides/content-collections/
  - https://semver.org/
  - https://github.com/OWASP/ASVS/blob/master/README.md
  - https://www.rfc-editor.org/rfc/rfc7322
  - https://www.rfc-editor.org/rfc/rfc2119
  - https://www.rfc-editor.org/rfc/rfc7991
  - https://www.w3.org/TR/qaframe-spec/
  - https://www.w3.org/guide/manual-of-style/
  - https://www.w3.org/TR/WCAG22/
  - https://www.w3.org/policies/process/
  - https://diataxis.fr/
  - https://diataxis.fr/reference/
  - https://diataxis.fr/how-to-guides/
  - https://diataxis.fr/explanation/
  - https://developers.google.com/style/headings
  - https://developers.google.com/style/lists
  - https://learn.microsoft.com/en-us/style-guide/scannable-content/
  - https://learn.microsoft.com/en-us/style-guide/scannable-content/lists
  - https://www.martinfowler.com/bliki/StandardsSpeak.html
approved-by: ""
approved-date: ""
triggers: []
---

# Guideline Formatting

A cookbook guideline carries complete frontmatter with `type: guideline`, opens with a summary statement under an H1 that matches its title, states each requirement as a named rule with an RFC 2119 keyword that ends by citing the research claims it stands on, and ends with a change history. A roled guideline gives every part but the intro and the history a role, and a guideline not listed in `cookbook/research-exempt.json` keeps the research it was written from in its folder.

Following this guideline means keeping every absolute rule in `## Rules`, and keeping every recommended rule there or saying why not; the keywords mean what [adc.guideline.cookbook.authoring.requirement-keywords](cookbook:456f23bd-4523-47e8-9541-073ac046f2ad) says they mean. Only `## Rules` is normative. The reviewer and build parts restate its rules as checks, and every other part is informative.

This guideline covers the structure of a guideline artifact in this cookbook: its frontmatter, headings, summary, parts and their roles, named rules and their research citations, and its change history. The trigger vocabulary belongs to [adc.guideline.cookbook.authoring.activity-triggers](cookbook:1b7b83f9-3b8a-46f7-81b7-9a55291a23a2), and the shape of the research document to [adc.guideline.researching.evidence.research-results-document](cookbook:2795e06d-b081-43ac-97d9-20ff3d0a93b1).

## Rules

- **gf-frontmatter-complete**: All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`: id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related and references. (claims: rfc7322-required-elements, rfc7991-front-matter-metadata, json-schema-required, remark-lint-frontmatter-schema)
- **no-domain-field**: The meta MUST NOT carry a `domain` field. (claim: json-schema-no-additional-properties)
- **gf-type-field**: The `type` field MUST be `guideline`. (claims: json-schema-enum, diataxis-four-forms)
- **gf-title-heading**: The first H1 heading MUST match the frontmatter `title` field exactly.

  **Applies when:** always. (claim: gf-title-heading-prior)
- **single-h1**: A guideline SHOULD have one unique level-1 heading. (claims: google-unique-h1, markdownlint-md025-front-matter-title)
- **no-skipped-heading-levels**: A guideline SHOULD NOT skip levels of the heading hierarchy. (claim: google-no-skipped-heading-levels)
- **gf-summary-statement**: A summary statement MUST appear immediately after the H1 heading, ahead of the body. (claims: rfc7322-abstract-required, rfc7322-required-elements)
- **summary-complete-in-itself**: The summary statement SHOULD be complete in itself, a concise overview a reader can take without the body. (claim: rfc7322-abstract-complete-in-itself)
- **summary-leads-with-most-important**: The summary statement SHOULD put the most important information first. (claim: ms-lead-with-most-important)
- **conformance-and-scope-statement**: A guideline SHOULD include a statement describing what is required of those who follow it. (claim: w3c-qa-conformance-clause)
- **guideline-defines-scope**: A guideline SHOULD define its scope. (claim: w3c-qa-define-scope)
- **scope-holds-no-requirements**: A guideline's scope statement SHOULD NOT include any requirements. (claim: w3c-qa-no-requirements-in-scope)
- **gf-structured-guidance**: The guideline MUST write its requirements in one consistent style that tells them apart from the rest of its text. (claim: w3c-qa-consistent-requirement-style)
- **guidance-in-discrete-components**: A guideline SHOULD organise its guidance into discrete components: bulleted lists, tables or subsections. (claim: ms-discrete-components)
- **list-items-share-one-structure**: Every item of a list SHOULD have the same structure, where possible. (claims: google-bulleted-lists, diataxis-reference-consistent)
- **keep-rule-lists-short**: A list SHOULD have at least two items and, if possible, no more than seven. (claim: ms-list-length)
- **key-rules-identifiable**: A guideline's key rules SHOULD be easy to identify. (claim: agree-key-recommendations-identifiable)
- **gf-rfc-keywords**: Requirements within the guideline MUST use RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) to indicate obligation levels. Keywords MUST be bold or uppercase when used normatively.

  **Applies when:** the guideline contains requirements or rules (not purely informational content). (claim: gf-rfc-keywords-prior)
- **normative-keywords-only-where-required**: A rule SHOULD use the RFC 2119 keywords with care and sparingly, only where they are required for interoperation or to limit harmful behaviour. (claim: rfc2119-use-sparingly)
- **keywords-impose-no-method**: A rule MUST NOT use a normative keyword to impose a particular method where the method is not required. (claim: rfc2119-no-method-imposition)
- **gf-named-rules**: Every bullet in a `rules` part MUST be a named rule: `- **kebab-name**: … MUST|SHOULD|MAY …`, its name unique in the guideline and its obligation an RFC 2119 keyword. (claims: w3c-qa-consistent-requirement-style, wcag-sc-number-and-short-name, rfc7991-anchor-attribute, vale-markup-aware-scopes)
- **conv-named-rules**: Each rule SHOULD be stated so that it can be uniquely referenced, by its name. (claims: nasa-uniquely-referenced, w3c-qa-consistent-requirement-style)
- **one-requirement-per-rule**: A rule SHOULD express only one thought. (claims: nasa-one-thought-per-requirement, nasa-requirements-and-rationale-mixed)
- **rule-specific-and-unambiguous**: A rule SHOULD be specific and unambiguous. (claim: agree-specific-unambiguous)
- **rules-are-verifiable**: A rule SHOULD be worded so that compliance with it can be evaluated, by test, demonstration, inspection or analysis. (claims: nasa-requirements-verifiable, iom-compliance-evaluable, w3c-qa-test-assertions, wcag-success-criteria-testable)
- **rule-in-standardized-form**: A rule SHOULD be written in a standardized form that states precisely the action it requires. (claim: iom-standardized-form-and-circumstances)
- **rule-states-when-it-applies**: A rule SHOULD state the circumstances in which it applies. (claim: iom-standardized-form-and-circumstances)
- **rule-has-rationale**: Each rule SHOULD be accompanied by an intelligible rationale, including its assumptions and a summary of the relevant evidence and its gaps. (claims: nasa-rationale-accompanies-requirement, iom-evidence-per-recommendation)
- **conv-rationale-to-references**: A rule's rationale SHOULD be kept in a closely bounded rationale part, out of the rule's bullet. (claims: nasa-rationale-accompanies-requirement, nasa-requirements-and-rationale-mixed, diataxis-explanation-bounded, fowler-normative-part-of-standard)
- **stable-rule-identifiers**: A rule's name SHOULD stay the same across revisions. (claims: w3c-mos-dont-break-links, asvs-versioned-identifiers)
- **no-positional-rule-identifiers**: A rule SHOULD NOT be identified by its position. (claims: asvs-versioned-identifiers, asvs-positional-ids-problematic)
- **gf-roled-parts**: A roled guideline MUST give every part but the intro and the history a `role` in `artifact.json`, one of `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`, and MUST have at least one part of each of `rules`, `review-focus`, `review-bar` and `build-bar`. It sets no `routes` and no `hosts/`, and does not live under `guidelines/reviewing/`.

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

  **Applies when:** any part of the guideline carries a `role`. (claim: gf-roled-parts-prior)
- **conv-roled-parts**: Each part of a guideline SHOULD be labelled with the form of documentation it holds. (claims: w3c-qa-distinguish-normative, diataxis-four-forms)
- **informative-part-says-so**: Each informative part of a guideline SHOULD say so at its start. (claim: w3c-mos-label-each-section)
- **mark-normative-and-informative**: A guideline SHOULD clearly distinguish its normative content from its informative content. (claims: w3c-qa-distinguish-normative, w3c-mos-distinguish-informative, fowler-normative-part-of-standard)
- **informative-text-not-normative-sounding**: An informative part SHOULD NOT use language that sounds normative. (claim: w3c-qa-avoid-normative-sounding-informative)
- **examples-are-non-normative**: A guideline SHOULD NOT make any example, diagram or note normative. (claims: w3c-mos-examples-never-normative, wcag-examples-notes-informative)
- **references-marked-normative-or-informative**: A guideline's reference list SHOULD say whether each reference is normative or informative. (claim: rfc7322-references-normative-informative)
- **conv-roled-artifact-complete**: A roled artifact gives every other part a role, names each rule in its `rules` parts (`- **kebab-name**: … MUST|SHOULD|MAY …`), and sets no `routes` and no `hosts/`. `cookr validate` lists what is wrong. (claim: conv-roled-artifact-complete-prior)
- **conv-role-values**: Roles MUST be used as follows: A part may carry a `role` in `artifact.json`: `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`. The intro and the history never carry one. An artifact with no role is compiled as it always was. (claim: conv-role-values-prior)
- **conv-no-roles-under-reviewing**: Roles MUST be placed as follows: A guideline with roles may live under any use-case folder but `guidelines/reviewing/`, which is folded into each topic and never roled; a principle may carry roles too, an ingredient or a recipe never. (claim: conv-no-roles-under-reviewing-prior)
- **conv-four-skills**: A roled artifact MUST compile as follows: It compiles to four skills, each the intro plus the parts of its roles:

  | Skill | Roles | Name |
  |---|---|---|
  | builder | `rules`, `how-to`, `examples` | `<use-case>-<tail>` |
  | build-verifier | `build-bar` | `verifying-build-<tail>` |
  | reviewer | `rules`, `review-focus` | `reviewing-<tail>` |
  | review-verifier | `review-bar` | `verifying-review-<tail>` |

  (claim: conv-four-skills-prior)
- **conv-skill-names**: The compiled skills MUST be named as follows: The builder keeps the name the artifact would have unroled; the other three replace only its use case: `guidelines/planning/data/t` gives `planning-data-t` and `reviewing-data-t`, and `principles/t`, which has no use case, keeps its type: `principle-t` and `reviewing-principle-t`. Two artifacts whose skills would share a name, after a long name is cut to the hosts' limit, are refused, each naming the other. (claim: conv-skill-names-prior)
- **conv-legacy-keeps-working**: The cookbook MUST keep this true: An artifact written before this design keeps working as it is: an unroled artifact compiles as it always did, and one with no research is listed in `cookbook/research-exempt.json` until its research is written. (claim: conv-legacy-keeps-working-prior)
- **gf-research-folder**: The guideline MUST keep the research it was written from in `research/` in its folder: `research/research.json`, in the shape of the research-results document (`guidelines/researching/evidence/research-results-document`), and `research/research.md`, the same, readable, under the four question headings in this order: `## Best practices`, `## Known solutions`, `## Platform guidelines`, `## The expert's view`.

  Each claim in `research.json`'s `claims` list is the per-claim record: `id` (kebab-case, unique), `question` (`best-practices`, `known-solutions`, `platform-guidelines` or `experts-view`), `claim`, `citations` (each with `title`, `author`, `publisher`, `date`, `url`, `accessed`), `source_type`, `quote`, `generated_by`, `query`, `trust` (`{"score": 0-100, "basis"}`) and `independence` (`multi-independent`, `single` or `uncorroborated`). The `verdicts` list gives each rule checked a verdict, `supported`, `contradicted`, `unsupported` or `new`, and the claims it rests on, at least one; every claim a rule cites MUST be named by a verdict. A rule the research cannot support is recorded as a claim itself, its source the cookbook's own text at the topic's base commit, with an `unsupported` verdict (`contradicted` when the research finds against it) naming that claim; a rule kept for the owner cites it, and `cookr validate` passes it with an `owner-decides` warning naming the rule and the claim.

  **Applies when:** always, unless the guideline is listed in `cookbook/research-exempt.json` as a topic written before research-first whose research is still to come. (claim: gf-research-folder-prior)
- **gf-rule-cites-research**: Each named rule MUST cite the claims of its research it stands on, once, at the end of its bullet: `(claim: <id>)`, or `(claims: <id>, <id>)` for several. Nothing follows the citation. Every id cited MUST be a claim in `research/research.json`. The citation names the claim, never the document (`cite-the-claim-not-the-document`), so a reader can follow a rule to the quote and source behind it.

  ```markdown
  - **index-foreign-keys**: Every foreign-key column MUST have an index. (claims: fk-index-postgres, fk-index-sqlite)
  ```

  **Applies when:** the guideline has a `research/` folder. In a roled guideline the named rules are its `rules` parts' bullets; in an unroled one, every named bullet that states MUST, SHOULD or MAY outside the intro and the history. (claim: gf-rule-cites-research-prior)
- **conv-research-cited**: Each rule SHOULD have an explicit link to its supporting evidence. (claims: agree-explicit-link-to-evidence, iom-evidence-per-recommendation)
- **conv-one-source-per-topic**: A guideline SHOULD NOT duplicate what existing documentation already says. (claim: govuk-dont-duplicate)
- **link-instead-of-repeating**: A guideline SHOULD link to material held in another document rather than contain it. (claims: diataxis-how-to-link-out, diataxis-reference-link-out)
- **gf-change-history**: The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary. (claim: w3c-process-document-substantive-changes)
- **change-history-entry-per-version**: The change history SHOULD have an entry for every version. (claim: keepachangelog-entry-per-version)
- **change-history-explains-changes**: Each change history entry SHOULD explain, or link to an explanation of, the significant changes from the previous version. (claim: w3c-process-status-explains-changes)
- **change-history-dates-each-version**: The change history SHOULD show the date of each version. (claim: keepachangelog-date-displayed)
- **change-history-newest-first**: The change history SHOULD put the latest version first. (claim: keepachangelog-latest-first)
- **change-history-not-commit-log**: A change history entry SHOULD NOT be a commit-log diff. (claim: keepachangelog-commit-diffs-bad)
- **released-versions-immutable**: Once a version of a guideline is released, its contents MUST NOT be modified. (claim: semver-released-immutable)
- **gf-compliance-section**: The guideline MAY include a `## Compliance` section listing evaluated compliance checks and their status. This is recommended when the guideline is referenced by compliance checks in other categories.

  **Applies when:** the guideline is referenced by one or more compliance check definitions. (claim: gf-compliance-section-prior)
- **gf-triggers-field**: The `triggers` field SHOULD be present in guideline frontmatter. It MUST be a YAML list of trigger names from the canonical taxonomy defined in `introduction/trigger-guide.md`. Empty list `[]` is acceptable for guidelines not yet classified.

  **Applies when:** always. (claim: gf-triggers-field-prior)
- **check-guidelines-automatically**: A guideline's structure SHOULD be checked automatically, with the same kind of tools and tests as code. (claims: writethedocs-docs-as-code, astro-schema-enforces-frontmatter, markdownlint-md043-required-headings, vale-existence-check)

## How to keep the rules

This part is informative: it describes one way to keep the rules above.

- **Start from the frontmatter.** Fill every required field, set `type: guideline`, give the artifact a new UUID as its `id`, and leave `domain` out. Leave `approved-by` and `approved-date` as `""` until approval stamps them. Set `triggers` to names from `guide/introduction/trigger-guide.md`, or `[]` when none fits.
- **Write the H1 and the summary next.** Copy the frontmatter `title` into the H1 word for word, then write the summary statement directly under it: the action a reader takes, first, in a paragraph that stands without the rest of the doc.
- **Say what conforming means, and what the guideline covers.** After the summary, one paragraph names the normative part and how its keywords are read; another states the scope as a plain description, leaving every requirement to the rules.
- **Lay out the parts in order.** The headings are `## Rules`, `## How to keep the rules`, `## Examples`, `## What a reviewer looks for`, `## A complete review must establish`, `## A build must establish`, `## Rationale`, `## References` and `## Change History`. `cookr roles set` gives each a role after `cookr convert`; the intro and the history carry none. Each informative part opens with a sentence saying it is informative.
- **Write one rule to a bullet.** Name it in kebab-case, state one requirement with one RFC 2119 keyword in uppercase, and end it with its citation. A rule's subject usually says where it applies; an `**Applies when:**` line says so when the subject alone does not. The why goes in the rationale part.
- **Choose the keyword from the evidence.** A rule reads truest at the strength of the weakest claim it cites: a claim that says must supports a MUST, and a claim that says should, or that a second check found only partly supported, supports a SHOULD.
- **Cite the claim, at the end.** Write `(claim: <id>)` or `(claims: <id>, <id>)` as the bullet's last text, with nothing after it, not even a full stop. Every id is a claim in `research/research.json` that some verdict names.
- **Indent what continues a rule.** A rule that needs a second paragraph, a table or a code block indents those lines under its bullet, so they stay part of it, and the citation still ends the last line.
- **Write the build bar from the rules.** It has exactly one line per named rule, `` - `rule-name`: … ``, and no line naming anything else.
- **Keep names once they ship.** A rule's name is how other docs and reviews link to it; a rename comes only with a new version, and rules are never numbered by position.
- **Let the tools check it.** `cookr roles check <folder>` reports unnamed, duplicate and uncited rules and citations not at the end, and `cookr validate` checks the frontmatter, links, research and the index.
- **Record each version.** `cookr bump <folder> --summary "..."` writes the version, the `modified` date and a row of the change history table, with the date and a summary a reader can follow.

## Examples

These examples are informative.

A rules part with two named rules, each citing its claims at its end:

```markdown
## Rules

- **index-foreign-keys**: Every foreign-key column MUST have an index. (claims: fk-index-postgres, fk-index-sqlite)
- **name-indexes-by-columns**: An index SHOULD be named for the table and columns it covers. (claim: index-naming-convention)
```

The build-bar lines that go with them, one per rule:

```markdown
## A build must establish

- `index-foreign-keys`: every foreign-key column has an index.
- `name-indexes-by-columns`: every index is named for its table and columns.
```

A rule that is not named, and one whose citation is not at its end, both of which `cookr roles check` reports:

```markdown
- Every foreign-key column MUST have an index. (claim: fk-index-postgres)
- **index-foreign-keys**: Every foreign-key column MUST have an index (claim: fk-index-postgres), on every table.
```

A change history row:

```markdown
| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-21 | Mike Fullerton | Initial creation |
```

## What a reviewer looks for

- Frontmatter missing a required field, carrying `domain`, with a `type` other than `guideline`, or with a `triggers` name not in the trigger guide.
- An H1 that differs from the `title`, more than one H1, or a skipped heading level.
- A summary that is not directly under the H1, that needs the body to make sense, or that buries the most important information.
- No statement of what following the guideline requires, no scope, or a scope that states a requirement.
- Requirements in no consistent style, guidance as unbroken prose, list items of mixed structure, overlong lists, or key rules that are hard to find.
- A bullet in a `rules` part that has no kebab-case name, states no RFC 2119 keyword, or shares its name with another rule.
- A rule that states more than one requirement, is vague or ambiguous, cannot be checked, does not state precisely the action it requires, or does not say when it applies.
- A rule with no rationale, or with its rationale written into its bullet.
- A keyword used where nothing requires it, or used to impose a method.
- A rule with no citation, a citation before its end, an id that is no claim in `research/research.json`, or a claim no verdict names.
- A missing `research/research.json` or `research/research.md`, or one not in the documented shape.
- A part without a role, a role not in the list, a role on the intro or the history, a roled guideline missing a `rules`, `review-focus`, `review-bar` or `build-bar` part, `routes` or `hosts/` set, or a roled guideline under `guidelines/reviewing/`.
- An informative part that does not say so at its start, sounds normative, or holds an example, diagram or note that reads as a requirement; a reference not marked normative or informative.
- A build bar with a missing line for a rule, two lines for one rule, or a line naming something that is not a rule.
- A rule renamed or numbered by position, or a released version's content changed, without a new version.
- Text that repeats what another document already says instead of linking to it.
- A change history that is not the last section, is missing a column, lacks a dated row for a version, has a row that does not explain its changes, is oldest-first, or is a commit-log dump.
- A `## Compliance` section that does not list evaluated checks and their status.
- Structure checked only by eye, where a schema, linter or `cookr` check could check it.

## A complete review must establish

- Every MUST rule is kept, with no exception: `gf-frontmatter-complete`, `no-domain-field`, `gf-type-field`, `gf-title-heading`, `gf-summary-statement`, `gf-structured-guidance`, `gf-rfc-keywords`, `keywords-impose-no-method`, `gf-named-rules`, `gf-roled-parts`, `conv-roled-artifact-complete`, `conv-role-values`, `conv-no-roles-under-reviewing`, `conv-four-skills`, `conv-skill-names`, `conv-legacy-keeps-working`, `gf-research-folder`, `gf-rule-cites-research`, `gf-change-history`, `released-versions-immutable`
- Every SHOULD rule is kept, or the review says why not: `single-h1`, `no-skipped-heading-levels`, `summary-complete-in-itself`, `summary-leads-with-most-important`, `conformance-and-scope-statement`, `guideline-defines-scope`, `scope-holds-no-requirements`, `guidance-in-discrete-components`, `list-items-share-one-structure`, `keep-rule-lists-short`, `key-rules-identifiable`, `normative-keywords-only-where-required`, `conv-named-rules`, `one-requirement-per-rule`, `rule-specific-and-unambiguous`, `rules-are-verifiable`, `rule-in-standardized-form`, `rule-states-when-it-applies`, `rule-has-rationale`, `conv-rationale-to-references`, `stable-rule-identifiers`, `no-positional-rule-identifiers`, `conv-roled-parts`, `informative-part-says-so`, `mark-normative-and-informative`, `informative-text-not-normative-sounding`, `examples-are-non-normative`, `references-marked-normative-or-informative`, `conv-research-cited`, `conv-one-source-per-topic`, `link-instead-of-repeating`, `change-history-entry-per-version`, `change-history-explains-changes`, `change-history-dates-each-version`, `change-history-newest-first`, `change-history-not-commit-log`, `gf-triggers-field`, `check-guidelines-automatically`
- Every MAY rule that is taken is kept as written: `gf-compliance-section`
- The build bar has exactly one line per named rule and no other line naming anything.

A review passes when it establishes every item above.

## A build must establish

- `gf-frontmatter-complete`: every required meta field is present.
- `no-domain-field`: the meta has no `domain` field.
- `gf-type-field`: `type` is `guideline`.
- `gf-title-heading`: the first H1 matches the frontmatter `title` exactly.
- `single-h1`: there is one unique level-1 heading.
- `no-skipped-heading-levels`: no heading level is skipped.
- `gf-summary-statement`: a summary statement appears immediately after the H1.
- `summary-complete-in-itself`: the summary is a concise overview that stands without the body.
- `summary-leads-with-most-important`: the summary puts the most important information first.
- `conformance-and-scope-statement`: the guideline says what following it requires.
- `guideline-defines-scope`: the guideline defines its scope.
- `scope-holds-no-requirements`: the scope statement holds no requirement.
- `gf-structured-guidance`: the requirements are written in one consistent style that sets them apart.
- `guidance-in-discrete-components`: the guidance is in bulleted lists, tables or subsections.
- `list-items-share-one-structure`: the items of each list share one structure where possible.
- `keep-rule-lists-short`: each list has at least two and, where possible, no more than seven items.
- `key-rules-identifiable`: the key rules are easy to find.
- `gf-rfc-keywords`: requirements use RFC 2119 keywords, in bold or uppercase when normative.
- `normative-keywords-only-where-required`: each keyword is used only where an obligation is required.
- `keywords-impose-no-method`: no keyword imposes a method that is not required.
- `gf-named-rules`: every bullet in a `rules` part is a named rule with a unique kebab-case name and an RFC 2119 keyword.
- `conv-named-rules`: each rule can be referenced uniquely by its name.
- `one-requirement-per-rule`: each rule expresses one thought.
- `rule-specific-and-unambiguous`: each rule is specific and unambiguous.
- `rules-are-verifiable`: compliance with each rule can be evaluated.
- `rule-in-standardized-form`: each rule is in the standard form and states precisely the action it requires.
- `rule-states-when-it-applies`: each rule states the circumstances in which it applies.
- `rule-has-rationale`: each rule has a rationale with its assumptions and its evidence.
- `conv-rationale-to-references`: rationale sits in a bounded rationale part, not in the rules' bullets.
- `stable-rule-identifiers`: rule names are unchanged across revisions.
- `no-positional-rule-identifiers`: no rule is identified by its position.
- `gf-roled-parts`: every part but the intro and the history has a role from the list, the four required roles are present, and no `routes` or `hosts/` is set.
- `conv-roled-parts`: each part is labelled with the form of documentation it holds.
- `informative-part-says-so`: each informative part says so at its start.
- `mark-normative-and-informative`: normative content is told apart from informative content.
- `informative-text-not-normative-sounding`: no informative part uses language that sounds normative.
- `examples-are-non-normative`: no example, diagram or note is normative.
- `references-marked-normative-or-informative`: each reference is marked normative or informative.
- `conv-roled-artifact-complete`: every other part has a role, each rule is named, and no `routes` or `hosts/` is set.
- `conv-role-values`: every `role` is one of the listed values, and the intro and history carry none.
- `conv-no-roles-under-reviewing`: no roled artifact is under `guidelines/reviewing/`, and no ingredient or recipe is roled.
- `conv-four-skills`: a roled artifact compiles to the builder, build-verifier, reviewer and review-verifier skills.
- `conv-skill-names`: the compiled skills are named as documented, and no two artifacts' skills share a name.
- `conv-legacy-keeps-working`: unroled artifacts compile as before, and unresearched ones are listed in `cookbook/research-exempt.json`.
- `gf-research-folder`: `research/research.json` and `research/research.md` are present in the documented shape, and every cited claim is named by a verdict.
- `gf-rule-cites-research`: each named rule ends with one citation of claims in `research/research.json`.
- `conv-research-cited`: each rule links explicitly to its evidence.
- `conv-one-source-per-topic`: the guideline does not repeat what existing documentation says.
- `link-instead-of-repeating`: material held in another document is linked to, not copied in.
- `gf-change-history`: the file ends with a `## Change History` table with Version, Date, Author and Summary columns.
- `change-history-entry-per-version`: every version has an entry.
- `change-history-explains-changes`: each entry explains or links to its significant changes.
- `change-history-dates-each-version`: each version's date is shown.
- `change-history-newest-first`: the latest version comes first.
- `change-history-not-commit-log`: no entry is a commit-log diff.
- `released-versions-immutable`: no released version's content is modified.
- `gf-compliance-section`: a `## Compliance` section, where present, lists evaluated compliance checks and their status.
- `gf-triggers-field`: `triggers` is present, a YAML list of names from the trigger guide, or `[]`.
- `check-guidelines-automatically`: the guideline's structure is checked by tools as code is.

## Rationale

This part is informative: it gives the reasons and sources behind the rules.

- **Frontmatter is the document's metadata, and a schema can check it.** RFC 7322 lists the elements every RFC carries and marks the required ones, and xml2rfc v3 holds a document's metadata in a front element ahead of the abstract. JSON Schema's `required` names the fields an object must have, `additionalProperties: false` refuses one the format forbids, such as `domain`, and `enum` holds a field such as `type` to a fixed set; remark-lint-frontmatter-schema applies such a schema to Markdown frontmatter. Diátaxis's four forms of documentation are why the type is a closed set.
- **Headings follow the documentation norms.** Google's style guide uses one unique level-1 heading per page and does not skip levels; markdownlint's MD025 treats a frontmatter title as the top-level heading, MD041 checks that a document has a title, and a custom rule can check what the built-ins lack, such as an H1 that equals the frontmatter title.
- **The summary comes first and stands alone.** RFC 7322 requires every RFC to have an abstract, complete in itself, and Microsoft's style guide leads with what is most important, since the first screen is what is most likely to be read.
- **A reader is told what conforming means and what is covered.** The W3C QA Framework describes a conformance clause as a high-level description of what is required of implementations, asks a specification to define its scope, and keeps requirements out of the scope section.
- **Rules are told apart from everything else.** The W3C QA Framework requires conformance requirements in a consistent style, explained so a reader can tell them apart. Microsoft's style guide organises text into discrete components to support scanning, Google's gives every item of a list the same structure where it can, and Microsoft keeps a list to between two and, if possible, seven items. Diátaxis finds reference useful when it is consistent, and AGREE II appraises a guideline on whether its key recommendations are easy to identify.
- **Keywords are a tool, not decoration.** RFC 2119 asks that its imperatives be used with care and sparingly, only where required for interoperation or to limit harm, and never to impose a method that is not required. The cookbook's own rule that requirements use the keywords, bold or uppercase, is kept for the owner: the W3C QA Framework requires a consistent, distinguishable style and gives the keywords as one technique for it.
- **A named rule can be referenced, checked and linked.** NASA's requirements checklist asks for one thought per statement, each uniquely referenceable, and flags a paragraph that holds both requirements and rationale; AGREE II asks that recommendations be specific and unambiguous. WCAG gives each success criterion a number and a short name, xml2rfc gives blocks anchors, and Vale can scope a check to list items. The W3C Manual of Style asks editors to be careful not to break links in revisions, and OWASP ASVS notes that its identifiers, which are positional, may change between versions, so a reference to one without its version becomes a problem as the standard grows and changes.
- **A rule is worded so compliance can be judged, and says what it asks and when.** NASA's checklist asks whether the system can be tested, demonstrated, inspected or analysed against each requirement; the IOM's standard for trustworthy guidelines asks that strong recommendations be worded so compliance can be evaluated, in a standardized form that states precisely the action and the circumstances in which it applies; the W3C QA Framework describes test assertions as measurable or testable statements; and WCAG provides testable success criteria for each guideline.
- **Each rule carries its reasons and its evidence, kept apart from it.** NASA's checklist asks that each requirement be accompanied by an intelligible rationale with its assumptions; the IOM asks for a summary of the relevant evidence and its gaps for each recommendation, and AGREE II appraises a guideline on the explicit link from its recommendations to their evidence. Diátaxis keeps explanation closely bounded rather than mixed with instruction, and Martin Fowler reads normative text as the standard itself, which is why the rationale lives in its own part and the rules hold only requirements. The cookbook's research folder and its citation form are its own design for that link, kept for the owner.
- **Normative and informative are labelled.** The W3C QA Framework has a specification say how normative content is told from informative; the W3C Manual of Style asks that informative material be clearly distinguished, that each informative section say so at its start, and that no figure, example or note be made normative, as WCAG 2.2 treats its diagrams, examples and notes; editors are warned against informative text that sounds normative; and RFC 7322 has a reference list mark each reference normative or informative. Diátaxis's four forms of documentation are the reason each part is labelled with the form it holds.
- **One topic, one place.** GOV.UK's documentation style tells writers not to duplicate what existing documentation says, a Diátaxis how-to guide links to material that would get in its way, and Diátaxis reference links to how-to guides and explanation rather than containing them.
- **Versions are fixed once released, and each is recorded.** Semantic Versioning forbids modifying a released version's contents. The W3C Process has a revised draft publicly document its substantive changes, and a report's status section explain or link to its significant changes. Keep a Changelog has an entry for every version, the latest first, with each release's date displayed, and calls commit-log diffs a bad changelog because they are full of noise.
- **Structure is checked like code.** Write the Docs' docs-as-code practice writes documentation with the same tools as code; Astro content collections enforce frontmatter with a schema, markdownlint's MD043 checks headings against a required list, and Vale's existence check looks for listed tokens.
- **Questions left to the owner.** Whether gf-research-folder, gf-rule-cites-research, gf-rfc-keywords and gf-roled-parts stay MUST, since the outside sources put their substance at should or good-practice strength; whether gf-title-heading is kept, given markdownlint's default; whether gf-compliance-section is kept, since no source speaks to it; whether examples-are-non-normative is written as MUST NOT; whether normative-keywords-only-where-required belongs here or to requirement-keywords; whether keep-rule-lists-short applies to a rules part; whether the change history is ordered newest-first or oldest-first; whether the conv-* rules that state tool behaviour stay as design statements without outside research; and whether a rule is held to the strength of the weakest claim it cites, which no claim in this research states.

## References

This part is informative: it lists the sources the rules were researched from.

### Normative

- [RFC 2119: Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119) (IETF)

### Informative

- [Appendix C: How to Write a Good Requirement](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/) (NASA)
- [Clinical Practice Guidelines We Can Trust, Chapter 5: Current Best Practices and Standards for Development of Trustworthy CPGs: Part II, Traversing the Process](https://www.nationalacademies.org/read/13058/chapter/7) (The National Academies Press)
- [Clinical Practice Guidelines We Can Trust, Chapter 1: Introduction](https://www.nationalacademies.org/read/13058/chapter/3) (The National Academies Press)
- [AGREE II: advancing guideline development, reporting and evaluation in health care](https://pmc.ncbi.nlm.nih.gov/articles/PMC3001530) (CMAJ (Canadian Medical Association Journal))
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) (keepachangelog.com)
- [Docs as Code](https://www.writethedocs.org/guide/docs-as-code/) (Write the Docs)
- [Documentation style guide](https://docs.publishing.service.gov.uk/manual/docs-style-guide.html) (GOV.UK Developer Documentation)
- [markdownlint Rules (doc/Rules.md)](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md) (GitHub (DavidAnson/markdownlint))
- [markdownlint Custom Rules (doc/CustomRules.md)](https://github.com/DavidAnson/markdownlint/blob/main/doc/CustomRules.md) (GitHub (DavidAnson/markdownlint))
- [Existence](https://docs.vale.sh/checks/existence) (docs.vale.sh)
- [Scopes](https://docs.vale.sh/topics/scopes) (docs.vale.sh)
- [Understanding JSON Schema: object](https://json-schema.org/understanding-json-schema/reference/object) (json-schema.org)
- [Understanding JSON Schema: Enumerated values](https://json-schema.org/understanding-json-schema/reference/enum) (json-schema.org)
- [remark-lint-frontmatter-schema](https://github.com/JulianCataldo/remark-lint-frontmatter-schema) (GitHub)
- [Content collections](https://docs.astro.build/en/guides/content-collections/) (docs.astro.build)
- [Semantic Versioning 2.0.0](https://semver.org/) (semver.org)
- [OWASP Application Security Verification Standard (README)](https://github.com/OWASP/ASVS/blob/master/README.md) (GitHub (OWASP/ASVS))
- [RFC 7322: RFC Style Guide](https://www.rfc-editor.org/rfc/rfc7322) (RFC Editor)
- [RFC 7991: The "xml2rfc" Version 3 Vocabulary](https://www.rfc-editor.org/rfc/rfc7991) (RFC Editor (IAB stream))
- [QA Framework: Specification Guidelines](https://www.w3.org/TR/qaframe-spec/) (W3C)
- [W3C Manual of Style](https://www.w3.org/guide/manual-of-style/) (W3C)
- [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/) (W3C)
- [W3C Process Document](https://www.w3.org/policies/process/) (W3C)
- [Diátaxis](https://diataxis.fr/) (diataxis.fr)
- [Reference](https://diataxis.fr/reference/) (diataxis.fr)
- [How-to guides](https://diataxis.fr/how-to-guides/) (diataxis.fr)
- [Explanation](https://diataxis.fr/explanation/) (diataxis.fr)
- [Headings and titles](https://developers.google.com/style/headings) (Google developer documentation style guide)
- [Lists](https://developers.google.com/style/lists) (Google developer documentation style guide)
- [Scannable content - Microsoft Style Guide](https://learn.microsoft.com/en-us/style-guide/scannable-content/) (Microsoft Learn)
- [Lists - Microsoft Style Guide](https://learn.microsoft.com/en-us/style-guide/scannable-content/lists) (Microsoft Learn)
- [Standards Speak](https://www.martinfowler.com/bliki/StandardsSpeak.html) (martinfowler.com)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-21 | Mike Fullerton | Initial creation |
