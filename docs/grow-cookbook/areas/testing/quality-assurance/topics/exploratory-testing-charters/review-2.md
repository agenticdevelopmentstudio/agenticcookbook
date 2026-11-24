# Review: exploratory-testing-charters

## Findings

- `rationale.md`, last paragraph (changed this round), the sentence "Some rest on one publisher alone: ... the sizing, splitting, stakeholder and new-charter rules on Hendrickson ...": the "sizing" rules are `charter-gives-direction-not-tests` and `charter-target-is-finishable` (how-to step 3, "Size it", covers both). `charter-gives-direction-not-tests` cites `charter-does-not-list-tests` and `charter-detail-trade-off`, both from the ISTQB Test Analyst syllabus, as well as Hendrickson, so it does not rest on Hendrickson alone. This is the same source-fidelity error R1.6 asked to remove. It is the only instance: the other single-publisher attributions in the sentence are accurate. `split-large-areas-into-focused-charters`, `charters-framed-with-stakeholders` and `off-charter-ideas-become-new-charters` cite only Hendrickson claims. `off-charter-work-logged-as-opportunity` and `dispatch-sessions-as-todo-charters` cite only SBTM. `treat-documentation-as-unconfirmed` cites only Bolton, and `no-vacuous-expected-result` only the RST guide. Fix: replace "the sizing" with "the finishable-target rule" (`charter-target-is-finishable`, which cites only `hendrickson-too-broad`), or drop the sizing rules from the list.

## Checked

- R1.1: the example finding now gives `Where: /checkout/confirmation` and an `Expected:` line. Step 8 lists "what was expected instead" unconditionally and gives "why the behaviour is a problem" as an addition. The intro lists the URL or path and what was expected.
- R1.2: the opportunity time is now spent on the order-history page, which the charter does not exclude and where no anomaly was found. The `New charter noted:` line matches.
- R1.3: the review focus now says "within 25 browser steps per pass and on the site's own origin". It checks that where is given as a URL or path, and that a clean pass is neither padded nor returned as a silent empty result.
- R1.4: step 5 adds the 25-step cap. Step 6 adds the own-origin limit and the out-of-charter handling, in the MUST rule's own words. Step 10 adds no padding and no empty result, also in the rule's own words. No owner open question is settled.
- R1.5: `look-for-what-specs-cannot-anticipate` keeps its prior name and first clause. `treat-documentation-as-unconfirmed` (SHOULD) cites `bolton-documentation-is-rumour`. `charter-gives-direction-not-tests` and `charter-target-is-finishable` replace the bundled rule, and each has a build-bar line, a review-bar entry and existing claims.
- R1.6: the single-publisher justification is gone. The new text gives the research's how-to bar (LOW-MEDIUM, broad independent consensus, per research.json methodology) and the reporting/method-guidance reason, and names multi-publisher examples correctly (steps-to-reproduce, time-box).
- Summary is 155 characters and describes the new text. Tags, platforms and related are unchanged and still fit.
- The five owner-list rules keep their prior text with the "This MUST hold:" lead-in.
- `cookr roles check` passes.

## Rulings

- R1.1: fixed — the example finding has a path and an Expected line, step 8 makes the expectation unconditional, and the intro lists what was expected.
- R1.2: fixed — the opportunity time is now on a non-excluded area with no anomaly, and the new-charter line matches.
- R1.3: fixed — the step cap and the own-origin rule are stated as the MUST rules word them, and the clean-pass and URL-or-path checks are added.
- R1.4: fixed — steps 5, 6 and 10 now carry the four missing MUST rules without settling an open question.
- R1.5: fixed — both bundled rules are split into separate SHOULD rules with their own citations, build-bar lines and review-bar entries.
- R1.6: fixed — the false single-publisher justification is replaced by the research's bar and reason. The sizing attribution in the new sentence is raised above as a new finding.

## Lint

/lint-artifact on cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters (guideline), compiled with this checkout's cookr; `cookr validate` passed.
Pass: 27 | Warn: 1 | Fail: 0. The WARN is GF-04 (no ## Compliance section, which is optional). All FM-*, GF-01..03 and gf-* checks pass: 41 named rules, each citing existing claims, and the build bar has one line per rule.
RESULT: CLEAN.
lint: clean

verdict: fail
