# Review: dependency-tracking

## Findings

- `rationale.md`, first paragraph, the sentence added this round: "the count of days blocked rests on the practitioners alone, so it is an option, as recording a blocked task's dates is in task breakdown." The reason it gives for MAY ("rests on the practitioners alone") also fits `keep-resolved-dependency-blockers`. That rule cites only `leopold-red-blocker-sticker-days-blocked` too, whose `trust.basis` corroborates only the reason-with-flag part, yet it is SHOULD. Read with the rules, the rationale gives one reason for two different strengths. This is the only instance in the changed text. Fix: give the reason for each strength on its own terms. For example, say the day count is an option so that it matches `task-breakdown`'s `blocker-records-dates`, and that keeping resolved blockers is a recommendation because Leopold and Magennis say it emphatically ("DON'T THROW THE BLOCKER POST-ITS AWAY!"), which matches `task-breakdown`'s `keep-resolved-blockers`. Or drop "rests on the practitioners alone, so" as the reason.

## Checked

- `examples.md`: the identity-team row is now "External", which matches `map-internal-and-external-dependencies` and `internal-and-external-dependency-classes`.
- `rationale.md`, last paragraph: "no rule rests on them" now covers only the PMBOK Guide, ISO 21502 and ISO 31000. PRINCE2 is named as reached through APM's quotation and prince2.wiki, and as used by the internal-and-external and escalation rules.
- `rationale.md`, fourth paragraph: the halving model is now stated as direction only, with no figure, and the research's limit is put on the research, not on the model. This matches the `trust.basis` of `each-dependency-halves-on-time-chance`.
- Each of the seven bundled rules is split into one behaviour per rule. The prior name stays on one half, the new halves have fresh names (`dependency-confirmed-by-other-side`, `need-by-date-agreed-with-source`, `review-dependencies-at-regular-points`, `include-dependencies-in-status-reports`, `count-days-dependency-blocked`, `keep-resolved-dependency-blockers`, `at-risk-dependency-reviewed-against-milestones`), and each has its own citation. Each also has its own line in `a-build-must-establish.md` and sits in the right strength list in `a-complete-review-must-establish.md`. There are 25 rules in `rules.md`, and the reviewer and build lists account for all of them.
- Every new citation exists in research.json and is named by some verdict: `tracker-health-on-track-at-risk-off-track` (verdict `track-dependency-availability-and-status`) and `each-dependency-halves-on-time-chance` (verdict `reduce-dependencies-before-tracking`).
- Strength rule: `dependency-confirmed-by-other-side` and `reduce-dependencies-before-tracking` cite claims the second check refuted (`owner-agreed-and-confirmed-by-other-side`, `rescope-to-remove-dependencies`, `each-dependency-halves-on-time-chance`), and both are SHOULD, not MUST. `dependency-confirmed-by-other-side` says "the other side", not "providing", which avoids the direction the second check refuted.
- `need-by-date-agreed-with-source` ("resources included") follows the APM quote "(including resource)". `at-risk-dependency-reviewed-against-milestones` follows the Essex/APM quote "schedule implications to programme milestones".
- Blocker rules against `task-breakdown`: they are now scoped to a blocked dependency's record, and the Scope paragraph sends a team's own blocked tasks to task breakdown. The day count is MAY (matching `blocker-records-dates`) and keeping resolved blockers is SHOULD (matching `keep-resolved-blockers`). `analyse-resolved-blockers` now cites only `cluster-blockers-internal-external`, which supports it.
- `artifact.json`: `related` holds `risk-tracking` (a55182ef-…), `task-breakdown` (f264cc0b-…) and `milestone-scheduling` (023d4c91-…, which the Scope paragraph names). All three resolve in the index. `tags` now includes `dependency-tracking`. Removing `raid-log` breaks no rule.
- `examples.md` step 7: the added "Keep the note once the block is cleared" matches `keep-resolved-dependency-blockers`.
- The two owner-list rules keep their prior text word for word, behind the accepted lead-in.
- `cookr roles check` on the folder ran clean.

## Rulings

- R1.1: fixed — the example row now reads "External".
- R1.2: fixed — "no rule rests on them" is limited to PMBOK, ISO 21502 and ISO 31000, and PRINCE2's secondary sources and the rules that use them are named.
- R1.3: fixed — only the direction is stated, with no figure, and the limit is put on how the research uses the model.
- R1.4: fixed — all seven bundled rules are split into single behaviours, each with its own citation, build line and strength-list entry, and the prior names are kept.
- R1.5: fixed — the blocker rules are scoped to the dependency record, their strengths match `task-breakdown`, and the Scope paragraph points to task breakdown for blocked tasks.
- R1.6: fixed — `related` holds both sibling uuids (plus milestone-scheduling), and the `dependency-tracking` tag is added.

## Lint

lint-artifact v2.0.2 on `cookbook/guidelines/planning/project-management/dependency-tracking`, type guideline: FM-01 to FM-13, GF-01 to GF-04 and gf-triggers-field all PASS (19 pass, 0 warn, 0 fail). The cookbook-wide `cookr validate` passed. RESULT: CLEAN.

lint: clean

verdict: fail
