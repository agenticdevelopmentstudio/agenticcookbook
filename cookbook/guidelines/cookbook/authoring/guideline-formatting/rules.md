
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

