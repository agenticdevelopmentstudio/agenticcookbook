# Review: guideline-formatting

## Findings

- `rules.md`, **gf-structured-guidance**: the rule is MUST, but two of the four claims it cites are hedged below MUST. `google-bulleted-lists` reads "Use the same syntax/structure for all list items in a given list, if possible", and `diataxis-reference-consistent` says only that reference "is useful when it is consistent". `ms-discrete-components` is style advice ("to support scanning"). Only `w3c-qa-consistent-requirement-style` (QA Framework Requirement 7) is MUST-strength. The "every item of a list in the same structure" and "discrete components" parts therefore outrun their claims. No other MUST rule cites a hedged or refuted claim: all 43 rules were checked, and no refuted claim carries MUST anywhere. Fix: either lower gf-structured-guidance to SHOULD, or keep gf-structured-guidance at MUST for "requirements written in one consistent style that tells them apart" citing only `w3c-qa-consistent-requirement-style` and move the discrete-components and same-list-structure requirement into a new SHOULD rule citing `ms-discrete-components, google-bulleted-lists, diataxis-reference-consistent`, with its own build-bar line.
- `rules.md`, **rule-states-when-it-applies**: the rule's text now says only "a standardized form that states precisely the action it requires". The circumstances half is gone, but four places still require it. The rule's name says "when it applies". `what-a-reviewer-looks-for.md` line 5 reads "or does not say when it applies". `a-complete-review-must-establish.md` line 5 reads "and the circumstances it applies in". `how-to-keep-the-rules.md` ("Write one rule to a bullet") says "say when it applies". The `rationale.md` bullet head reads "and says when it applies". So the reviewer and the review-verifier check a requirement that no rule states. Fix: restore the circumstances clause to the rule at SHOULD ("… that states precisely the action it requires and the circumstances in which it applies"). `iom-standardized-form-and-circumstances` states it, and as a refuted claim it can still carry SHOULD (the second check found the clause in IOM Standard 6.1, just outside the quote). Otherwise, rename the rule (for example `rule-states-action-precisely`) and remove the "when it applies" or "circumstances" wording from all four places.
- `what-a-reviewer-looks-for.md` ("A rule whose keyword is stronger than the claims it cites"), `a-complete-review-must-establish.md` ("No rule is stronger than the weakest claim it cites.") and `how-to-keep-the-rules.md` ("Pick the keyword from the evidence. A rule is no stronger than the weakest claim it cites. Use MUST only where the cited claims say must; a claim that says should carries SHOULD."): all three state and enforce a requirement that no named rule in `## Rules` holds. Informative parts state a requirement of their own, which mark-normative-and-informative and examples-are-non-normative say they should not, and the review bar holds a reviewer to something the rules never ask of a builder. Fix: tie each of these lines to a named rule the research supports (for example, fold the check into what normative-keywords-only-where-required covers, a keyword used where its evidence does not require it). If no cited claim carries it, remove the two review lines, recast the how-to bullet as informative advice, and add the missing strength rule to the rationale's "Questions left to the owner".
- `intro.md`: the summary statement says a guideline "MUST … give each part a role" and "keep that research in its folder" with no conditions. Both contradict the rules they summarise. gf-roled-parts applies only "when any part of the guideline carries a `role`". conv-legacy-keeps-working keeps unroled artifacts compiling as they always did. gf-research-folder exempts topics listed in `cookbook/research-exempt.json`. Fix: state the conditions ("a roled guideline gives each part but the intro and history a role"; "keeps its research in its folder unless it is listed as research-exempt"), or drop the MUST from the summary and phrase it as a description.
- `rationale.md` and `rules.md` **stable-rule-identifiers**: three source statements contradict what the second check found.
  - Rationale ("A named rule can be referenced…") says "OWASP ASVS warns that positional identifiers change between versions and become a problem as a standard grows". The second check on `asvs-positional-ids-problematic` found that "this becomes problematic" refers to identifiers used without the version element, not to positional identifiers. stable-rule-identifiers repeats the same misreading in its "since positional identifiers may change between versions and become problematic as the guideline grows and changes" clause.
  - Rationale (same bullet) says NASA "names the paragraph that mixes requirements with rationale as a common failure". Per the second check on `nasa-requirements-and-rationale-mixed`, the source does not call it common.
  - Rationale ("A rule is worded so compliance can be judged…") says "NASA requires a requirement to be verifiable". Per the second check on `nasa-requirements-verifiable`, NASA phrases this as a checklist question, not a requirement.

  Fix: reword the rationale to "OWASP ASVS notes that its identifiers may change between versions", "NASA's checklist flags a paragraph that holds both requirements and rationale" and "NASA's checklist asks whether the system can be tested, demonstrated, inspected or analysed against each requirement". Drop the "since…" clause from stable-rule-identifiers.
- `rules.md`, rationale written into rule bullets: these rules carry their reasons inside the rule, against the guideline's own one-requirement-per-rule ("not mix the requirement with its rationale") and conv-rationale-to-references.
  - **change-history-newest-first**: "which are full of noise"
  - **stable-rule-identifiers**: "so they do not break links into the guideline" and "since positional identifiers may change … grows and changes"
  - **conv-research-cited**: "so a reader can find the reasoning and the evidence behind it"
  - **conv-rationale-to-references**: "so the rules alone are the standard"

  Rules on the owner list are exempt. Fix: end each rule at its requirement and move the reason to the matching `rationale.md` bullet, where most of it already is.
- `rules.md`, compound rules: these rules bundle two or more requirements into one bullet. That goes against one-requirement-per-rule ("express only one thought") and recipe-quality/behavioral-requirements `must-not-bundle-behaviors-into-one-requirement`, and the build bar then has one line covering several checks.
  - **gf-frontmatter-complete**: required fields present, and no `domain`
  - **gf-structured-guidance**: discrete components, same list structure, and one requirement style
  - **summary-complete-in-itself**: complete in itself, and most important first
  - **change-history-entry-per-version**: an entry per version, and its changes explained
  - **change-history-newest-first**: latest first, and no commit-log diffs
  - **mark-normative-and-informative**: normative told apart, informative not normative-sounding, and references marked
  - **examples-are-non-normative**: two clauses that restate each other
  - **conformance-and-scope-statement**: conformance statement, scope defined, and no requirements in the scope
  - **stable-rule-identifiers**: names stable, and not positional
  - **conv-one-source-per-topic**: written once, no duplication, and link instead

  Rules on the owner list are exempt. Fix: split each into separately named rules, each with its own citation (prior names stay on the part they named, and new names are free), and give each new rule its own build-bar line.
- The guideline does not keep three of its own SHOULD rules:
  - `references.md` marks no reference as normative or informative (mark-normative-and-informative: "the guideline's references SHOULD each be marked normative or informative").
  - The guideline has no statement of what following it requires and no scope statement (conformance-and-scope-statement).
  - None of its informative parts (`how-to-keep-the-rules.md`, `examples.md`, `rationale.md`, `references.md`) says so at its start (conv-roled-parts: "each informative part says so at its start").

  Fix: mark each reference, for example RFC 2119 and RFC 7322 as normative and the style guides as informative. Add a short conformance and scope statement to the intro, with no requirement in the scope sentence. Open each informative part with a sentence saying it is informative.
- `a-complete-review-must-establish.md`: the review bar does not establish 18 named rules, so the review-verifier never checks them:
  - gf-structured-guidance
  - key-rules-identifiable
  - normative-keywords-only-where-required
  - keywords-impose-no-method
  - change-history-newest-first
  - released-versions-immutable (only renames are covered)
  - gf-compliance-section
  - conv-roled-parts (each informative part labelled)
  - conformance-and-scope-statement
  - mark-normative-and-informative (references marked)
  - rule-has-rationale
  - conv-rationale-to-references
  - keep-rule-lists-short
  - gf-research-folder (`research.json` and `research.md` present and in shape; only the verdict link is covered)
  - conv-role-values (the intro and history carry no role)
  - conv-no-roles-under-reviewing
  - conv-four-skills and conv-skill-names
  - check-guidelines-automatically

  The worked example the guideline itself names (`guidelines/implementing/data/indexing`) has its review bar name every MUST rule and every SHOULD rule. Fix: add a line for each missing rule, or follow the indexing form: "Every MUST rule is kept, with no exception: …" and "Every SHOULD rule is kept, or the review says why not: …", naming all 43 rules.
- `artifact.json` `related`: it lists only research-results-document and template-conformance. It omits the sibling requirement-keywords (`456f23bd-4523-47e8-9541-073ac046f2ad`), which overlaps gf-rfc-keywords, normative-keywords-only-where-required and keywords-impose-no-method and already holds `gf-rfc-keywords` and `keywords-only-where-required` of its own. It also omits activity-triggers (`1b7b83f9-3b8a-46f7-81b7-9a55291a23a2`), the trigger vocabulary gf-triggers-field depends on. conv-one-source-per-topic asks the guideline to link to such docs rather than repeat them. Fix: add both UUIDs to `related`. Whether the shared `gf-rfc-keywords` and the overlapping keyword rule belong here or in requirement-keywords is an open question on the owner list, so it is not raised here; the orchestrator may route the duplicate rule name to requirement-keywords.

## Checked

- Every rule ends with exactly one citation in `(claim: …)` or `(claims: …)` form with nothing after it. Every cited id is a claim in `research.json` that some verdict names (scripted check), and `cookr roles check` reports no findings for the 43 rules.
- Every claim named by a `supported` or `new` verdict is cited by at least one rule (scripted check). No supported or new claim is left without a rule.
- Every rule on the owner list keeps its prior text word for word (scripted comparison against each `<rule>-prior` claim, after removing the 2-space continuation indent) and cites only `<rule>-prior`: gf-title-heading, gf-rfc-keywords, gf-compliance-section, gf-triggers-field, gf-roled-parts, gf-research-folder, gf-rule-cites-research and conv-roled-artifact-complete, all with no lead-in.
- The five lead-ins match owner-list.md exactly: conv-legacy-keeps-working "The cookbook MUST keep this true:", conv-role-values "Roles MUST be used as follows:", conv-no-roles-under-reviewing "Roles MUST be placed as follows:", conv-four-skills "A roled artifact MUST compile as follows:", conv-skill-names "The compiled skills MUST be named as follows:". conv-roled-artifact-complete correctly takes no lead-in, since the owner list gives it none.
- No refuted claim (the 23 listed under "Second-check corrections, refuted") is cited by a MUST rule. Every rule that cites one is at SHOULD or below. The write brief lists no "citation dropped" corrections.
- The other MUST and MUST NOT rules match their claims' strength: gf-frontmatter-complete (RFC 7322 required elements, JSON Schema `required` and `additionalProperties: false`), gf-type-field, gf-summary-statement (RFC 7322 "must have an Abstract"), keywords-impose-no-method (RFC 2119 "must not … impose"), gf-change-history (W3C Process "must provide public documentation"), released-versions-immutable (SemVer MUST NOT).
- Every new rule's SHOULD or SHOULD NOT matches its cited claims, apart from the bundling and wording findings above.
- The prior rule names the verdicts key on are all present and unrenamed. New rules (summary-complete-in-itself, key-rules-identifiable, keywords-impose-no-method, change-history-entry-per-version) cite claims some verdict names.
- The text settles none of the owner list's open questions. The rationale's "Questions left to the owner" restates them without deciding them.
- The build bar has exactly one line per named rule, in rule order, and names nothing else (scripted check, and `cookr roles check` ok).
- `artifact.json` parts: intro, then rules, how-to, examples, review-focus, review-bar, build-bar, rationale and references, then history. The intro and history carry no role, all four required roles are present, and there are no `routes` and no `hosts/`. The four compiled skills are named `cookbook-authoring-guideline-formatting`, `verifying-build-…`, `reviewing-…` and `verifying-review-authoring-guideline-formatting`.
- Frontmatter: `summary` is 153 characters and describes the new text, `type` is `guideline`, `triggers` is `[]`, `platforms` is `[]` (platform-neutral), the tags fit the topic, and both `related` UUIDs resolve (research-results-document, template-conformance). Version, modified and history are left to `cookr bump` and were not reviewed.
- `references` in `artifact.json` matches `references.md` one for one, and each research source is listed.
- `cookr validate --research` on this folder passes. The full `cookr validate` fails only on neutrality findings in sibling topics (activity-triggers and principle-formatting name `claude`/`codex`); none of them is in this folder. Its `owner-decides` warnings for this topic are the expected ones for owner-list rules.
- The H1 equals the `title` and there is a single H1. The examples are informative and correctly formed (named rules, citation last, a build-bar pair, a change-history row).

## Lint

- I ran `/lint-artifact` (v2.0.1) on `cookbook/guidelines/cookbook/authoring/guideline-formatting`, using the checkout's cookr. It checked against `tbd/compliance/artifact-formatting/guideline-formatting.md`.
- Pass 18, Warn 1, Fail 0. RESULT: CLEAN.
- These checks passed: FM-01 through FM-13 (FM-11a links resolve), GF-01 summary after the H1, GF-02 structured guidance, GF-03 RFC 2119 keywords, plus gf-roled-parts, gf-named-rules, gf-research-folder and gf-rule-cites-research (`research.json` and `research.md` present; cookr's roles, citation and research checks pass).
- [WARN] GF-04 / gf-compliance-section: there is no `## Compliance` section. The rule asks for one only when compliance checks reference this guideline, so this is a warning, not an error.
- The repo-wide `cookr validate` failure comes from other artifacts. Its rows are owner-decides and neutrality findings in sibling topics, and none is in this folder.

lint: clean

verdict: fail

