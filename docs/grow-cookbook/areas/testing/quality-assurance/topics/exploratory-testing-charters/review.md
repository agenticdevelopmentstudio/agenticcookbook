# Review: exploratory-testing-charters

## Findings

none

## Checked

- diff-3.md changes one phrase only: `rationale.md`, last paragraph, "the sizing, splitting, stakeholder and new-charter rules on Hendrickson" became "the finishable-target, splitting, stakeholder and new-charter rules on Hendrickson".
- `charter-target-is-finishable` (rules.md) cites only `hendrickson-too-broad`, so attributing the finishable-target rule to Hendrickson alone is accurate.
- `charter-gives-direction-not-tests`, which also cites the ISTQB Test Analyst claims `charter-does-not-list-tests` and `charter-detail-trade-off`, is no longer in the single-publisher list.
- The rest of the sentence is unchanged and its attributions still hold (as R2.1 found): splitting, stakeholder and new-charter rules on Hendrickson; opportunity-time and to-do-sheet rules on SBTM; the documentation rule on Bolton; the vacuous-expectation rule on the RST guide.
- No other text changed this round, so there is nothing else to re-review.
- `cookr roles check` on the folder: ok, 41 rules, no findings, all four skills compile.

## Rulings

- R2.1: fixed — "the sizing" was replaced with "the finishable-target", naming `charter-target-is-finishable`, which cites only `hendrickson-too-broad`; `charter-gives-direction-not-tests`, which has ISTQB support, is no longer listed as resting on Hendrickson alone.

## Lint

/lint-artifact on `cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters`, compiled to the scratchpad:

- PASS: FM-01 to FM-13, FM-03/FM-11a (`cookr validate` passed, index entry matches), GF-01, GF-02, GF-03 / gf-named-rules (41 named rules, each with an RFC keyword, no repeated names), gf-roled-parts (build-bar has 41 lines for 41 rules, names match), gf-research-folder, gf-rule-cites-research (every rule cites, every cited claim exists), gf-triggers-field (SHOULD only), gf-change-history.
- WARN: GF-04, no `## Compliance` section. It applies only when another compliance check references this guideline, and none does.
- Summary: Pass 24 | Warn 1 | Fail 0. RESULT: CLEAN.

lint: clean

verdict: pass
