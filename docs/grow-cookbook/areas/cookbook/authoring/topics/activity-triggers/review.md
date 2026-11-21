# Review: activity-triggers

## Findings

none

## Checked

- `rules.md` new rule **task-set-size-reference-point** cites `ev-fifty-information-needs`, which exists in research.json and is named by the `new` verdict for measure-trigger-selection-with-labelled-tasks; the citation closes the rule.
- The rule is at SHOULD, within the strength of its one claim (a textbook rule of thumb, trust 74, not refuted by the second check), and states the 50 as a reference point ("usually been found a sufficient minimum"), faithful to the quote.
- The rule leaves the adopted size to the owner, matching the owner list's open question on the task set's size and `measuring-selection.md` step 1; it does not settle the open question.
- `a-build-must-establish.md` gains a matching `task-set-size-reference-point` line, consistent with the rule and with how its neighbours are listed.
- No other text changed this round (diff-3.md shows only these two additions); `cookr roles check` is ok with 59 rules and no findings.
- No `supported` or `new` claim is left uncited after the fix.

## Rulings

- R2.1: fixed — `ev-fifty-information-needs` is cited again, on the new rule task-set-size-reference-point at SHOULD, giving the rule of thumb as the reference point and leaving the adopted count to the owner.

## Lint

lint-artifact v2.0.1, guideline, compliance tbd/compliance/artifact-formatting/guideline-formatting.md.
Pass: 24 | Warn: 2 | Fail: 0 — RESULT: CLEAN.
- [WARN] GF-04: no `## Compliance` section (optional).
- [WARN] gf-roled-parts / gf-named-rules: confirmed by `cookr validate` only, not part by part.
`cookr validate` ended "Validation passed".
lint: clean

verdict: pass
