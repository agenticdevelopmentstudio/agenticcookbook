# Review: project-record-linking

## Findings

none

## Checked

- The diff changes four places: the second paragraph of `intro.md`, step 5 of `linking-project-records.md`, the `child-record-carries-parent-link` rule in `rules.md`, and its line in `a-build-must-establish.md`. Nothing else changed, and every strength is the same as before.
- The new `intro.md` sentence follows the R1.1 fix. Where a kind of record's own guideline requires one of these links at a stronger level, that guideline governs for that kind, and this guideline is the baseline for the others. It names all four MUST rules from R1.1, and each name was checked against the sibling's `rules.md`: `acknowledge-contradicted-decisions` (decision-records), `blocked-task-references-blocker` (task-breakdown), `blocked-dependency-linked-to-affected-work` (dependency-tracking) and `blocked-milestone-has-issue-or-concern` (milestone-scheduling). Each is a MUST there. The sentence assigns them correctly: the supersession link for decisions, and the blocker link for tasks, dependencies and milestones.
- The `close-or-supersede-never-delete` overlap ("marked superseded") is covered by the same sentence, because that sentence makes decision-records govern supersession for decisions.
- `child-record-carries-parent-link` now reads "the link between them MAY be carried on the smaller record". The option is now which end carries the link, not whether the link exists. This matches the research and `rationale.md` ("only GitHub documents which end carries it"), so it no longer competes with task-breakdown `link-tasks-to-milestones` or issue-tracking `link-fix-change-to-issue` (both SHOULD). The citation is unchanged (ks-github-sub-issues-and-milestones, ks-github-closing-keywords) and still ends the rule.
- The `a-build-must-establish.md` line for that rule matches the new wording word for word: "where used, the link between a part record and the record it is part of is carried on the part record". There is still one build-bar line per rule (15).
- R1.2: the intro's six sibling mentions and step 5's "question for decision records" are now all `[adc.guideline.planning.project-management.<name>](cookbook:<uuid>)` links with the full rdid. Each UUID resolves in `cookbook/index.json` to the named sibling's path: decision-records 2b7a1593…, issue-tracking f77eeffe…, milestone-scheduling 023d4c91…, task-breakdown f264cc0b…, risk-tracking a55182ef…, dependency-tracking 3f978ba7…. All six are in `related`. No freeform sibling names remain in `intro.md` or `linking-project-records.md`.
- The intro's "No rule here is a MUST" is still accurate: the MUSTs it now mentions belong to the sibling guidelines.
- Owner list: the changed text settles none of the seven open questions. Step 5 still leaves decision amendments open, and now links to decision-records for it.

## Rulings

- R1.1: fixed — `intro.md` now says a kind's own guideline governs where it requires a link at a stronger level, and it names all four MUST rules with in-text links. `child-record-carries-parent-link` and its build-bar line now make the end optional, not the link. Every strength is kept.
- R1.2: fixed — all six sibling mentions in `intro.md` and the one in step 5 of `linking-project-records.md` are `[adc.guideline.planning.project-management.<name>](cookbook:<uuid>)` links, and each UUID resolves to its named sibling.

## Lint

/lint-artifact on `cookbook/guidelines/planning/project-management/project-record-linking`, run with this checkout's cookr. It compiled the folder to the scratchpad and ran `cookr validate`, which passed for the whole cookbook. It printed `owner-decides` warnings for rules in other guidelines and none for this one.

```
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md

[PASS] FM-01: YAML frontmatter present
[PASS] FM-02: id is a valid UUID (23e55c7c-...)
[PASS] FM-03: index.json entry matches folder and rdid adc.guideline.planning.project-management.project-record-linking
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.0
[PASS] FM-06: all required fields present
[PASS] FM-07: license MIT
[PASS] FM-08: copyright "2026 Mike Fullerton"
[PASS] FM-09: created and modified are ISO dates
[PASS] FM-10: summary is non-empty
[PASS] FM-11: H1 matches title
[PASS] FM-11a: links resolve (cookr validate passed)
[PASS] FM-12: Change History present, 1 row
[PASS] FM-13: no TODO/TBD/FIXME/placeholder text
[PASS] GF-01: summary statement follows H1
[PASS] GF-02: structured guidance (rules, tables, subsections)
[PASS] GF-03: rules use SHOULD, SHOULD NOT and MAY
[WARN] GF-04: no ## Compliance section
       -> Optional, and only expected when other compliance checks reference this guideline.
[PASS] gf-triggers-field: triggers is present (empty list is allowed)
[PASS] gf-roled-parts: all parts have roles, with rules, review-focus, review-bar and build-bar present
[PASS] gf-named-rules: 15 unique kebab-case rules, each with an RFC 2119 keyword
[PASS] gf-build-bar: 15 build-bar lines, matching the 15 rules in order
[PASS] gf-research-folder: research.json and research.md are present, with the four headings in order
       -> All 28 claims have every required field, and every cited claim has a verdict.
[PASS] gf-rule-cites-research: every rule ends with a citation, and no cited id is missing from research.json

=== LINT SUMMARY ===
Artifact: project-record-linking
Type: guideline
Pass: 23 | Warn: 1 | Fail: 0
RESULT: CLEAN — artifact passes all checks.
```

The one WARN (GF-04) is about an optional section and is not an error.

lint: clean

verdict: pass
