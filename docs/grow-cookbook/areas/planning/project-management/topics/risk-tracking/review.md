# Review: risk-tracking

## Findings

- `a-build-must-establish.md`, build lines that ask for more than their rule (behavioral-requirements, source-fidelity: a build check must test the rule at the strength and scope it states, no more). Two lines changed this round have this problem:
  - `risk-identification-and-attention-flagging`: "the register includes risks whose sources lie outside the team's control." The rule, like `iso-identify-risks-whatever-their-source` ("should identify risks, whether or not their sources are under its control"), asks that identification not stop at what the team controls. It does not say such risks must exist. A project with no external-source risks keeps the rule but fails this line. Fix: "risk identification covered sources outside the team's control as well as those within it."
  - `agree-escalation-criteria`: "escalation criteria are agreed and written down." The rule and its claims (`orange-book-timely-escalation` "based on agreed criteria"; `nao-escalation-criteria-immediate-action` "clear criteria for escalating risks") ask for agreed, clear criteria. Neither the rule nor its claims says the criteria are written down. Fix: "clear escalation criteria are agreed."

## Checked

- R1.1 split: all nine bundled rules are split into one behaviour each. The prior names stay on one half each: `risk-identification-and-attention-flagging`, `distinguish-immediate-action-from-monitoring`, `link-concerns-to-related-elements`, `concern-has-status-and-raiser`, `risk-review-cadence`, `risk-response-triage`, `escalate-risks-beyond-tolerance` and `describe-risk-as-cause-event-effect`. `owner-most-capable-and-not-overloaded` became `owner-most-capable-of-managing` plus `no-owner-holds-too-many-risks`. That renames the prior rule, but `owner-most-capable-and-not-overloaded` names no verdict, so its name is not fixed. Every new rule cites only the claims behind its own half.
- Every new rule has its own build-bar line (30 rules, 30 lines). Each of the 26 SHOULD rules appears in the SHOULD list of `a-complete-review-must-establish.md`, and each of the 4 MAY rules appears in the MAY list.
- R1.2: the rules are grouped under six `###` subsections with 7, 5, 4, 5, 6 and 3 rules: Recording a risk, Status and history, Ownership, Review, Response and escalation, Tooling.
- R1.3: `risk-becomes-issue-when-it-happens` now reads "SHOULD be closed in the risk register and raised as an issue" and cites `prince2-risk-status-field`. It agrees with `risk-has-active-or-closed-status`, `keep-risk-status-history`, how-to step 7 and the build line. No refuted claim carries MUST.
- R1.4: `flag-project-at-risk` ends at the health indicator, and its build line reads "where used, a threatened project carries a health indicator". Nothing in the text now rules on the tracker-mapping open question.
- R1.5: `related` holds `f77eeffe-2699-4028-9195-4bfc23c75e91` (issue-tracking) and `3f978ba7-c8c1-4b53-8fda-12e5a6966b75` (dependency-tracking). Both resolve in `cookbook/index.json`. The intro links both siblings as `[rdid](cookbook:uuid)` and leaves `project-record-linking` as a topic mention.
- Source fidelity of the new and changed rules:
  - `surface-new-risks-continually` follows from `scrum-daily-identifies-impediments` and `pmbok8-monitoring-never-stops` ("hunt for new ones").
  - `owner-most-capable-of-managing` and `no-owner-holds-too-many-risks` rest on the part of `prince2-owner-and-actionee-agreed` that the second check found the quote supports.
  - `agree-escalation-criteria`, `keep-register-up-to-date`, `check-register-at-each-review`, `record-risk-proximity`, `weigh-response-cost-against-benefit`, `no-duplicate-risk-entries`, `risk-uniquely-identified` and `keep-risk-status-history` each match their cited claim.
  - Every rule is at SHOULD or MAY.
- Every cited claim exists in research.json, and every cited claim is named by some verdict.
- Frontmatter: the new `summary` is 153 characters and describes the new text, including closing a risk into an issue. `tags` and `platforms` still fit.
- The changed how-to steps 2 to 5 and the example's new `Status history` line agree with the split rules: identifier, owner load, cost against benefit, escalation criteria and kept status history.
- The changed rationale sentence: proximity and status history rest on PRINCE2 claims alone, and `prince2-proximity-field`'s trust basis confirms that no second source names proximity.
- The changed what-a-reviewer-looks-for paragraph covers every rule after the split.
- Owner's open questions: no changed text settles one. Dropping "who may or may not be the risk's owner" from `risk-response-has-an-actionee` leaves the open question on a separate actionee open.
- `cookr roles check`: ok, 30 rules, no findings.
- disputes.md (lint FM-03, index entry): moot, because the index now holds the entry and FM-03 passes.

## Rulings

- R1.1: fixed — each of the nine bundled rules is split into single-behaviour rules, each with its own citation, its own build line and its own review-bar entry.
- R1.2: fixed — the rules sit under six `###` subsections, none with more than seven rules.
- R1.3: fixed — the rule now closes the risk in the register and raises an issue, cites `prince2-risk-status-field`, and agrees with the status rules, step 7 and the build line.
- R1.4: fixed — the per-risk clause is gone from both the rule and the build line, and the rule ends at the indicator.
- R1.5: fixed — both sibling UUIDs are in `related`, and the intro links issue tracking and dependency tracking by `cookbook:` UUID.

## Lint

lint-artifact v2.0.1 on `cookbook/guidelines/planning/project-management/risk-tracking` (guideline), compliance `tbd/compliance/artifact-formatting/guideline-formatting.md`:

```
[PASS] FM-01: YAML frontmatter block present
[PASS] FM-02: id is a valid UUID (a55182ef-...)
[PASS] FM-03: index.json entry matches folder (rdid adc.guideline.planning.project-management.risk-tracking), no domain field
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.0 is valid semver
[PASS] FM-06: all required fields present (approved-by/approved-date are blank, not checked)
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright "2026 Mike Fullerton"
[PASS] FM-09: created/modified are ISO dates
[PASS] FM-10: summary is non-empty
[PASS] FM-11: H1 "Risk Tracking" matches title
[PASS] FM-11a: links resolve (related are UUIDs; in-text cookbook:<uuid> links validate; cookr validate passes)
[PASS] FM-12: Change History section present with a row
[PASS] FM-13: no TODO/TBD/FIXME/placeholder text
[PASS] GF-01: summary statement follows H1
[PASS] GF-02: structured guidance (bullets and subsections)
[PASS] GF-03: RFC 2119 keywords in every rule
[PASS] GF-04: Compliance section is optional and not required; no check references it
[PASS] gf-frontmatter-complete
[PASS] gf-roled-parts: parts have roles; rules, review-focus, review-bar and build-bar are present; the build-bar has exactly one line per rule (30 rules, 30 lines)
[PASS] gf-named-rules: 30 unique kebab-case names, each with MUST, SHOULD or MAY
[PASS] gf-research-folder: research.json and research.md present, with the four headings in order; every cited claim has a verdict
[PASS] gf-rule-cites-research: every rule ends with one citation and every cited id is a claim in research.json
[PASS] gf-triggers-field: `triggers: []` is present (acceptable)

=== LINT SUMMARY ===
Artifact: risk-tracking
Type: guideline
Pass: 23 | Warn: 0 | Fail: 0
RESULT: CLEAN
```

lint: clean

verdict: fail
