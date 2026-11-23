# testing/quality-assurance: area plan

The general quality-assurance practices a QA team runs against a deployed
product: writing end-to-end specs, triaging the failures they produce,
exploring a product under a charter, and choosing which tests a change
affects. myagenticteams-qa-team's four `testing/` specialities
(spec-authoring, failure-triage, exploratory-charter, commit-impact) are
grounded in this area by owner ruling (2026-11-21: "general QA research and
guidelines go into the cookbook, researched; what is specific to the team's
purpose (adh conventions, its paths, its output contracts) stays in the
team"). What stays in the team and out of every topic here: the adh `e2e/`
layout and its `@smoke` tag, the LoginCard selectors and `page.route` mocks
of adh sites, the hub path for exploratory reports, the JSON output
contracts, and the site registry. Every topic is new.

## Topics

| Topic | Path | Survivor | Copies | Specialities | Research type |
|---|---|---|---|---|---|
| e2e-test-authoring | `cookbook/guidelines/testing/quality-assurance/e2e-test-authoring` (new; input: myagenticteams-qa-team `specialities/testing/spec-authoring.md`, its general parts) | itself (new) | none | none | Technology / software (intent Do; domain browser end-to-end testing; method tool documentation and practitioner sources) |
| test-failure-triage | `cookbook/guidelines/testing/quality-assurance/test-failure-triage` (new; input: myagenticteams-qa-team `specialities/testing/failure-triage.md`) | itself (new) | none | none | Technology / software (intent Evaluate; domain test failure classification; method tool documentation, published industry studies and practitioner sources) |
| exploratory-testing-charters | `cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters` (new; input: myagenticteams-qa-team `specialities/testing/exploratory-charter.md`, its general parts) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain exploratory testing; method practitioner sources and published method guides) |
| test-impact-analysis | `cookbook/guidelines/testing/quality-assurance/test-impact-analysis` (new; input: myagenticteams-qa-team `specialities/testing/commit-impact.md`, its general parts) | itself (new) | none | none | Technology / software (intent Decide; domain change-based test selection; method tool documentation, published industry studies and practitioner sources) |

No topic has a copy, so nothing folds in this area. Each topic was added to
the worklist as `new: true`, `kind: "new"`, `devteam: "authored"`, in the
`testing/quality-assurance` batch.

The area is a sub-area of `testing/`, whose fifteen topics sit directly under
it. A sub-area keeps these four QA practices together and leaves the existing
topics where they are; the area path is an Owner question.

## Gaps

The area has no speciality: `run_gaps.py` reports `why_empty` "area has no
speciality", and `reference.json` is `[]`. No speciality text is measured, no
new topic claims a speciality, and the worklist's `building` list is empty, so
"Building specialities not yet measured" has nothing to list. The gaps of this
area are the **Missing subjects** below, judged by hand against the general
parts of myagenticteams-qa-team's four specialities.

No R9 measure is owed or possible: every topic is `kind: new` and the area has
no reference. Candidate survivors were chosen from a whole-cookbook search
(G87): `grep -ril` over `cookbook/` for selector, data-testid, getByRole,
playwright, exploratory, charter, test impact, impact analysis, test
selection, affected tests, triage, end-to-end and e2e, plus every topic of
`cookbook/guidelines/testing/`, `cookbook/guidelines/implementing/testing/`,
`cookbook/guidelines/planning/testing/` and `cookbook/guidelines/cookbook/testing/`.
The hits weighed: `testing/the-testing-workflow` (E2E verification, Playwright),
`implementing/testing/testing` (Playwright for TypeScript E2E),
`planning/testing/test-pyramid` (the E2E share), `testing/contract-testing`
(E2E as the costly alternative), `testing/flaky-test-quarantine` and
`testing/flaky-test-prevention` (flaky tests), `shipping/ephemeral-environments`
(E2E against preview environments), `implementing/ui/modern-css` and
`planning/code-quality/framework-conventions` (the word "selector", CSS only).
Nothing in the cookbook names exploratory testing, a charter, test impact
analysis or failure triage. The ones that touch a proposed topic are listed
under **Overlaps**.

## Missing subjects

1. **E2E selector strategy**: the qa-team's spec author picks stable selectors; no artifact says which locators an end-to-end spec uses (role, label, text, test id) and which it avoids (CSS paths, XPath, generated class names).
2. **Hermetic versus live E2E runs**: the qa-team writes specs that mock the network and specs that hit a live site; no artifact says when an end-to-end spec is hermetic, when it runs live, and how the two are kept apart.
3. **E2E determinism**: no artifact says how an end-to-end spec avoids timing flakes (auto-waiting assertions, no fixed sleeps, isolated state per test, controlled clocks and data).
4. **E2E secret handling**: the qa-team's specs never hold credentials; no artifact says how an end-to-end spec gets test accounts and secrets without committing them.
5. **Failure disposition taxonomy**: the qa-team gives each failed test a disposition (bug, flake, environment, spec rot, uncertain); no artifact names the dispositions a failure is triaged into or what evidence separates them.
6. **Failure triage evidence and confidence**: no artifact says what evidence a triage verdict cites (trace, screenshot, log, rerun history, recent changes) or how its confidence is stated.
7. **Charter structure**: the qa-team's explorer works from a charter; no artifact says what a charter holds (mission, target areas, resources, the information sought) or how one is written.
8. **Exploratory session time-boxing**: the qa-team caps an exploratory session's steps; no artifact says how a session is bounded in time or steps, or how session-based test management debriefs it.
9. **Exploratory anomaly reports**: the qa-team reports each anomaly with where it was seen, what was seen, what was expected and whether it repeats; no artifact says what an exploratory finding records.
10. **Fail-closed impact analysis**: the qa-team's impact analyst selects every target when it cannot tell what a change touches; no artifact says how test selection by change fails safe.
11. **Impact analysis evidence**: the qa-team cites the diff for each affected target; no artifact says what evidence a test-selection decision records so it can be checked.

## Overlaps

`copy_check.py` finds no copy to fold and no move in this area. The overlaps
below are existing topics whose rules touch part of a proposed topic, from the
whole-cookbook search (see **Gaps**). None holds the ground of a proposed
topic, so every topic stays `new`; each cites the artifact it touches rather
than restating it.

- **e2e-test-authoring** and `cookbook/guidelines/testing/the-testing-workflow`: "E2E verification SHOULD use Playwright for web UIs and platform test runners for native" (`should-verify-end-to-end`) and "E2E verification SHOULD cover critical user journeys" (`should-cover-critical-user-journeys-in-e2e`). The survivor rules that E2E runs and what it covers; e2e-test-authoring rules how a spec is written. Partial overlap: kept `new`, citing both rules and never restating them.
- **e2e-test-authoring** and `cookbook/guidelines/implementing/testing/testing`: "In TypeScript, you SHOULD use Playwright for end-to-end and visual regression testing" (`should-use-playwright-for-end-to-end-tests`). The tool choice; e2e-test-authoring cites it.
- **e2e-test-authoring** and `cookbook/guidelines/planning/testing/test-pyramid`: "Projects SHOULD follow the Google SWE Book ratio: 80% unit / 15% integration / 5% E2E". How many E2E tests, not how one is written; cited for scope.
- **e2e-test-authoring** and `cookbook/guidelines/testing/contract-testing` and `cookbook/guidelines/shipping/ephemeral-environments`: E2E as the costly alternative to contracts, and E2E against preview environments. Checked; cited where the hermetic-versus-live question touches them.
- **test-failure-triage** and `cookbook/guidelines/testing/flaky-test-quarantine`: "A test that needs a retry to pass MUST be treated as flaky" (`must-treat-retry-pass-as-flaky`) and the quarantine lifecycle. The survivor rules what happens to a test once it is known to be flaky; test-failure-triage rules how a failure is classified as a flake, a bug, an environment fault or spec rot in the first place. Partial overlap: kept `new`; a flake disposition hands the test to flaky-test-quarantine's lifecycle, cited and never restated.
- **test-failure-triage** and `cookbook/guidelines/testing/flaky-test-prevention`: "Flaky tests SHOULD be quarantined immediately, then fixed or deleted" (`should-quarantine-flaky-tests-immediately`). Cited with flaky-test-quarantine.
- **test-impact-analysis** and `cookbook/guidelines/testing/flaky-test-quarantine`: "the gating job's test selection excludes the quarantine tag" (`must-exclude-quarantined-tests-from-gate`). Selection by tag, not by change. Checked; no shared rule.
- **exploratory-testing-charters**: no artifact names exploratory testing or charters. No overlap.
- `cookbook/guidelines/implementing/ui/modern-css` and `cookbook/guidelines/planning/code-quality/framework-conventions` were checked: "selector" there means a CSS selector in styling. No overlap.

copy_check.py testing/quality-assurance: copies 0; identical 0; moved 0; unreadable 0; twin_differs 0; differ_uncarried none; result 8f6aaa512007

## Proposed topics

| Topic | Action | Artifact | Why |
|---|---|---|---|
| e2e-test-authoring | new | `cookbook/guidelines/testing/quality-assurance/e2e-test-authoring` | No artifact rules how an end-to-end spec is written (locators, determinism, hermetic or live, secrets); `the-testing-workflow` only requires that E2E runs. |
| test-failure-triage | new | `cookbook/guidelines/testing/quality-assurance/test-failure-triage` | No artifact rules how a failed test is classified; `flaky-test-quarantine` starts once a test is known to be flaky. |
| exploratory-testing-charters | new | `cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters` | No artifact names exploratory testing. |
| test-impact-analysis | new | `cookbook/guidelines/testing/quality-assurance/test-impact-analysis` | No artifact rules choosing tests by the change under test. |

## Research questions

Every topic cites the existing testing guidelines named under **Overlaps** and
never restates them. No topic holds an adh path, the qa-team's JSON output
contract, its `@smoke` tag or its site registry: those stay in
myagenticteams-qa-team (owner ruling, 2026-11-21).

### e2e-test-authoring (new)

1. Best practice: how should a browser end-to-end spec be written so it tests what a user does, stays stable as the UI changes and states the rationale for what it checks?
2. Known solutions: how do Playwright, Cypress, WebdriverIO and Selenium compare on locators, auto-waiting, network mocking, tracing and parallel runs, and what do page objects and fixtures add?
3. Platform guidelines: what do Playwright's best-practices and locator guides, Testing Library's query priority, the WAI-ARIA roles the locators rest on, and Apple's XCUITest and Android's Espresso guides say about writing stable UI tests?
4. The expert's view: what do test engineers say teams get wrong with end-to-end specs (CSS-path selectors, fixed sleeps, shared state between tests, specs that duplicate unit tests), and what to do instead?
5. **E2E selector strategy**: find the locator priority the tool owners and Testing Library publish, and state which locators a spec uses first, when a test id is warranted, and which it never uses.
6. **Hermetic versus live E2E runs**: find how teams split mocked-network specs from specs against a live or preview environment, and state when a spec is hermetic, when it runs live, and how each is tagged and gated.
7. **E2E determinism**: find the tool owners' guidance on waiting, retries, test isolation, clocks and test data, and state the rules that keep a spec free of timing flakes.
8. **E2E secret handling**: find how the tool owners and security guidance provide test accounts and secrets to specs (environment variables, secret stores, stored auth state), and state how a spec gets credentials without committing them.

### test-failure-triage (new)

1. Best practice: how should a failed automated test be triaged: who triages it, what is gathered first, and how the cause is classified before anyone fixes it?
2. Known solutions: how do the flake-detection and failure-classification systems published by Google, Meta, Microsoft and others, and the reporting features of Playwright, BuildPulse, Datadog CI Visibility and Trunk, classify a failure, and how do they compare?
3. Platform guidelines: what do the test-runner owners' guides (Playwright's trace viewer and retries, pytest's rerun and xfail markers, GitHub Actions' and other CI vendors' failure reports) say about diagnosing a failed test?
4. The expert's view: what do test engineers say teams get wrong when triaging failures (calling every failure a flake, rerunning until green, fixing the test when the product is broken), and what to do instead?
5. **Failure disposition taxonomy**: find the classes published studies and tools sort test failures into, and state the dispositions a failure is triaged into and what separates each from the others; each figure on failure-cause frequency takes the *Statistical* bar.
6. **Failure triage evidence and confidence**: find what evidence practitioners and tools gather for a verdict and how they express uncertainty, and state what a triage verdict cites and how its confidence is stated, including when the verdict is "uncertain".

### exploratory-testing-charters (new)

1. Best practice: how should exploratory testing be planned, run and reported so it finds what scripted tests miss and its results can be acted on?
2. Known solutions: how do session-based test management, charter templates (Elisabeth Hendrickson's "Explore ... with ... to discover ..."), test tours and heuristics such as SFDIPOT compare?
3. Platform guidelines: what do ISO/IEC/IEEE 29119 and the ISTQB syllabus say about exploratory and experience-based testing, and what do the method owners (James Bach, Jonathan Bach, Michael Bolton, Elisabeth Hendrickson) publish on charters and sessions?
4. The expert's view: what do exploratory testers say teams get wrong (exploring with no charter, no notes, reports that cannot be reproduced, treating it as ad hoc clicking), and what to do instead?
5. **Charter structure**: find the fields the method owners give a charter, and state what a charter holds and how one is written.
6. **Exploratory session time-boxing**: find how session-based test management bounds and debriefs a session, and state how a session is bounded (time or step cap) and what its debrief records.
7. **Exploratory anomaly reports**: find what the method owners and bug-report guidance require of a finding, and state the fields an exploratory finding records (where, what was seen, what was expected, whether it repeats).

### test-impact-analysis (new)

1. Best practice: how should a team choose which tests to run for a change so the run stays fast without missing a test the change breaks?
2. Known solutions: how do Bazel's and Nx's affected-target queries, Microsoft's Test Impact Analysis, Launchable, Meta's and Google's published predictive test selection, and coverage-based selection compare, and what does each miss?
3. Platform guidelines: what do the build and CI owners' guides (Bazel, Nx, Gradle, GitHub Actions path filters, Azure DevOps Test Impact Analysis) say about selecting tests by change and when to run everything?
4. The expert's view: what do build and test engineers say teams get wrong with test selection (trusting path filters alone, skipping tests on config or dependency changes, no periodic full run), and what to do instead?
5. **Fail-closed impact analysis**: find how selection tools behave when a change cannot be mapped to tests, and state the rule that a change of unknown reach selects every target; each figure on selection recall or saved time takes the *Statistical* bar.
6. **Impact analysis evidence**: find what selection tools record for each choice, and state what a test-selection decision cites (the changed files, the mapping that linked them to each target) so it can be checked.

## Owner questions

1. Research bar for every topic: no escalation is proposed. e2e-test-authoring and test-impact-analysis stay at the *Technology / software* bar, exploratory-testing-charters at the *How-to / troubleshooting* bar, and test-failure-triage at the *Technology / software* bar with intent *Evaluate*; each metric claim (failure-cause frequency, selection recall, time saved) takes the *Statistical* bar.
2. The area path: the four topics go under a new sub-area `cookbook/guidelines/testing/quality-assurance/`, while `testing/`'s fifteen existing topics sit directly under `testing/`. Approve the sub-area, or place the topics directly under `cookbook/guidelines/testing/` beside the existing ones (which makes the area `testing`, and every existing topic there part of this plan).
3. test-failure-triage and flaky-test-quarantine: the plan keeps triage `new` and hands a flake disposition to flaky-test-quarantine's lifecycle. Approve that split, or fold triage into flaky-test-quarantine as its first step.

## Step-4 re-check

### On 1.4.48

Short path: the area has no speciality (`why_empty` "area has no
speciality"), so re-run checklist items 4 to 6 are skipped and item 5 owes no
R9.

First check (`stage_status.py --first-check`, `A/first-check.txt`), run on the
saved reports after the plan was first written:

- unmeasured.py testing/quality-assurance: check unchanged; changes 0; new_keys 0; stale_reference 0; result a7c23a7e7fca
- run_gaps.py --check testing/quality-assurance: changed, exit 1; would_clear 0; failed 0; unplaced 0; stale_reference 0; r9_stale 0; verdict_changes 0; counted_rows 0; counted_rows_differ 0; changes 1; gap_total_rows 0; measured_total 0; missing_subjects 11; not_compared 0; counted_with_prior_verdict 0; counted_never_judged 0; stated 0 -> measured 0 (+0: counted_with_prior_verdict 0, counted_never_judged 0, verdict_changes 0); hints on (flag); report 6d4ff9414f2f9a562784a1e864d512fba290b1bc
- stage_status.py testing/quality-assurance: next approve; plan_sections 0; stale_reference 0; r9_stale 0; stale_copy_check 0; host_check 0; cite_moved 0; stale_verdicts 0; result 0785eeb62840

First check's `new_keys` 0, `changes` 1, `cleared` 0. The one change is this
plan's own: `missing_subjects` went from 0 to 11 (the **Missing subjects**
above). Step 1.3 was re-run (`run_gaps.py --hints`), which saved the report again.

Hand-off check, after the plan's final edit:

- unmeasured.py testing/quality-assurance: check unchanged; changes 0; new_keys 0; stale_reference 0; result a7c23a7e7fca
- run_gaps.py --check testing/quality-assurance: unchanged, exit 0; would_clear 0; failed 0; unplaced 0; stale_reference 0; r9_stale 0; verdict_changes 0; counted_rows 0; counted_rows_differ 0; changes 0; gap_total_rows 0; measured_total 0; missing_subjects 11; not_compared 0; counted_with_prior_verdict 0; counted_never_judged 0; stated 0 -> measured 0 (+0: counted_with_prior_verdict 0, counted_never_judged 0, verdict_changes 0); hints on (flag); report 35689372b5cde834adc561ca3cae106e1de0524c
- run_gaps.py --check-homes testing/quality-assurance: `check_homes` [], exit 0
- run_gaps.py --check-verdicts testing/quality-assurance: `check_verdicts` [], exit 0
- copy_check.py testing/quality-assurance: copies 0; identical 0; moved 0; unreadable 0; twin_differs 0; differ_uncarried none; result 8f6aaa512007
- stage_status.py testing/quality-assurance: next approve; plan_sections 0; stale_reference 0; r9_stale 0; stale_copy_check 0; host_check 0; cite_moved 0; stale_verdicts 0; result 0785eeb62840

This plan cites no other area plan, so no plan hash is recorded.
