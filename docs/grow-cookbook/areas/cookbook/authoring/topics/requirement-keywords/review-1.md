# Review: requirement-keywords

## Findings

- `a-complete-review-must-establish.md`, `what-a-reviewer-looks-for.md`, `writing-a-requirement.md`: the review bar makes SHOULD rules items that a passing review must establish, and these parts state the uppercase case convention without the condition the rules attach to it. Instances:
  - (a) Review bar bullet 1, "in the form subject, keyword, operation", makes `one-keyword-per-requirement` (SHOULD) a pass condition.
  - (b) Bullet 3 does the same for `state-the-keyword-interpretation` (SHOULD).
  - (c) Bullet 4 does the same for `no-keywords-in-non-normative-text` (SHOULD NOT).
  - (d) Bullet 5 does the same for `one-keyword-set-never-mixed` and `no-mixed-case-negation-or-may-not` (SHOULD / SHOULD NOT).
  - (e) Bullet 6, "Lint findings take their severity from the keyword", makes `keyword-sets-finding-severity` a pass condition. That rule is a SHOULD, applies "by default", and says "The level stays configurable per check".
  - Since "A review passes when it establishes every item above", items (a) to (e) contradict the bar's own last bullet: "Every SHOULD rule is kept, or the change says why not".
  - (f) Review bar bullet 1 says "in uppercase", the review focus says "one uppercase keyword", and how-to step 2 says "Pick one keyword, in uppercase". `keywords-meaningful-only-in-uppercase` is conditional ("Where the cookbook follows BCP 14 as RFC 8174 states it … A document that declares a different convention … is read by its declaration"), and the build bar keeps that condition. These three parts drop it, which settles owner-list open question 1 (the case convention). They also contradict the kept MUST rule `gf-rfc-keywords-bold-or-uppercase` ("bold or uppercase"), which the same review bar lists as kept "with no exception".
  - Fix: reword bullets 1 and 3 to 6 so that each SHOULD item is something the review checks, kept or skipped with a stated reason, rather than a pass condition. Or drop them and rely on the two "Every MUST/SHOULD rule is kept" bullets. In all three parts, replace the unconditional "uppercase" with the rule's conditional form, or with "in the form the document's declared convention gives it".
- `rules.md`: the guideline breaks its own `one-keyword-per-requirement` rule ("in the active form 'X MUST do Y' rather than the passive 'X MUST be Y'"), and `examples.md` labels exactly this form "Weak, passive". Every instance outside the owner-list wording:
  - `must-is-absolute-requirement`: "A rule's MUST MUST be read as …"
  - `should-is-recommendation`: "A rule's SHOULD MUST be read as …" and "the full implications MUST be understood and carefully weighed".
  - `may-is-optional-behavior`: "A rule's MAY MUST be read as …"
  - `keywords-meaningful-only-in-uppercase`: "only the UPPERCASE form of a keyword MUST be read as carrying its defined meaning".
  - `keywords-only-where-required`: "Keywords SHOULD be used with care and sparingly".
  - Fix: name the actor and use an active verb, for example "A reader MUST treat a rule's MUST as an absolute requirement …", "a deviating builder MUST first understand and weigh the full implications", and "An author SHOULD use the keywords with care and sparingly …".
- `rules.md`: the rules break the guideline's own `lowercase-keyword-in-rule-text-flagged` rule and its fantasai-backed point that an ordinary-sense keyword word in rule text is an editorial error to reword. Its own linter would flag these lowercase keyword words in named-rule text:
  - `should-is-recommendation`: "a preferred but not required course" and "valid reasons to deviate may exist".
  - `may-is-optional-behavior`: "a course of action permitted, not required".
  - Fix: reword without the keyword words, for example "a preferred but not obligatory course", "valid reasons to deviate can exist" and "permitted, not obligatory". Claim ids and mentioned words inside quotes ("must and shall", 'MUST not') are not instances.
- `rules.md`, `use-core-keyword-subset`: the rule says rules "SHOULD limit themselves to MUST, MUST NOT, SHOULD and MAY", which leaves out SHOULD NOT. This conflicts with the rest of the guideline:
  - The kept owner-list rules (`gf-rfc-keywords`, `rule-uses-rfc-2119-keywords`) enumerate five keywords, including SHOULD NOT.
  - The build-bar lines for `gf-rfc-keywords` and `rule-uses-rfc-2119-keywords` also list five.
  - The guideline's own rules use SHOULD NOT in `no-keywords-in-non-normative-text`, `warn-findings-do-not-block` and `no-mixed-case-negation-or-may-not` (twice).
  - The reading-a-keyword table lists SHOULD NOT.
  - Open question 4 itself describes Infra's encouraged set as "the five keywords MUST, MUST NOT, SHOULD, SHOULD NOT, MAY".
  - The build-bar line for `use-core-keyword-subset` repeats the four-keyword list.
  - Fix: list SHOULD NOT in the rule and in its build-bar line, or say explicitly that SHOULD NOT is the negation of SHOULD and falls within the subset.
- `rules.md`, `warn-findings-do-not-block`: the closing clause, "a threshold that makes warnings block is an opt-in setting", says that a warning threshold exists or is allowed. That answers owner-list open question 3 ("Whether warnings ever block /approve-artifact … or never do"). Fix: drop the clause, or recast it as what the sources report, for example "the tools cited make a warning threshold optional", without saying whether `/approve-artifact` admits one.
- `artifact.json` `references` and `references.md`: sources behind cited claims are missing. These claims are cited by the rules:
  - ISO/IEC Directives Part 2 Annex H (https://www.mhonarc.org/archive/html/ietf/2011-09/pdfBUKoWRBJxm.pdf) backs `iso-shall-requirement`, `iso-should-preferred`, `iso-may-permission`, `iso-no-must-for-shall` and `iso-no-may-not`. `rationale.md` names "ISO/IEC Directives Part 2" and "ISO/IEC" twice, and no reference backs either.
  - Atkins, spec-prod 0017, backs `tab-drop-formatting-requirement` and `tab-keywordless-must-equivalent`.
  - Sperberg-McQueen, spec-prod 0018, backs `sperberg-mcqueen-lowercase-misuse`, `sperberg-mcqueen-focus-attention` and `sperberg-mcqueen-iso-avoids-nonstandard-senses`.
  - fantasai, spec-prod 0016 and 0019, backs `fantasai-styling-requirement` and `fantasai-lowercase-misuse-is-editorial-error`.
  - Caceres, spec-prod 0024, backs `caceres-respec-defaults-bcp14` and `lint-unmarked-keyword-usage`.
  - The plainlanguage.gov shall-and-must page backs `plainlanguage-must-not-shall`.
  - https://vale.sh/docs/keys/minalertlevel backs `vale-minalertlevel-ci`.
  - The GitHub default-setup configuration page backs `github-ruleset-blocks-merge`.
  - Fix: add each URL to `references` and to `references.md`. The internal `git:` sources of the `-prior` claims need no entry.
- `artifact.json` `related`: the field is `[]`, so it does not connect the guideline to the guidelines it overlaps with:
  - `guideline-formatting` (99eb40d3-98a6-4213-9fee-f8a62694dba4). Per the area plan, it cites this topic for keyword case and severity.
  - `recipe-quality/behavioral-requirements` (04fe1298-3880-4584-8a4a-c7a538eb5193), which states its own RFC 2119 keyword rules.
  - Fix: add both UUIDs.
- Sibling `guideline-formatting` (route there, not this topic's to fix): its `rules.md` restates keyword rules this topic owns. The area plan says "The formatting topics cite it, never restate it". The restated rules:
  - `gf-rfc-keywords`, which also merges in the bold-or-uppercase text.
  - `normative-keywords-only-where-required`, which duplicates this topic's `keywords-only-where-required`.
  - Fix in guideline-formatting: cite requirement-keywords instead of restating these rules.

## Checked

- The four owner-list rules (`gf-rfc-keywords`, `gf-rfc-keywords-bold-or-uppercase`, `use-rfc-2119-keywords-for-behavioral-requirements` and `rule-uses-rfc-2119-keywords`) keep their prior text word for word and each cites its `-prior` claim.
- The one lead-in, "An artifact MUST follow this convention:", matches owner-list.md.
- Every verdict rule (21) is present under its fixed name. No supported or new verdict is left without a rule.
- Every rule ends with exactly one citation and nothing after it. Every cited id exists in research.json and is named by a verdict. `cookr roles check` reports ok, 21 rules, no findings.
- Strength rule: none of the MUST rules cites a refuted claim. The MUST rules are `must-is-absolute-requirement`, `should-is-recommendation`, `may-is-optional-behavior`, `follow-must-address-should-checks`, `approve-on-zero-fail` and `keywords-meaningful-only-in-uppercase`.
  - `approve-on-zero-fail` drops the refuted `markdownlint-cli2-exit-codes` and `bikeshed-die-on-default-fatal` from its verdict list.
  - `keywords-meaningful-only-in-uppercase` drops the refuted `bikeshed-lowercase-for-readability`.
  - Criterion 4 permits both.
- Every rule citing one of the 15 refuted claims is at SHOULD, SHOULD NOT or MAY. `state-how-keywordless-text-is-read` is correctly a SHOULD, not the research summary's MUST, because `qa-consistent-style-explain` is refuted.
- The SHOULD rules follow from their claims. They are: `keyword-sets-finding-severity` (an inferred mapping, configurable per check), `state-the-keyword-interpretation`, `no-keywords-in-non-normative-text`, `one-keyword-per-requirement`, `no-mixed-case-negation-or-may-not`, `one-keyword-set-never-mixed`, `keywords-only-where-required` and `lowercase-keyword-in-rule-text-flagged`.
- Open questions 2, 5, 6 and 7 are left unsettled:
  - The documented-reason wording of `follow-must-address-should-checks` is open question 2's subject and is not a finding.
  - `lowercase-keyword-in-rule-text-flagged` names no severity.
  - `keyword-sets-finding-severity` leaves the level configurable.
  - `keywords-only-where-required` reports both sides on styling.
- `oasis-should-use-rfc2119` is uncited. It is named only by unsupported verdicts, so no rule is owed for it.
- Frontmatter:
  - The summary is 152 characters and describes the new text.
  - The tags fit.
  - `platforms: []` suits a cookbook-authoring guideline.
  - Version, modified date and history are left for stage 5.
- Structure: intro, Rules, how-to, Examples, What a reviewer looks for, A complete review must establish, A build must establish, Rationale, References and Change History are all present and roled. The build bar has exactly one line per named rule. The guideline compiles.
- Keywords in the reading-a-keyword table, the examples and the rationale are quoted mentions, not requirements, so `no-keywords-in-non-normative-text` is not broken there.
- `cookr validate` shows only owner-decides notes for this artifact (the four `-prior` rules). Its overall failure comes from index drift and from neutrality findings on other topics.
- The recipe-quality guidelines were checked. Template-conformance holds: the summary is a single line of 160 characters or fewer, the link fields are sequences, the H1 matches the title, and Change History comes last. Source-fidelity holds: the rules trace to the research. Cookbook-compliance raised no conflict for this topic to fix; the keyword-set and documentation differences from behavioral-requirements are open questions 2 and 4.

## Lint

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

verdict: fail
