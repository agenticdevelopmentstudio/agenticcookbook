# Write brief: requirement-keywords

Today is 2026-11-21.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/requirement-keywords (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/requirement-keywords/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/requirement-keywords/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/requirement-keywords/owner-list.md.
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
- gf-rfc-keywords: unsupported (claims: gf-rfc-keywords-prior, keywords-not-required-for-normative-text, qa-consistent-style-explain, oasis-should-use-rfc2119, keywords-make-requirements-easy-to-spot)
- gf-rfc-keywords-bold-or-uppercase: contradicted (claims: gf-rfc-keywords-bold-or-uppercase-prior, uppercase-only-meaning, lowercase-has-normal-english-meaning, bcp14-boilerplate, oasis-uppercase-only)
- use-rfc-2119-keywords-for-behavioral-requirements: unsupported (claims: use-rfc-2119-keywords-for-behavioral-requirements-prior, keywords-not-required-for-normative-text, qa-consistent-style-explain, tab-keywordless-must-equivalent)
- must-is-absolute-requirement: supported (claims: rfc2119-must-absolute-requirement, rfc2119-must-not-absolute-prohibition, iso-shall-requirement)
- should-is-recommendation: supported (claims: rfc2119-should-recommendation, rfc2119-should-not-recommendation, iso-should-preferred)
- may-is-optional-behavior: supported (claims: rfc2119-may-truly-optional, iso-may-permission)
- rule-uses-rfc-2119-keywords: unsupported (claims: rule-uses-rfc-2119-keywords-prior, keywords-not-required-for-normative-text, oasis-should-use-rfc2119, infra-core-subset)
- follow-must-address-should-checks: supported (claims: rfc2119-must-absolute-requirement, rfc2119-should-recommendation, qa-indicate-levels, qa-conformance-classes-by-level)
- approve-on-zero-fail: supported (claims: vale-only-errors-nonzero, eslint-error-for-ci, markdownlint-cli2-exit-codes, github-check-fails-on-error, bikeshed-die-on, bikeshed-die-on-default-fatal)
- keywords-meaningful-only-in-uppercase: new (claims: uppercase-only-meaning, lowercase-has-normal-english-meaning, oasis-uppercase-only, oasis-case-change-is-material, infra-willful-violation, infra-lowercase-equivalent, bikeshed-lowercase-for-readability)
- lowercase-keyword-in-rule-text-flagged: new (claims: sperberg-mcqueen-lowercase-misuse, fantasai-lowercase-misuse-is-editorial-error, oasis-case-change-is-material, bikeshed-accidental-2119, caceres-respec-defaults-bcp14, lint-unmarked-keyword-usage, eslint-warn-for-uncertain)
- state-the-keyword-interpretation: new (claims: state-the-interpretation, bcp14-boilerplate, idnits-boilerplate-check, respec-conformance-boilerplate, respec-warns-missing-conformance)
- state-how-keywordless-text-is-read: new (claims: qa-consistent-style-explain, keywords-not-required-for-normative-text, infra-no-keywords-in-non-normative, tab-keywordless-must-equivalent)
- no-keywords-in-non-normative-text: new (claims: qa-no-normative-language-in-informative, w3c-mos-no-keywords-informative, infra-lowercase-equivalent, etsi-requirements-only-normative, bikeshed-accidental-2119)
- keyword-sets-finding-severity: new (claims: rfc2119-must-absolute-requirement, rfc2119-should-recommendation, rfc2119-may-truly-optional, qa-conformance-classes-by-level, sarif-error-level, sarif-warning-level, sarif-note-level, eslint-warn-for-uncertain, markdownlint-error-or-warning, respec-lint-severity, bikeshed-error-levels)
- warn-findings-do-not-block: new (claims: vale-only-errors-nonzero, vale-minalertlevel-ci, eslint-warn-no-exit-code, eslint-max-warnings, markdownlint-cli2-exit-codes, github-check-fails-on-error, github-ruleset-blocks-merge, bikeshed-die-on-default-fatal)
- one-keyword-per-requirement: new (claims: qa-subject-keyword-operation, w3c-wiki-active-form)
- use-core-keyword-subset: new (claims: infra-core-subset, plainlanguage-must-not-shall)
- no-mixed-case-negation-or-may-not: new (claims: idnits-mixed-case-not, idnits-may-not, oasis-may-not-not-keyword, iso-no-may-not)
- one-keyword-set-never-mixed: new (claims: oasis-never-mix-keyword-sets, iso-no-must-for-shall, plainlanguage-must-not-shall, oasis-iso-keywords-by-definition, sperberg-mcqueen-iso-avoids-nonstandard-senses)
- keywords-only-where-required: new (claims: keywords-used-sparingly, sperberg-mcqueen-focus-attention, keywords-make-requirements-easy-to-spot, w3c-mos-uppercase-em, tab-drop-formatting-requirement, fantasai-styling-requirement)

Second-check corrections, refuted (criteria 3 applies to these claims):
- bcp14-boilerplate: refuted (quote-found yes, supports-claim partly); trust 88 -> 68; a rule citing it cannot carry MUST
- bikeshed-lowercase-for-readability: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST
- eslint-warn-for-uncertain: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- state-the-interpretation: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST
- idnits-boilerplate-check: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST; dropped 1 citation(s) lacking the quote; independence single -> single
- qa-consistent-style-explain: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST
- etsi-requirements-only-normative: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST
- sarif-warning-level: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST
- respec-lint-severity: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- vale-minalertlevel-ci: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- eslint-warn-no-exit-code: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST
- markdownlint-cli2-exit-codes: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- github-ruleset-blocks-merge: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- bikeshed-die-on-default-fatal: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- plainlanguage-must-not-shall: refuted (quote-found yes, supports-claim partly); trust 55 -> 35; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **gf-rfc-keywords** — verdict `unsupported` (claims: gf-rfc-keywords-prior, keywords-not-required-for-normative-text, qa-consistent-style-explain, oasis-should-use-rfc2119, keywords-make-requirements-easy-to-spot). Prior text, kept word for word: "Requirements within the guideline MUST use RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) to indicate obligation levels."
  - against: Using the keywords is not required: normative text does not need them, and much normative text without them is still normative.
  - against: Specifications convey conformance requirements in different styles (RFC 2119 keywords, imperative voice, descriptive assertions); a specification must use a consistent style and tell readers which styles it uses and how to distinguish them.
  - against: OASIS says work products that become specifications should use RFC 2119 keywords: a recommendation, not a requirement.
  - against: RFC 2119 keywords make conformance requirements easy to spot, and are usually given distinctive formatting such as uppercase or bold.
- **gf-rfc-keywords-bold-or-uppercase** — verdict `contradicted` (claims: gf-rfc-keywords-bold-or-uppercase-prior, uppercase-only-meaning, lowercase-has-normal-english-meaning, bcp14-boilerplate, oasis-uppercase-only). Prior text, kept word for word: "Keywords MUST be bold or uppercase when used normatively."
  - against: Only the UPPERCASE forms of the keywords carry the defined BCP 14 meanings.
  - against: When the words are not capitalized they have their normal English meanings and BCP 14 does not apply to them.
  - against: A document that follows BCP 14 states near its beginning a boilerplate that names the keywords and says they carry the BCP 14 meaning only in all capitals.
  - against: OASIS writes RFC 2119 keywords in UPPERCASE; in lowercase they have only normal English meaning and state no requirement.
- **use-rfc-2119-keywords-for-behavioral-requirements** — verdict `unsupported` (claims: use-rfc-2119-keywords-for-behavioral-requirements-prior, keywords-not-required-for-normative-text, qa-consistent-style-explain, tab-keywordless-must-equivalent). Prior text, kept word for word: "Use RFC 2119 keywords for all behavioral requirements:" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Using the keywords is not required: normative text does not need them, and much normative text without them is still normative.
  - against: Specifications convey conformance requirements in different styles (RFC 2119 keywords, imperative voice, descriptive assertions); a specification must use a consistent style and tell readers which styles it uses and how to distinguish them.
  - against: Specifications state many requirements without any keyword, through 'is' statements and algorithm steps that are MUST-equivalent, so a keyword-only reading misses them.
- **rule-uses-rfc-2119-keywords** — verdict `unsupported` (claims: rule-uses-rfc-2119-keywords-prior, keywords-not-required-for-normative-text, oasis-should-use-rfc2119, infra-core-subset). Prior text, kept word for word: "**Use RFC 2119 keywords** for requirements — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY."
  - against: Using the keywords is not required: normative text does not need them, and much normative text without them is still normative.
  - against: OASIS says work products that become specifications should use RFC 2119 keywords: a recommendation, not a requirement.
  - against: WHATWG Infra encourages documents to limit themselves to must, must not, should and may.

## Open questions

- Case convention: follow RFC 8174 (only all-capital keywords carry meaning) or WHATWG Infra's willful violation (lowercase keywords carry the same meaning and are preferred for legibility); the sources support either if declared, and the owner chooses one.
- Whether skipping a SHOULD requires a documented reason (follow-must-address-should-checks) or only that the implications be understood and weighed (RFC 2119's wording); RFC 2119 does not require documentation.
- Whether warnings ever block /approve-artifact (an ESLint --max-warnings style threshold) or never do; the tools make a warning threshold optional and default to warnings not blocking.
- Whether rules restrict themselves to the five keywords MUST, MUST NOT, SHOULD, SHOULD NOT, MAY (as Infra encourages) or also admit SHALL, REQUIRED, RECOMMENDED and OPTIONAL as BCP 14 defines them.
- Whether a lowercase keyword found in rule text is reported as a WARN (as Bikeshed's opt-in accidental-2119 lint and ReSpec's warnings do) or a FAIL.
- Whether lint-artifact's GF-03 level 'WARN if missing' stays a warning; the sources support a keyword as SHOULD, which maps to a warning, but the owner decides.
- Whether keywords are additionally styled (bold, or the W3C Manual of Style's em with class rfc2119) for readability; no source makes styling carry the meaning, and a W3C editor recommends dropping the formatting requirement.

## Round 1 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R1.1: `a-complete-review-must-establish.md`, `what-a-reviewer-looks-for.md`, `writing-a-requirement.md`: the review bar makes SHOULD rules items that a passing review must establish, and these parts state the uppercase case convention without the condition the rules attach to it. Instances:
    - (a) Review bar bullet 1, "in the form subject, keyword, operation", makes `one-keyword-per-requirement` (SHOULD) a pass condition.
    - (b) Bullet 3 does the same for `state-the-keyword-interpretation` (SHOULD).
    - (c) Bullet 4 does the same for `no-keywords-in-non-normative-text` (SHOULD NOT).
    - (d) Bullet 5 does the same for `one-keyword-set-never-mixed` and `no-mixed-case-negation-or-may-not` (SHOULD / SHOULD NOT).
    - (e) Bullet 6, "Lint findings take their severity from the keyword", makes `keyword-sets-finding-severity` a pass condition. That rule is a SHOULD, applies "by default", and says "The level stays configurable per check".
    - Since "A review passes when it establishes every item above", items (a) to (e) contradict the bar's own last bullet: "Every SHOULD rule is kept, or the change says why not".
    - (f) Review bar bullet 1 says "in uppercase", the review focus says "one uppercase keyword", and how-to step 2 says "Pick one keyword, in uppercase". `keywords-meaningful-only-in-uppercase` is conditional ("Where the cookbook follows BCP 14 as RFC 8174 states it … A document that declares a different convention … is read by its declaration"), and the build bar keeps that condition. These three parts drop it, which settles owner-list open question 1 (the case convention). They also contradict the kept MUST rule `gf-rfc-keywords-bold-or-uppercase` ("bold or uppercase"), which the same review bar lists as kept "with no exception".
    - Fix: reword bullets 1 and 3 to 6 so that each SHOULD item is something the review checks, kept or skipped with a stated reason, rather than a pass condition. Or drop them and rely on the two "Every MUST/SHOULD rule is kept" bullets. In all three parts, replace the unconditional "uppercase" with the rule's conditional form, or with "in the form the document's declared convention gives it".
- R1.2: `rules.md`: the guideline breaks its own `one-keyword-per-requirement` rule ("in the active form 'X MUST do Y' rather than the passive 'X MUST be Y'"), and `examples.md` labels exactly this form "Weak, passive". Every instance outside the owner-list wording:
    - `must-is-absolute-requirement`: "A rule's MUST MUST be read as …"
    - `should-is-recommendation`: "A rule's SHOULD MUST be read as …" and "the full implications MUST be understood and carefully weighed".
    - `may-is-optional-behavior`: "A rule's MAY MUST be read as …"
    - `keywords-meaningful-only-in-uppercase`: "only the UPPERCASE form of a keyword MUST be read as carrying its defined meaning".
    - `keywords-only-where-required`: "Keywords SHOULD be used with care and sparingly".
    - Fix: name the actor and use an active verb, for example "A reader MUST treat a rule's MUST as an absolute requirement …", "a deviating builder MUST first understand and weigh the full implications", and "An author SHOULD use the keywords with care and sparingly …".
- R1.3: `rules.md`: the rules break the guideline's own `lowercase-keyword-in-rule-text-flagged` rule and its fantasai-backed point that an ordinary-sense keyword word in rule text is an editorial error to reword. Its own linter would flag these lowercase keyword words in named-rule text:
    - `should-is-recommendation`: "a preferred but not required course" and "valid reasons to deviate may exist".
    - `may-is-optional-behavior`: "a course of action permitted, not required".
    - Fix: reword without the keyword words, for example "a preferred but not obligatory course", "valid reasons to deviate can exist" and "permitted, not obligatory". Claim ids and mentioned words inside quotes ("must and shall", 'MUST not') are not instances.
- R1.4: `rules.md`, `use-core-keyword-subset`: the rule says rules "SHOULD limit themselves to MUST, MUST NOT, SHOULD and MAY", which leaves out SHOULD NOT. This conflicts with the rest of the guideline:
    - The kept owner-list rules (`gf-rfc-keywords`, `rule-uses-rfc-2119-keywords`) enumerate five keywords, including SHOULD NOT.
    - The build-bar lines for `gf-rfc-keywords` and `rule-uses-rfc-2119-keywords` also list five.
    - The guideline's own rules use SHOULD NOT in `no-keywords-in-non-normative-text`, `warn-findings-do-not-block` and `no-mixed-case-negation-or-may-not` (twice).
    - The reading-a-keyword table lists SHOULD NOT.
    - Open question 4 itself describes Infra's encouraged set as "the five keywords MUST, MUST NOT, SHOULD, SHOULD NOT, MAY".
    - The build-bar line for `use-core-keyword-subset` repeats the four-keyword list.
    - Fix: list SHOULD NOT in the rule and in its build-bar line, or say explicitly that SHOULD NOT is the negation of SHOULD and falls within the subset.
- R1.5: `rules.md`, `warn-findings-do-not-block`: the closing clause, "a threshold that makes warnings block is an opt-in setting", says that a warning threshold exists or is allowed. That answers owner-list open question 3 ("Whether warnings ever block /approve-artifact … or never do"). Fix: drop the clause, or recast it as what the sources report, for example "the tools cited make a warning threshold optional", without saying whether `/approve-artifact` admits one.
- R1.6: `artifact.json` `references` and `references.md`: sources behind cited claims are missing. These claims are cited by the rules:
    - ISO/IEC Directives Part 2 Annex H (https://www.mhonarc.org/archive/html/ietf/2011-09/pdfBUKoWRBJxm.pdf) backs `iso-shall-requirement`, `iso-should-preferred`, `iso-may-permission`, `iso-no-must-for-shall` and `iso-no-may-not`. `rationale.md` names "ISO/IEC Directives Part 2" and "ISO/IEC" twice, and no reference backs either.
    - Atkins, spec-prod 0017, backs `tab-drop-formatting-requirement` and `tab-keywordless-must-equivalent`.
    - Sperberg-McQueen, spec-prod 0018, backs `sperberg-mcqueen-lowercase-misuse`, `sperberg-mcqueen-focus-attention` and `sperberg-mcqueen-iso-avoids-nonstandard-senses`.
    - fantasai, spec-prod 0016 and 0019, backs `fantasai-styling-requirement` and `fantasai-lowercase-misuse-is-editorial-error`.
    - Caceres, spec-prod 0024, backs `caceres-respec-defaults-bcp14` and `lint-unmarked-keyword-usage`.
    - The plainlanguage.gov shall-and-must page backs `plainlanguage-must-not-shall`.
    - https://vale.sh/docs/keys/minalertlevel backs `vale-minalertlevel-ci`.
    - The GitHub default-setup configuration page backs `github-ruleset-blocks-merge`.
    - Fix: add each URL to `references` and to `references.md`. The internal `git:` sources of the `-prior` claims need no entry.
- R1.7: `artifact.json` `related`: the field is `[]`, so it does not connect the guideline to the guidelines it overlaps with:
    - `guideline-formatting` (99eb40d3-98a6-4213-9fee-f8a62694dba4). Per the area plan, it cites this topic for keyword case and severity.
    - `recipe-quality/behavioral-requirements` (04fe1298-3880-4584-8a4a-c7a538eb5193), which states its own RFC 2119 keyword rules.
    - Fix: add both UUIDs.
- R1.8: Sibling `guideline-formatting` (route there, not this topic's to fix): its `rules.md` restates keyword rules this topic owns. The area plan says "The formatting topics cite it, never restate it". The restated rules:
    - `gf-rfc-keywords`, which also merges in the bold-or-uppercase text.
    - `normative-keywords-only-where-required`, which duplicates this topic's `keywords-only-where-required`.
    - Fix in guideline-formatting: cite requirement-keywords instead of restating these rules.

Lint failed (`lint: fail 1`): fix each lint error in the draft. The review's `## Lint` section:

````
```
[FAIL] FM-03: Index entry matches folder
       -> cookbook/index.json has no entry for id 456f23bd-4523-47e8-9541-073ac046f2ad.
          It has no entry under cookbook/authoring at all, and `cookr validate` reports
          index/triggers.yaml drift. Run `cookr update` to regenerate the index.
[PASS] FM-01, FM-02, FM-04, FM-05, FM-06, FM-07, FM-08, FM-09, FM-10, FM-11, FM-11a, FM-12, FM-13
       (FM-06: approved-by and approved-date are not checked.)
[PASS] GF-01: Summary statement follows the H1
[PASS] GF-02: Structured guidance (rules, how-to, examples, bars)
[PASS] GF-03: RFC 2119 keywords in every rule
[PASS] gf-type-field, gf-title-heading, gf-change-history, gf-triggers-field (recipe-authoring)
[PASS] gf-roled-parts: every part has a role, with rules, review-focus, review-bar and build-bar all present
[PASS] gf-named-rules: kebab-case names, RFC 2119 keywords
[PASS] gf-build-bar: one line per named rule, 21 of 21
[PASS] gf-rule-cites-research: every rule ends with a citation, and validate reports no unknown-claim for this artifact
[PASS] gf-research-folder: research/ is present
[WARN] GF-04: Compliance section absent
       -> Optional, and only needed if other compliance checks reference this guideline.
[WARN] gf-rule-cites-research (owner-decides): four rules cite claims whose research verdict is unsupported or contradicted.
       -> gf-rfc-keywords, gf-rfc-keywords-bold-or-uppercase,
          use-rfc-2119-keywords-for-behavioral-requirements and rule-uses-rfc-2119-keywords
          cite *-prior claims. The owner decides whether to keep, reword or drop each one.

=== LINT SUMMARY ===
Artifact: requirement-keywords
Type: guideline
Pass: 23 | Warn: 2 | Fail: 1
RESULT: NOT CLEAN — 1 failing check.
```

The FM-03 fix is `cookr update`, which regenerates the index. The linter also pointed out a dangling colon in `use-rfc-2119-keywords-for-behavioral-requirements`. That is owner-list wording kept word for word, so it is exempt.

lint: fail 1
````
