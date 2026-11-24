# Review: milestone-scheduling

## Findings

none

## Checked

- `rules.md` `define-and-sequence-milestones`: it keeps its fixed name and now requires only that the milestones are defined, put in sequence and given recorded dependency chains, with the same citations. The target date and status are gone from it, so it no longer overlaps the owner-listed `milestone-has-status-and-target-date`.
- `rules.md` `track-milestone-progress`: the new SHOULD rule cites `github-milestones-due-date-progress` and `linear-milestones-optional-date`. Both exist in research.json, a verdict names both, both have trust 85, and both state completion percentages, so they support tracking progress at SHOULD.
- `a-build-must-establish.md`: the `define-and-sequence-milestones` line is narrowed to match the rule, and the new `track-milestone-progress` line is there. `cookr roles check` reports ok, with 37 rules and no findings, and lint confirms 37 build-bar lines that match the 37 rule names one for one.
- `what-a-reviewer-looks-for.md` first two bullets and `a-complete-review-must-establish.md` first bullet: both are narrowed to defined, sequenced and recorded chains, plus progress tracked. Neither still asks for "dated" or status at a strength that contradicts the owner-listed rule.
- `rules.md` `justify-missing-logic` and `justify-unavoidable-hard-constraints`: both are now MUST. That matches the "must" in the GAO quotes of `missing-logic-justified` and `avoid-hard-date-constraints`, and the second check refuted neither claim.
- `rationale.md` paragraphs 1 and 2: they now say "most of its practice at SHOULD" and name the cycle rule and the two justification rules as the MUSTs. They also explain that the justification MUSTs apply only on a departure. All of this is consistent with `rules.md`.
- `examples.md` cycle sentence: I ran the example under Python 3 with `start` depending on `launch` and `PYTHONHASHSEED` set to 0 through 19. All 20 runs printed `api-freeze -> docs-ready -> launch -> start -> api-freeze`, which matches the text. The parenthetical now describes graphlib's successor order correctly, which keeps the example faithful to `topological-order-iff-acyclic`.
- `artifact.json` `related`: it holds both sibling UUIDs, `3f978ba7-c8c1-4b53-8fda-12e5a6966b75` (dependency-tracking) and `f264cc0b-45d3-4593-a437-7371610c5a8a` (task-breakdown). `intro.md` paragraph 2 and the last paragraph of `rationale.md` link both as `[adc.guideline.planning.project-management.<name>](cookbook:<uuid>)`, and `cookr validate` resolves every link. project-record-linking stays freeform, as asked, because that topic has no UUID yet.
- `artifact.json` `summary`: it is still 160 characters or fewer and still describes the text.
- Owner-listed rules `milestone-has-status-and-target-date` and `blocked-milestone-has-issue-or-concern`: neither changed this round. Each keeps its prior text word for word behind the listed lead-in and cites its `-prior` claim.

## Rulings

- R1.1: fixed — `define-and-sequence-milestones` is cut to define, sequence and record the chains, and the date and status are left to the owner-listed rule. Progress tracking is the new SHOULD rule `track-milestone-progress`, which has its own build-bar line, and the build-bar, review-focus and review-bar wording is narrowed to match.
- R1.2: fixed — both justification rules are now MUST, matching their unrefuted "must" claims, and `rationale.md` paragraphs 1 and 2 name them as MUSTs.
- R1.3: fixed — the shown message is the real graphlib output, confirmed over 20 hash seeds, and the parenthetical now describes the successor order.
- R1.4: fixed — both sibling UUIDs are in `related`, and the intro and rationale mentions are UUID links in the standard format. project-record-linking stays freeform.

## Lint

Type: guideline | Compliance: `tbd/compliance/artifact-formatting/guideline-formatting.md`

The source folder compiled. `cookr validate` passed with no failures. It printed some informational warnings, which the lint agent saw only cut off: they are about rules the research marks unsupported or contradicted, which the owner keeps, rewords or drops.

```
[PASS] FM-01: Frontmatter present
[PASS] FM-02: id is a valid UUID (023d4c91-d797-4e82-880c-a4ad7906a54a)
[PASS] FM-03: Index entry matches folder (path and rdid adc.guideline.planning.project-management.milestone-scheduling)
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.0
[PASS] FM-06: All required fields present
[PASS] FM-07: license MIT
[PASS] FM-08: copyright "2026 Mike Fullerton"
[PASS] FM-09: created and modified are ISO dates
[PASS] FM-10: summary is non-empty
[PASS] FM-11: H1 matches title
[PASS] FM-11a: Links resolve (both related UUIDs are in index.json; cookr validate passed)
[PASS] FM-12: Change History present with a row
[PASS] FM-13: No placeholder text
[PASS] GF-01: Summary statement follows H1
[PASS] GF-02: Structured guidance (bullets and subsections)
[PASS] GF-03: RFC 2119 keywords used (41)
[WARN] GF-04: No Compliance section
       -> Recommended only when other compliance checks reference this guideline.
[PASS] gf-roled-parts: Every part has a role. Each of rules, review-focus, review-bar and build-bar has a part.
[PASS] gf-roled-parts: The build-bar has exactly 37 lines, matching the 37 rule names one for one.
[PASS] gf-named-rules: 37 named rules, unique names, each with a keyword
[PASS] gf-research-folder: research.json (50 claims) and research.md present, with the four headings in order
[PASS] gf-rule-cites-research: Every rule ends with a citation, and every cited claim id exists
[PASS] gf-triggers-field: Not required here (the field is not in the required list)

=== LINT SUMMARY ===
Artifact: milestone-scheduling
Type: guideline
Pass: 22 | Warn: 1 | Fail: 0
RESULT: CLEAN — artifact passes all checks.
```

lint: clean

verdict: pass
