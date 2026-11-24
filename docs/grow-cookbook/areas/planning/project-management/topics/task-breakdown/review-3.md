# Review: task-breakdown

## Findings

none

## Checked

- diff-3.md changes only the 80-hour and WBS-scope lines named in R2.1. No other text changed this round.
- `rules.md` work-package-within-eighty-hours now reads "no more than about 80 hours of effort". That matches `wbs-eighty-hour-heuristic` ("at about 80 hours"), a heuristic with no study behind it, at SHOULD.
- `rules.md` work-package-within-one-reporting-period keeps its "In a work breakdown structure" scope at SHOULD. It follows from the same claim.
- `a-build-must-establish.md` work-package-within-eighty-hours reads "where a WBS is used … about 80 hours of effort or less", so the bar tests what the rule says.
- `a-complete-review-must-establish.md` line 3 is now scoped by "where a WBS is used". Line 5 reads "every WBS work package is within about 80 hours and one reporting period".
- `what-a-reviewer-looks-for.md` line 3 is now scoped by "in a work breakdown structure". Line 6 reads "a WBS work package over about 80 hours or one reporting period".
- `breaking-work-into-tasks.md` step 4 reads "WBS work packages within about 80 hours and one reporting period". Step 1 already had its WBS scope.
- A grep of the guideline's parts finds no 80-hour or work-package line left without "about" or WBS scope. The only remaining mention is rationale.md's "the WBS 80-hour rule", which names the heuristic, did not change this round, and already sits in WBS context.

## Rulings

- R2.1: fixed — "about 80 hours" is restored in the rule and in every 80-hour echo (build bar, review bar, review focus, how-to step 4). WBS scope is restored on the review-bar, review-focus and how-to lines that name work packages.

## Lint

/lint-artifact on cookbook/guidelines/planning/project-management/task-breakdown (guideline). The folder was compiled with cookr and `cookr validate` passed.

- PASS: FM-01 to FM-13 and FM-11a, GF-01 to GF-04, gf-triggers-field, gf-roled-parts, gf-build-bar (33 lines, one per rule), gf-named-rules.
- WARN: GF-RESEARCH. The research folder is present and every cited claim resolves. Three owner-list rules (task-has-assignee-and-priority, task-milestone-must-exist, blocked-task-references-blocker) cite their own `-prior` claim and raise `owner-decides` warnings.
- Summary: Pass 22 | Warn 1 | Fail 0. RESULT: CLEAN.

lint: clean

verdict: pass
