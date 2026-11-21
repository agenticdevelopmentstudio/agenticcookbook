# Write brief: guideline-formatting

Today is 2026-11-21.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/guideline-formatting (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/guideline-formatting/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/guideline-formatting/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/guideline-formatting/owner-list.md.
cookr, this checkout's own (never an installed one): PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook <command>

Review criteria. Stage 4 reviews against exactly these, and the author writes to them:

1. Every guideline in /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/recipe-quality/:
   behavioral-requirements, completeness, cookbook-compliance,
   cross-recipe-consistency, source-fidelity and template-conformance.
2. Source fidelity means fidelity to the research:
   - every rule follows from the claims it cites, at the strength it states;
   - no claim with a `supported` or `new` verdict is left without a rule;
   - every rule ends with its citation, and every cited claim exists.
3. The strength rule: each rule is at the strength of the weakest claim it
   cites. A claim the second check refuted (listed under "Second-check
   corrections, refuted" in the write brief; its `trust.basis` says "Second
   check … refuted") cannot carry MUST. A claim that only lost a citation
   whose source lacked the quote (listed under "citation dropped") is still
   supported, and its strength is unchanged.
4. A rule's citations are authoritative. A verdict's `claims` list is stage
   2's record of the old rule: nobody compares it with the rule's citations,
   and research is not edited after stage 2. A rule may cite any claim of
   research.json that some verdict names. Prior rule names (the names the
   verdicts key on) are fixed; new rules may be named and renamed freely.
5. The owner list (owner-list.md): a prior rule listed there keeps its prior
   text word for word, citing `<rule>-prior`. Only its wording is exempt from
   review, nothing else. Where the prior text has no RFC keyword, one lead-in
   in front of it carries the keyword the old text implied ("In TypeScript,
   the panel MUST be reached this way:"); owner-list.md lists the lead-in, and
   it is the one change accepted. An open question listed there is the
   owner's: the text does not settle it, and it is never a finding.
6. Frontmatter: the author updates `summary` (160 characters or fewer,
   describing the new text), `tags`, `platforms` and `related` to match the
   new guideline. `version`, `modified` and Change History are left for stage
   5's `cookr bump`: a stale version, modified date or history is never a
   finding.
7. One topic at a time: a finding about a sibling topic's guideline names the
   sibling, and the orchestrator routes it there; it is not this topic's to
   fix.

Write one roled guideline, as a single markdown doc with frontmatter, that:
- keeps every rule whose verdict is `supported`, reworded only where the
  research says it is wrong or unclear, at the strength of its weakest cited
  claim;
- adds a named rule for every `new` verdict, at the strength of its weakest
  cited claim;
- leaves every rule on the owner list below worded exactly as its prior
  text, citing its `<rule-name>-prior` claim: `(claim: <rule-name>-prior)`.
  Where the prior text has no MUST, SHOULD or MAY, put one lead-in in front of
  it carrying the keyword the old text implied, and keep the text after it
  word for word;
- settles none of the open questions on the owner list;
- follows /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/tbd/compliance/artifact-formatting/guideline-formatting.md,
  gf-roled-parts and gf-named-rules: an intro; a `## Rules` section of
  named rules `- **kebab-name**: … MUST|SHOULD|MAY …`; how-to and example
  sections; `## What a reviewer looks for`;
  `## A complete review must establish`; `## A build must establish`;
  `## Rationale`; `## References`; `## Change History`;
- gives `## A build must establish` exactly one line per named rule,
  `` - `rule-name`: … ``, and no line naming anything that is not a named
  rule of `## Rules` (`cookr roles check` refuses a rule with no line and a
  line naming no rule);
- cites research exactly as `cookr validate` enforces it: every named rule
  ends with one citation, `(claim: <id>)` or `(claims: <id>, <id>)`, with
  nothing after it, not even a full stop; only one citation per rule;
  every id is a claim `id` in research.json that some verdict names
  (gf-rule-cites-research);
- updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` to match the new text, and leaves `version`, `modified` and Change History to stage 5's `cookr bump`.

Edit only the draft. Never edit research, the owner list or another topic.
A finding you think is wrong is disputed, not obeyed: see the round sections
below, when there are any.

Verdicts:
- gf-frontmatter-complete: supported (claims: rfc7322-required-elements, rfc7991-front-matter-metadata, json-schema-required, json-schema-no-additional-properties, astro-schema-enforces-frontmatter, remark-lint-frontmatter-schema)
- gf-type-field: supported (claims: json-schema-enum, diataxis-four-forms)
- gf-title-heading: unsupported (claims: gf-title-heading-prior, google-unique-h1, markdownlint-md025-front-matter-title, markdownlint-md041-first-line-heading, markdownlint-custom-rules)
- gf-summary-statement: supported (claims: rfc7322-abstract-required, rfc7322-abstract-complete-in-itself, ms-lead-with-most-important)
- gf-structured-guidance: supported (claims: w3c-qa-consistent-requirement-style, ms-discrete-components, google-bulleted-lists, agree-key-recommendations-identifiable, diataxis-reference-consistent)
- gf-rfc-keywords: unsupported (claims: gf-rfc-keywords-prior, w3c-qa-rfc2119-technique, w3c-qa-consistent-requirement-style, w3c-qa-distinctive-formatting, rfc7322-requirements-language, rfc2119-use-sparingly)
- gf-change-history: supported (claims: w3c-process-document-substantive-changes, w3c-process-status-explains-changes, keepachangelog-entry-per-version, keepachangelog-date-displayed, markdownlint-md043-required-headings)
- gf-compliance-section: unsupported (claims: gf-compliance-section-prior)
- gf-triggers-field: unsupported (claims: gf-triggers-field-prior, json-schema-enum)
- gf-roled-parts: unsupported (claims: gf-roled-parts-prior, w3c-qa-distinguish-normative, w3c-mos-label-each-section, diataxis-four-forms, diataxis-reference-link-out, diataxis-how-to-link-out, diataxis-explanation-bounded)
- gf-named-rules: supported (claims: w3c-qa-consistent-requirement-style, nasa-uniquely-referenced, nasa-one-thought-per-requirement, wcag-sc-number-and-short-name, rfc7991-anchor-attribute, vale-markup-aware-scopes)
- gf-research-folder: unsupported (claims: gf-research-folder-prior, iom-evidence-per-recommendation, agree-explicit-link-to-evidence, iom-transparent-process)
- gf-rule-cites-research: unsupported (claims: gf-rule-cites-research-prior, iom-evidence-per-recommendation, agree-explicit-link-to-evidence)
- conv-roled-parts: supported (claims: w3c-qa-distinguish-normative, w3c-mos-label-each-section, diataxis-four-forms)
- conv-named-rules: supported (claims: nasa-one-thought-per-requirement, nasa-uniquely-referenced, w3c-qa-consistent-requirement-style)
- conv-one-source-per-topic: supported (claims: govuk-dont-duplicate, diataxis-how-to-link-out)
- conv-research-cited: supported (claims: iom-evidence-per-recommendation, agree-explicit-link-to-evidence)
- conv-legacy-keeps-working: unsupported (claims: conv-legacy-keeps-working-prior)
- conv-role-values: unsupported (claims: conv-role-values-prior)
- conv-no-roles-under-reviewing: unsupported (claims: conv-no-roles-under-reviewing-prior)
- conv-roled-artifact-complete: unsupported (claims: conv-roled-artifact-complete-prior)
- conv-four-skills: unsupported (claims: conv-four-skills-prior)
- conv-skill-names: unsupported (claims: conv-skill-names-prior)
- conv-rationale-to-references: supported (claims: nasa-rationale-accompanies-requirement, nasa-requirements-and-rationale-mixed, diataxis-explanation-bounded, fowler-normative-part-of-standard)
- conformance-and-scope-statement: new (claims: w3c-qa-conformance-clause, w3c-qa-define-scope, w3c-qa-no-requirements-in-scope)
- mark-normative-and-informative: new (claims: w3c-qa-distinguish-normative, w3c-mos-distinguish-informative, w3c-qa-avoid-normative-sounding-informative, rfc7322-references-normative-informative, fowler-normative-part-of-standard)
- examples-are-non-normative: new (claims: w3c-mos-examples-never-normative, wcag-examples-notes-informative)
- one-requirement-per-rule: new (claims: nasa-one-thought-per-requirement, agree-specific-unambiguous, nasa-requirements-and-rationale-mixed)
- rules-are-verifiable: new (claims: nasa-requirements-verifiable, iom-compliance-evaluable, w3c-qa-test-assertions, wcag-success-criteria-testable)
- rule-states-when-it-applies: new (claims: iom-standardized-form-and-circumstances)
- rule-has-rationale: new (claims: nasa-rationale-accompanies-requirement, iom-evidence-per-recommendation)
- stable-rule-identifiers: new (claims: w3c-mos-dont-break-links, asvs-versioned-identifiers, asvs-positional-ids-problematic)
- normative-keywords-only-where-required: new (claims: rfc2119-use-sparingly, rfc2119-no-method-imposition)
- single-h1: new (claims: google-unique-h1, markdownlint-md025-front-matter-title)
- no-skipped-heading-levels: new (claims: google-no-skipped-heading-levels)
- keep-rule-lists-short: new (claims: ms-list-length)
- change-history-newest-first: new (claims: keepachangelog-latest-first, keepachangelog-commit-diffs-bad)
- released-versions-immutable: new (claims: semver-released-immutable)
- check-guidelines-automatically: new (claims: writethedocs-docs-as-code, astro-schema-enforces-frontmatter, markdownlint-md043-required-headings, vale-existence-check)

Second-check corrections, refuted (criteria 3 applies to these claims):
- w3c-qa-conformance-clause: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST
- w3c-qa-define-scope: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST
- w3c-qa-distinguish-normative: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST
- fowler-normative-part-of-standard: refuted (quote-found yes, supports-claim partly); trust 60 -> 40; a rule citing it cannot carry MUST
- w3c-mos-examples-never-normative: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST
- nasa-one-thought-per-requirement: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST
- nasa-requirements-and-rationale-mixed: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST
- nasa-requirements-verifiable: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST
- w3c-qa-test-assertions: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST
- wcag-success-criteria-testable: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST
- iom-standardized-form-and-circumstances: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST
- iom-evidence-per-recommendation: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST
- w3c-mos-dont-break-links: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST
- asvs-versioned-identifiers: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- asvs-positional-ids-problematic: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST
- rfc2119-use-sparingly: refuted (quote-found yes, supports-claim partly); trust 90 -> 70; a rule citing it cannot carry MUST
- markdownlint-md025-front-matter-title: refuted (quote-found yes, supports-claim partly); trust 88 -> 68; a rule citing it cannot carry MUST
- ms-list-length: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- keepachangelog-commit-diffs-bad: refuted (quote-found yes, supports-claim partly); trust 66 -> 46; a rule citing it cannot carry MUST
- writethedocs-docs-as-code: refuted (quote-found yes, supports-claim partly); trust 65 -> 45; a rule citing it cannot carry MUST
- astro-schema-enforces-frontmatter: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST
- markdownlint-md043-required-headings: refuted (quote-found yes, supports-claim partly); trust 88 -> 68; a rule citing it cannot carry MUST
- vale-existence-check: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **gf-title-heading** — verdict `unsupported` (claims: gf-title-heading-prior, google-unique-h1, markdownlint-md025-front-matter-title, markdownlint-md041-first-line-heading, markdownlint-custom-rules). Prior text, kept word for word: "The first H1 heading MUST match the frontmatter `title` field exactly.

**Applies when:** always."
  - against: Google's developer documentation style uses one unique level-1 heading per page.
  - against: markdownlint's MD025 (single-title) treats a front-matter title as the document's top-level heading and reports any further top-level heading; front_matter_title set to "" disables that.
  - against: markdownlint's MD041 checks that a document has a title, by its first line being a top-level heading or by a front-matter title.
  - against: markdownlint custom rules can do everything built-in rules can and receive the file's lines and front-matter lines, so a check the built-ins lack (such as H1 equals the front-matter title) can be written as one.
- **gf-rfc-keywords** — verdict `unsupported` (claims: gf-rfc-keywords-prior, w3c-qa-rfc2119-technique, w3c-qa-consistent-requirement-style, w3c-qa-distinctive-formatting, rfc7322-requirements-language, rfc2119-use-sparingly). Prior text, kept word for word: "Requirements within the guideline MUST use RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) to indicate obligation levels. Keywords MUST be bold or uppercase when used normatively.

**Applies when:** the guideline contains requirements or rules (not purely informational content)."
  - against: The W3C QA Framework gives RFC 2119 keywords as a technique that makes conformance requirements easy to spot.
  - against: The W3C QA Framework requires conformance requirements to be written in a consistent style and the specification to explain how to tell them apart.
  - against: Conformance requirements are usually set off with distinctive formatting such as uppercase or bold.
  - against: An RFC that uses the RFC 2119 interpretation must cite RFC 2119 as a normative reference, in a section within or after the Introduction.
  - against: RFC 2119's imperatives are to be used with care and sparingly, only where required for interoperation or to limit harmful behaviour, and not to impose a method that interoperability does not require.
- **gf-compliance-section** — verdict `unsupported` (claims: gf-compliance-section-prior). Prior text, kept word for word: "The guideline MAY include a `## Compliance` section listing evaluated compliance checks and their status. This is recommended when the guideline is referenced by compliance checks in other categories.

**Applies when:** the guideline is referenced by one or more compliance check definitions."
- **gf-triggers-field** — verdict `unsupported` (claims: gf-triggers-field-prior, json-schema-enum). Prior text, kept word for word: "The `triggers` field SHOULD be present in guideline frontmatter. It MUST be a YAML list of trigger names from the canonical taxonomy defined in `introduction/trigger-guide.md`. Empty list `[]` is acceptable for guidelines not yet classified.

**Applies when:** always."
  - against: JSON Schema's `enum` restricts a value to a fixed set, the mechanism for a closed-vocabulary field such as `type` or each item of a `triggers` list.
- **gf-roled-parts** — verdict `unsupported` (claims: gf-roled-parts-prior, w3c-qa-distinguish-normative, w3c-mos-label-each-section, diataxis-four-forms, diataxis-reference-link-out, diataxis-how-to-link-out, diataxis-explanation-bounded). Prior text, kept word for word: "A roled guideline MUST give every part but the intro and the history a `role` in `artifact.json`, one of `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`, and MUST have at least one part of each of `rules`, `review-focus`, `review-bar` and `build-bar`. It sets no `routes` and no `hosts/`, and does not live under `guidelines/reviewing/`.

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

**Applies when:** any part of the guideline carries a `role`."
  - against: A specification should say in its conformance clause how normative content is told from informative content, labelling each.
  - against: Where some sections of a W3C document are informative, each says so at its start.
  - against: Diátaxis identifies four distinct needs and four corresponding forms of documentation: tutorials, how-to guides, technical reference and explanation.
  - against: Diátaxis reference is austere, neutral description, and links to how-to guides and explanation rather than containing them.
  - against: A Diátaxis how-to guide has no digression, explanation or teaching; material that would get in the way is linked to instead.
  - against: Diátaxis explanation gives background, context and reasons, and is kept closely bounded rather than mixed with instruction or reference.
- **gf-research-folder** — verdict `unsupported` (claims: gf-research-folder-prior, iom-evidence-per-recommendation, agree-explicit-link-to-evidence, iom-transparent-process). Prior text, kept word for word: "The guideline MUST keep the research it was written from in `research/` in its folder: `research/research.json`, in the shape of the research-results document (`guidelines/researching/evidence/research-results-document`), and `research/research.md`, the same, readable, under the four question headings in this order: `## Best practices`, `## Known solutions`, `## Platform guidelines`, `## The expert's view`.

Each claim in `research.json`'s `claims` list is the per-claim record: `id` (kebab-case, unique), `question` (`best-practices`, `known-solutions`, `platform-guidelines` or `experts-view`), `claim`, `citations` (each with `title`, `author`, `publisher`, `date`, `url`, `accessed`), `source_type`, `quote`, `generated_by`, `query`, `trust` (`{"score": 0-100, "basis"}`) and `independence` (`multi-independent`, `single` or `uncorroborated`). The `verdicts` list gives each rule checked a verdict, `supported`, `contradicted`, `unsupported` or `new`, and the claims it rests on, at least one; every claim a rule cites MUST be named by a verdict. A rule the research cannot support is recorded as a claim itself, its source the cookbook's own text at the topic's base commit, with an `unsupported` verdict (`contradicted` when the research finds against it) naming that claim; a rule kept for the owner cites it, and `cookr validate` passes it with an `owner-decides` warning naming the rule and the claim.

**Applies when:** always, unless the guideline is listed in `cookbook/research-exempt.json` as a topic written before research-first whose research is still to come."
  - against: For each recommendation a trustworthy guideline should provide the reasoning behind it, including a summary of the relevant evidence and its gaps.
  - against: A guideline's quality is appraised on whether there is an explicit link between its recommendations and their supporting evidence.
  - against: A trustworthy guideline is based on an explicit and transparent development process.
- **gf-rule-cites-research** — verdict `unsupported` (claims: gf-rule-cites-research-prior, iom-evidence-per-recommendation, agree-explicit-link-to-evidence). Prior text, kept word for word: "Each named rule MUST cite the claims of its research it stands on, once, at the end of its bullet: `(claim: <id>)`, or `(claims: <id>, <id>)` for several. Nothing follows the citation. Every id cited MUST be a claim in `research/research.json`. The citation names the claim, never the document (`cite-the-claim-not-the-document`), so a reader can follow a rule to the quote and source behind it.

```markdown
- **index-foreign-keys**: Every foreign-key column MUST have an index. (claims: fk-index-postgres, fk-index-sqlite)
```

**Applies when:** the guideline has a `research/` folder. In a roled guideline the named rules are its `rules` parts' bullets; in an unroled one, every named bullet that states MUST, SHOULD or MAY outside the intro and the history."
  - against: For each recommendation a trustworthy guideline should provide the reasoning behind it, including a summary of the relevant evidence and its gaps.
  - against: A guideline's quality is appraised on whether there is an explicit link between its recommendations and their supporting evidence.
- **conv-legacy-keeps-working** — verdict `unsupported` (claims: conv-legacy-keeps-working-prior). Prior text, kept word for word: "An artifact written before this design keeps working as it is: an unroled artifact compiles as it always did, and one with no research is listed in `cookbook/research-exempt.json` until its research is written." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **conv-role-values** — verdict `unsupported` (claims: conv-role-values-prior). Prior text, kept word for word: "A part may carry a `role` in `artifact.json`: `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`. The intro and the history never carry one. An artifact with no role is compiled as it always was." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **conv-no-roles-under-reviewing** — verdict `unsupported` (claims: conv-no-roles-under-reviewing-prior). Prior text, kept word for word: "A guideline with roles may live under any use-case folder but `guidelines/reviewing/`, which is folded into each topic and never roled; a principle may carry roles too, an ingredient or a recipe never." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **conv-roled-artifact-complete** — verdict `unsupported` (claims: conv-roled-artifact-complete-prior). Prior text, kept word for word: "A roled artifact gives every other part a role, names each rule in its `rules` parts (`- **kebab-name**: … MUST|SHOULD|MAY …`), and sets no `routes` and no `hosts/`. `cookr validate` lists what is wrong."
- **conv-four-skills** — verdict `unsupported` (claims: conv-four-skills-prior). Prior text, kept word for word: "It compiles to four skills, each the intro plus the parts of its roles:

| Skill | Roles | Name |
|---|---|---|
| builder | `rules`, `how-to`, `examples` | `<use-case>-<tail>` |
| build-verifier | `build-bar` | `verifying-build-<tail>` |
| reviewer | `rules`, `review-focus` | `reviewing-<tail>` |
| review-verifier | `review-bar` | `verifying-review-<tail>` |" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **conv-skill-names** — verdict `unsupported` (claims: conv-skill-names-prior). Prior text, kept word for word: "The builder keeps the name the artifact would have unroled; the other three replace only its use case: `guidelines/planning/data/t` gives `planning-data-t` and `reviewing-data-t`, and `principles/t`, which has no use case, keeps its type: `principle-t` and `reviewing-principle-t`. Two artifacts whose skills would share a name, after a long name is cut to the hosts' limit, are refused, each naming the other." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.

## Open questions

- Whether gf-research-folder and gf-rule-cites-research stay MUST: the strongest outside sources (IOM Standard 5.1, AGREE II) phrase per-recommendation evidence as 'should be provided' or as an appraisal criterion; the owner decides whether the cookbook's research-first ruling justifies MUST.
- Whether gf-rfc-keywords stays MUST: the W3C QA Framework requires a consistent, distinguishable style for requirements (Requirement 7) and gives RFC 2119 keywords only as a technique; the owner decides whether the cookbook requires the keywords themselves (keyword case belongs to requirement-keywords).
- Whether gf-roled-parts stays MUST: outside sources support labelling normative and informative content and separating reference, how-to and explanation at SHOULD/good-practice strength; the specific role vocabulary and the four required roles are the cookbook's own design.
- Whether gf-title-heading (H1 equals the frontmatter title) is kept: no source requires it, and markdownlint's default (MD025 with front_matter_title) treats a frontmatter title as the document's top-level heading, so a title plus an H1 is reported as a second top-level heading unless the option is disabled.
- Whether gf-compliance-section is kept: no outside source speaks to a section listing evaluated compliance checks; the W3C's conformance clause is a different element (what conformance requires), proposed as the new rule conformance-and-scope-statement.
- Whether examples-are-non-normative is written as MUST NOT: the W3C Manual of Style says 'document editors must not make any figure, example or note normative' but also says 'No requirements for W3C publications are in this document.'
- Whether normative-keywords-only-where-required belongs to this topic or to requirement-keywords: it is about when a rule carries an obligation at all (structure), but it is RFC 2119's own keyword guidance.
- Whether keep-rule-lists-short applies to a rules part: Microsoft's seven-item limit is for lists in general ('if possible'), not for a rule-bearing document's rule count.
- Whether the change history is ordered newest-first (Keep a Changelog) or oldest-first (the conventions.md example has one row, so the order is not stated).
- Whether conv-* rules that state tool behaviour (conv-legacy-keeps-working, conv-role-values, conv-no-roles-under-reviewing, conv-roled-artifact-complete, conv-four-skills, conv-skill-names) remain in conventions.md as design statements without outside research, per owner ruling Q12.
