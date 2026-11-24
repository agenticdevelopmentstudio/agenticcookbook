# Review: decision-records

## Findings

none

## Checked

- `rules.md`, `supersession-links-both-ways` now reads "the superseded record's status SHOULD link to the record that replaces it". It no longer repeats the two behaviours that `acknowledge-contradicted-decisions` requires at MUST (marking the earlier record superseded, and the new record naming it). It keeps its three citations, and SHOULD is within the refuted `supersession-header-fields` and `gds-way-supersede-must`.
- `a-build-must-establish.md`: the `supersession-links-both-ways` line ("each superseded record's status links to its replacement") matches the narrowed rule. The `backfill-undocumented-decisions` line now reads "where used", which matches the MAY rule and the other MAY rule's line (`record-confidence-level`). The file still has one line per rule (18).
- `what-a-reviewer-looks-for.md`: the changed closing sentence ("each superseded record's status links to its replacement") matches the narrowed rule. Its other clauses match `acknowledge-contradicted-decisions` (MUST) and `supersede-never-edit-accepted-records` (SHOULD NOT).
- `intro.md`, first paragraph: "never silently contradicts" is the one absolute, and it matches the MUST in `acknowledge-contradicted-decisions`. "A new record rather than an edit" and "marks the old one superseded" match that rule's MUST text ("written as a new record that names the earlier decision, and the earlier record is marked superseded"). The status link is a lowercase "should", which matches the SHOULD in `supersession-links-both-ways`. The intro no longer says that accepted records are never edited.
- `intro.md`, second paragraph: datastore selection is now the in-text link `[adc.guideline.planning.data.datastore-selection](cookbook:6a653107-929d-418e-865d-636373a27b02)`. The link resolves, and the uuid matches the `related` entry.
- Index: `cookbook/index.json` now holds id `2b7a1593-48e0-4bbe-8e14-0df7a863628d`, with path `guidelines/planning/project-management/decision-records` and rdid `adc.guideline.planning.project-management.decision-records`. `guidelines/INDEX.md` lists Decision Records under project-management. The index drift that `cookr validate` still reports for `guidelines/INDEX.md` does not come from this artifact. Sibling topics that are not yet indexed, such as project-record-linking, account for it.
- `cookr roles check` is ok, with 18 rules, no findings, and the builder and verifier skills compiled. `cookr validate` reports no issue for this artifact. Its one frontmatter issue is in `project-record-linking/research/research.md`, a sibling.
- Nothing else changed in the diff. No changed text makes a factual error against a cited claim.

## Rulings

- R1.1: fixed — `supersession-links-both-ways` is cut to the status link alone, at SHOULD, with the same citations. Its build-bar line and the review-focus sentence are narrowed to match, so no behaviour is required at two strengths.
- R1.2: fixed — the backfill build-bar line now reads "where used, past decisions recorded retroactively are ones whose data was available", which is conditional on use and matches the MAY rule.
- R1.3: fixed — the intro keeps "never silently contradicts" as its one absolute. It drops "never edits", and it softens the link to "should", which matches the rules' strengths.
- R1.4: fixed — datastore selection is now an in-text `[rdid](cookbook:uuid)` link, as cross-recipe-consistency requires.
- R1.5: fixed — the author's dispute is right that indexing is outside the draft. Even so, the entry is now present in `cookbook/index.json` with the expected path and rdid, and in `guidelines/INDEX.md`, and lint FM-03 passes. The finding is resolved either way.

## Lint

/lint-artifact on `cookbook/guidelines/planning/project-management/decision-records`, run with this checkout's cookr:

```
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md

[PASS] FM-01: YAML frontmatter block present
[PASS] FM-02: id is a valid UUID (2b7a1593-48e0-4bbe-8e14-0df7a863628d)
[PASS] FM-03: index.json entry matches the folder (rdid adc.guideline.planning.project-management.decision-records, no domain field)
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.0 is valid semver
[PASS] FM-06: all required fields present
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright "2026 Mike Fullerton"
[PASS] FM-09: created and modified are ISO dates
[PASS] FM-10: summary is non-empty
[PASS] FM-11: H1 matches title
[PASS] FM-11a: links resolve (related UUID 6a653107... and the in-text cookbook: link)
[PASS] FM-12: Change History present with one row
[PASS] FM-13: no TODO, TBD, FIXME or placeholder text
[PASS] GF-01 / gf-summary-statement: the summary paragraph follows the H1
[PASS] GF-02 / gf-structured-guidance: rules bullets, numbered steps, examples
[PASS] GF-03 / gf-rfc-keywords: every rule carries MUST, SHOULD, SHOULD NOT or MAY
[PASS] GF-04 / gf-compliance-section: no Compliance section, and nothing references this guideline's checks, so it is not required
[PASS] gf-triggers-field: triggers is an empty list, which is acceptable
[PASS] gf-roled-parts: the parts have the roles rules, how-to, examples, review-focus, review-bar, build-bar, rationale and references; none are missing or unknown
[PASS] gf-named-rules: all rule bullets are named and unique, each with an RFC 2119 keyword
[PASS] gf-research-folder: research.json and research.md are present; every cited claim exists and has a verdict
[PASS] gf-rule-cites-research: each rule ends with a single (claim: ...) or (claims: ...) citation
[PASS] build-bar: one line per rule (18 lines for 18 rules)

=== LINT SUMMARY ===
Artifact: decision-records
Type: guideline
Pass: 24 | Warn: 0 | Fail: 0
RESULT: CLEAN — artifact passes all checks.
```

The lint's gf-named-rules line gave a count of 17 rule bullets. `rules.md` and `cookr roles check` both count 18, so the line above leaves the count out. `cookr validate` also reports two cookbook-wide issues that are not about this artifact: the frontmatter of `project-record-linking/research/research.md`, and drift in `guidelines/INDEX.md`.

lint: clean

verdict: pass
