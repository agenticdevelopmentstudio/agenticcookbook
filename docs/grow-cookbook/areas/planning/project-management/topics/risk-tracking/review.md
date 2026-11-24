# Review: risk-tracking

## Findings

none

## Checked

- diff-3.md changes only two lines of `a-build-must-establish.md`. No other part changed this round.
- `risk-identification-and-attention-flagging` build line: "risk identification covered sources outside the team's control as well as those within it." This matches the rule ("whether or not their sources are under its control", claim `iso-identify-risks-whatever-their-source`) at its scope. It no longer requires external-source risks to exist.
- `agree-escalation-criteria` build line: "clear escalation criteria are agreed." This matches the rule ("agree clear criteria for when a risk is escalated") and its claims `orange-book-timely-escalation` and `nao-escalation-criteria-immediate-action`. It no longer asks for the criteria to be written down.
- The build bar still has 30 lines, which match the 30 rules in order (lint gf-build-bar).
- The two changed lines contain no other line of the over-asking class that R2.1 named.
- disputes.md covers only lint-FM-03 (the index entry). The current lint passes FM-03, so that dispute raises no finding.

## Rulings

- R2.1: fixed — both build lines now read as the finding's fixes, and each tests its rule at the strength and scope the rule states.

## Lint

/lint-artifact on `cookbook/guidelines/planning/project-management/risk-tracking` (cookr run as the prompt gives it, with the checkout's own cli and the grow-cookbook venv):

- PASS: FM-01 to FM-13 and FM-11a (links resolve, and `cookr validate` passed); GF-01, GF-02 and GF-03; gf-frontmatter-complete, gf-change-history, gf-triggers-field, gf-roled-parts, gf-named-rules (30 rules), gf-build-bar (30 lines in rule order), gf-research-folder (64 claims, 14 verdicts) and gf-rule-cites-research.
- WARN: GF-04 / gf-compliance-section. There is no `## Compliance` section. That section is a MAY, so this is not an error.
- Summary: Pass 27, Warn 1, Fail 0. RESULT: CLEAN.

lint: clean

verdict: pass
