# Review: requirement-keywords

## Findings

none

## Checked

- Every rule's citations exist in research.json, and every cited claim is named by some verdict (scripted check: no missing, no unnamed ids), including `rfc2119-should-not-recommendation`, newly cited by `use-core-keyword-subset`.
- Every `supported` and `new` verdict (17 rules) still has its rule in `rules.md`; prior rule names are unchanged.
- The four owner-list rules keep their prior text word for word, citing `<rule>-prior`; `use-rfc-2119-keywords-for-behavioral-requirements` carries only the owner-listed lead-in "An artifact MUST follow this convention:".
- The reworded rules (`must-is-absolute-requirement`, `should-is-recommendation`, `may-is-optional-behavior`, `keywords-meaningful-only-in-uppercase`, `keywords-only-where-required`) now name an actor with an active verb and stay at the strength of their claims: none cites a claim the second check refuted.
- The changed rule text no longer uses keyword words in their ordinary sense ("not obligatory", "can exist"); 'truly optional', 'must', 'shall' and 'MAY NOT' appear only quoted, as mentioned words.
- `should-is-recommendation`, `may-is-optional-behavior` and `use-core-keyword-subset` follow their cited RFC 2119 claims (`rfc2119-should-recommendation`, `rfc2119-should-not-recommendation`, `rfc2119-may-truly-optional`) and ISO claims (`iso-should-preferred`, `iso-may-permission`).
- `warn-findings-do-not-block` now ends at "only FAIL findings do" and no longer settles owner-list open question 3.
- `use-core-keyword-subset` and its build-bar line list all five keywords, consistent with the owner-list rules, the reading table and open question 4; the rule still leaves SHALL/REQUIRED/RECOMMENDED/OPTIONAL to the owner only as a SHOULD.
- The review bar now holds only the two "Every MUST rule" / "Every SHOULD rule was checked" items, so no SHOULD rule is a pass condition; the review focus puts the SHOULD items under "checks whether the change keeps it or states why it skips it".
- The review focus states case as the rules do: "bold or uppercase where it is used normatively" (owner rule `gf-rfc-keywords-bold-or-uppercase`) and uppercase only "where the document follows BCP 14 as RFC 8174 states it"; how-to step 2 defers to "the document's declared convention". Neither settles open question 1.
- The reading-a-keyword table's MAY meaning, "Left to choice", and the build-bar line "treated as obligatory" are consistent with `rfc2119-may-truly-optional`.
- `artifact.json` `references` and `references.md` now hold every source behind a cited claim: ISO/IEC Directives Part 2 Annex H, spec-prod 0016, 0017, 0018, 0019 and 0024, plainlanguage.gov, Vale MinAlertLevel and the GitHub default-setup page; the two lists match one for one.
- `artifact.json` `related` lists guideline-formatting (99eb40d3-98a6-4213-9fee-f8a62694dba4) and recipe-quality/behavioral-requirements (04fe1298-3880-4584-8a4a-c7a538eb5193).
- `summary` is 156 characters and describes the new text; `tags` and `platforms` fit the guideline.
- `cookr roles check` on the folder: ok, 21 rules, no findings, four skills compiled.
- R1.8 appears under "From requirement-keywords's review" in guideline-formatting's write-brief.md.

## Rulings

- R1.1: fixed — review-bar bullets 1 to 6 are dropped, leaving the MUST-kept and SHOULD-checked items; the review focus and how-to step 2 now give case conditionally and keep "bold or uppercase".
- R1.2: fixed — every listed instance now names an actor with an active verb ("A builder or reviewer MUST treat …", "a builder who deviates MUST first understand …", "a reader MUST take …", "An author SHOULD use …").
- R1.3: fixed — "not obligatory", "can exist" and "permitted, not obligatory" replace the ordinary-sense keyword words.
- R1.4: fixed — `use-core-keyword-subset` and its build-bar line list SHOULD NOT, and the rule cites `rfc2119-should-not-recommendation`.
- R1.5: fixed — the opt-in threshold clause is dropped.
- R1.6: fixed — every listed source is in `references` and `references.md`.
- R1.7: fixed — both UUIDs are in `related`.
- R1.8: routed — it belongs to the sibling guideline-formatting and is recorded in that sibling's write-brief.md.

## Lint

lint-artifact v2.0.1 on `cookbook/guidelines/cookbook/authoring/requirement-keywords` (type guideline, compliance `tbd/compliance/artifact-formatting/guideline-formatting.md`), cookr run from this checkout; `cookr validate` passed on the whole cookbook.

```
[PASS] FM-01: Frontmatter block present (compiled doc)
[PASS] FM-02: id is a valid UUID (456f23bd-4523-47e8-9541-073ac046f2ad)
[PASS] FM-03: index.json entry matches folder; rdid adc.guideline.cookbook.authoring.requirement-keywords; no domain field
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.0 is valid semver
[PASS] FM-06: all required fields present
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright "2026 Mike Fullerton"
[PASS] FM-09: created and modified are ISO dates
[PASS] FM-10: summary is non-empty
[PASS] FM-11: H1 "Requirement Keywords" matches title
[PASS] FM-11a: links resolve (cookr validate passed)
[PASS] FM-12: Change History has 1 row
[PASS] FM-13: no TODO, TBD, FIXME, placeholder or fill-in text
[PASS] GF-01: summary statement follows H1
[PASS] GF-02: structured guidance (named rule bullets and subsections)
[PASS] GF-03: rules use RFC 2119 keywords
[PASS] GF-04: no Compliance section; the guideline is optional there and nothing in this run references it
[PASS] gf-triggers-field: triggers [recipe-authoring]
[PASS] gf-roled-parts: rules, review-focus, review-bar and build-bar parts all present
[PASS] gf-named-rules: every rules bullet is a unique kebab-name rule with a keyword
[PASS] gf-build-bar: 21 build-bar lines, one per named rule
[PASS] gf-research-folder: research.json and research.md present, with the four required headings in order
[PASS] gf-rule-cites-research: every rule ends with a citation; validate found all cited ids in research.json

=== LINT SUMMARY ===
Artifact: requirement-keywords
Type: guideline
Pass: 24 | Warn: 0 | Fail: 0
```

RESULT: CLEAN — artifact passes all checks. (The linter notes that `use-rfc-2119-keywords-for-behavioral-requirements` ends with a colon; that is the owner-list prior text, kept word for word, and not a finding.)

lint: clean

verdict: pass
