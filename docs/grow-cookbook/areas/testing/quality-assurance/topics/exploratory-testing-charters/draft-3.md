---
id: 979a89c0-0d26-4e8a-aae0-c4983ec5d675
title: Exploratory Testing Charters
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-24
modified: 2026-11-24
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Exploratory testing: charter, time-box and debrief each session; report each finding with its expectation, steps and repeatability, and what went untested."
platforms: []
tags:
  - testing
  - exploratory-testing
  - test-charters
  - session-based-testing
  - bug-reports
depends-on: []
related:
  - eb82d5d7-4f42-4417-8104-a14f6a27899f
  - 4825088c-7d3a-4ef3-8c1b-c5b70b88da0d
  - f77eeffe-2699-4028-9195-4bfc23c75e91
references:
  - https://cdn.standards.iteh.ai/samples/81291/2e08edad03eb48e882e398015d0120fa/ISO-IEC-IEEE-PRF-29119-1.pdf
  - https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
  - https://www.istqb.org/wp-content/uploads/sdm-uploads/ISTQB-CTAL-TA-Syllabus-v4.0-EN-4.pdf
  - https://www.ida.liu.se/~TDDD04/labs/2019/exploratory_testing/stqe-sbtm.pdf
  - https://www.workroom-productions.com/shaping-testing-with-charters/
  - https://whose.associationforsoftwaretesting.org/docs/communication/chartering/
  - https://arxiv.org/abs/1704.00988
  - https://arxiv.org/abs/1704.00537
  - http://kaner.com/pdfs/QAIExploring.pdf
  - https://www.developsense.com/resource/htsm.pdf
  - https://developsense.com/?p=1773
  - https://learn.microsoft.com/en-us/archive/blogs/james_whittaker/tour-of-the-month-the-landmark-tour
  - https://learn.microsoft.com/en-us/azure/devops/test/perform-exploratory-tests
  - https://learn.microsoft.com/en-us/azure/devops/test/connected-mode-exploratory-testing
  - https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  - https://developer.apple.com/bug-reporting/
  - https://source.android.com/docs/setup/contribute/report-bugs
  - https://developsense.com/?p=11835
  - https://www.satisfice.com/download/rapid-testing-guide-to-making-good-bug-reports
  - https://media.pragprog.com/titles/ehxta/charters.pdf
  - https://developsense.com/presentations/2011-05-STAREast-TestFraming.pdf
  - https://developsense.com/blog/2011/12/what-exploratory-testing-is-not-part-5-undocumented-testing
  - https://www.satisfice.com/blog/archives/1509
approved-by: ""
approved-date: ""
triggers: []
---

# Exploratory Testing Charters

Give every exploratory session a charter that names the target it explores, the resources it brings and the information it seeks, with its scope, its time budget, its focus areas in priority order and what it leaves alone. Run the session as one time-boxed block, keep a session sheet with bugs, issues and notes apart, and debrief it. Report each finding from what was observed in the product, with where it was seen (its URL or path), what was observed, what was expected instead, the steps to reproduce it, the environment, why it is a problem, and how repeatable it was; and report what the session covered and left untested, also when it found nothing.

This guideline covers how any team plans, runs and reports exploratory testing: what a charter holds and how one is sized and chosen, how a session is bounded, recorded and debriefed under session-based test management, and what each finding records. Writing scripted end-to-end tests belongs to [adc.guideline.testing.quality-assurance.e2e-test-authoring](cookbook:eb82d5d7-4f42-4417-8104-a14f6a27899f); classifying a failed automated test belongs to [adc.guideline.testing.quality-assurance.test-failure-triage](cookbook:4825088c-7d3a-4ef3-8c1b-c5b70b88da0d); the conventions of the issue tracker a finding is filed in belong to [adc.guideline.planning.project-management.issue-tracking](cookbook:f77eeffe-2699-4028-9195-4bfc23c75e91). Following this guideline means keeping every MUST rule below, keeping each SHOULD rule or stating why a session departs from it, and using each MAY rule where it helps.

## Rules

### What exploration looks for

- **look-for-what-specs-cannot-anticipate**: An exploratory session SHOULD aim at what the specification and the scripted tests do not cover, such as hidden behaviours, interactions between features and untested areas. (claims: iso-et-hunts-hidden-properties, et-explores-untested-areas, et-complements-formal-techniques, htsm-cover-what-matters)
- **treat-documentation-as-unconfirmed**: A tester SHOULD treat what documentation says about the product as unconfirmed until the product itself has been tried. (claim: bolton-documentation-is-rumour)
- **exploration-designs-runs-and-learns-together**: Within a session the tester SHOULD design each next test from what the tests already run have shown about the product, rather than run a list of tests fixed before the session. (claims: iso-et-definition, et-explores-untested-areas, kaner-et-definition, et3-testing-definition)
- **use-product-element-heuristics-and-tours**: A tester MAY choose what a session covers with a coverage heuristic, such as the product elements structure, function, data, interfaces, platform, operations and time, or with a tour, such as the landmark tour that visits the features drawing users in a shuffled order. (claims: htsm-model-purpose, htsm-product-elements, bolton-time-added-to-product-elements, whittaker-landmark-tour, iso-experience-based-tours-attacks)

### Charters

- **charter-states-target-resources-and-information-sought**: A charter SHOULD state the target the session explores, the resources it brings to the target, and the information it seeks. (claims: charter-format-explore-with-to-discover, hendrickson-template-via-lyndsay, ast-charter-definition, sbtm-session-definition, ghazi-charter-checklists, ghazi-levels-of-exploration)
- **charter-names-scope-cap-focus-and-exclusions**: A charter SHOULD state the session's scope, its planned duration as the time the team is prepared to spend rather than an estimate or a step count, its focus areas in priority order with the features users rely on most ranked highest, and the areas the session leaves out of scope. (claims: charter-mission-scope-limitations, charter-is-unit-of-work, whittaker-landmark-concentrate, sbtm-session-sheet-sections)
- **charter-may-carry-optional-contents**: A charter MAY also carry exit criteria, test ideas or techniques, entry criteria, the test environment, and limitations stating what the product must never do. (claims: charter-optional-contents, charter-states-what-product-must-never-do, ghazi-charter-checklists)
- **charter-gives-direction-not-tests**: A charter SHOULD give the session a direction without specifying the individual tests or test actions to run. (claims: hendrickson-direction-without-overspecifying, hendrickson-too-specific, charter-does-not-list-tests, charter-detail-trade-off)
- **charter-target-is-finishable**: A charter SHOULD be focused enough that the tester can tell when its target has been explored. (claim: hendrickson-too-broad)
- **split-large-areas-into-focused-charters**: An area too large for one charter SHOULD be covered by several charters, each focused on one area or one kind of problem. (claims: hendrickson-multiple-focused-charters, hendrickson-too-broad)
- **charters-framed-with-stakeholders**: Charters SHOULD be framed with the stakeholders who will act on what the sessions find, aimed at the questions those stakeholders find most valuable. (claims: hendrickson-work-with-stakeholders, hendrickson-actionable-information)
- **charter-set-kept-open**: A team SHOULD treat its set of charters as incomplete and add to it as sessions raise new questions. (claims: hendrickson-chartering-ongoing, lyndsay-charters-incomplete)

### Sessions

- **session-is-time-boxed**: A session SHOULD run as one uninterrupted block of chartered testing within a time box set before it starts. (claims: session-is-chartered-time-box, sbtm-session-definition, charter-is-unit-of-work)
- **session-length-within-reported-range**: A team MAY set a session's time box anywhere from about 10 to about 120 minutes, the range practitioners report. (claims: session-length-range, sbtm-session-length-ninety-minutes)
- **session-has-hard-step-cap**: This MUST hold: Hard cap: 25 browser steps per pass. (claim: session-has-hard-step-cap-prior)
- **stay-on-charter-origin**: This MUST hold: Stay on the site's own origin. (claim: stay-on-charter-origin-prior)
- **abort-a-session-that-gets-nowhere**: A tester who cannot make progress on a session's charter MAY abort the session and run a different one. (claim: sbtm-abort-or-rescope)
- **session-is-debriefed**: Each session SHOULD be followed by a short debrief between the tester and those who will use its results, covering what happened, what was achieved, what got in the way, what still needs doing, and how the tester feels about the work. (claims: session-is-chartered-time-box, sbtm-debrief-each-session, sbtm-proof-debrief, sbtm-dropping-debriefs-hurt, et3-accountability)
- **dispatch-sessions-as-todo-charters**: A team MAY dispatch a session as a to-do session sheet that carries its charter and leaves every other section for the tester to fill. (claim: sbtm-todo-session-sheets)

### Session records and off-charter work

- **session-sheet-keeps-bugs-issues-and-notes**: A session sheet SHOULD keep bugs (concerns about the product's quality), issues (questions or problems about the testing or the project) and notes (test ideas, risks, observations and anything else) in separate sections. (claims: sbtm-bugs-issues-notes, sbtm-session-sheet-sections, session-sheet-logs-questions-observations, bolton-risk-of-not-documenting)
- **session-sheet-records-steps-and-discoveries**: A session sheet MAY record the steps the tester followed and the discoveries made. (claim: session-sheet-records-steps)
- **record-sessions-with-a-session-tool**: A team MAY run sessions in a tool that files bugs from the session, records the actions that led to each, and exports a session report. (claims: azure-test-feedback-extension, azure-action-log-reproduce)
- **off-charter-work-logged-as-opportunity**: A session's record SHOULD report the time spent testing outside the charter as opportunity time, apart from the time spent on charter. (claim: sbtm-on-charter-vs-opportunity)
- **off-charter-ideas-become-new-charters**: An area that tempts the tester away from the charter SHOULD be noted as a charter for a later session. (claim: hendrickson-temptations-new-charters)
- **findings-stay-inside-charter**: This MUST hold: Findings stay inside the charter's ranked focus areas and respect its "leave alone" rules; an anomaly in an excluded area is reported as out-of-charter rather than raised as a finding. (claim: findings-stay-inside-charter-prior)

### What a finding records

- **report-anomaly-where-what-expected-repeatable**: Each finding SHOULD record where in the product it was seen, what was observed, what was expected instead, and how repeatable it was. (claims: defect-report-expected-and-actual, defect-report-identifies-object-and-environment, iso-incident-report-definition, mozilla-observed-and-expected, mozilla-reproducibility-at-will, apple-expected-results, bolton-peo-example, rst-seen-more-than-once, rst-frequency)
- **anomaly-carries-all-four-parts**: This MUST hold: Every reported anomaly carries all four parts: where (URL or path), what was seen, what was expected instead, and how repeatable it appeared. An anomaly missing the expectation is a fail — without it there is no claim of wrongness. (claim: anomaly-carries-all-four-parts-prior)
- **finding-gives-steps-to-reproduce**: A finding SHOULD give the steps that led to the problem, each described in enough detail for someone else to reproduce it, with any logs, screenshots or recordings captured. (claims: defect-report-enables-reproduction, defect-report-sufficient-information, mozilla-steps-most-important, apple-steps-to-reproduce, android-steps-to-reproduce, android-not-working-insufficient, rst-not-enough-to-reproduce, azure-action-log-reproduce)
- **finding-records-environment**: A finding SHOULD identify the test object and the environment it was tested in, such as the hardware, operating system and browser. (claims: defect-report-identifies-object-and-environment, rst-environment)
- **repeatability-states-retry**: A finding SHOULD state whether reproduction was tried and with what steps, and whether the problem reproduced at will, occasionally or not at all. (claims: rst-tried-to-reproduce, rst-seen-more-than-once, mozilla-reproducibility-at-will, rst-frequency)
- **occasional-finding-carries-more-information**: A finding that reproduces only occasionally SHOULD carry more information than its steps, such as the other times it was seen and how often it appeared. (claims: mozilla-occasional-needs-more-info, rst-seen-more-than-once, rst-frequency)
- **one-problem-per-finding**: Each finding SHOULD report one problem, with problems seen together reported as separate findings. (claims: apple-one-issue-per-report, rst-one-problem-per-report)

### How a finding is grounded

- **finding-is-observed-not-inferred**: A finding SHOULD rest on behaviour observed in the product itself, with what was observed kept apart from any inference or speculation about it, and SHOULD NOT rest on an opinion or a document's statement alone. (claims: rst-grounded-in-observation, mozilla-facts-vs-speculation, bolton-peo-example, rst-unsupported-opinion, bolton-documentation-is-rumour, et3-testing-definition)
- **finding-states-its-oracle**: A finding SHOULD say why the observed behaviour is a problem, naming its oracle, such as the specification, example, tool, preference or principle the product is inconsistent with, unless the problem is obvious. (claims: bolton-peo-problem, bolton-peo-oracle, rst-all-reports-based-on-oracle, rst-indicate-oracles-unless-obvious)
- **no-vacuous-expected-result**: A finding SHOULD NOT carry a vacuous or common-knowledge expected result, such as "the product should give the correct result" or "the product doesn't crash". (claims: rst-judicious-expected, rst-pedantic-reporting)
- **oracle-strength-may-be-stated**: A finding MAY say how strong its oracle is, from authoritative to merely suggestive of a problem. (claim: bolton-oracles-vary-strength)
- **check-for-duplicate-before-filing**: Before filing a finding as a bug, the tester MAY search the existing bugs for one with a similar title. (claim: azure-duplicate-search)
- **time-box-puzzling-bug-investigation**: A tester MAY investigate a puzzling bug for no more than about ten minutes before checking in with a developer about it. (claim: rst-ten-minute-heuristic)

### Reporting a session

- **clean-session-reports-coverage-and-gaps**: A session's report SHOULD state, whether or not it found problems, what was covered and how the product was configured, operated and observed, what was not tested, and why the testing done was good enough. (claims: bolton-story-of-untested, htsm-quality-story, htsm-cover-what-matters, sbtm-proof-debrief, bolton-two-stories)
- **no-anomalies-said-plainly**: A session that found no problem SHOULD say so explicitly in its report rather than return an empty result. (claims: bolton-story-of-untested, htsm-quality-story, sbtm-proof-debrief, bolton-two-stories)
- **clean-pass-reports-coverage**: This MUST hold: A pass that found nothing says so plainly and reports the areas actually covered. Padding a clean pass with severity-free observations is a fail, and so is a silent empty result. (claim: clean-pass-reports-coverage-prior)

## Running a chartered session

This section is informative: it shows one way to keep the rules, not a required method.

1. Frame the charters with the people who will act on the results. Ask which questions about the product matter most to them, and drop information nobody would act on. Keep the list of charters open: a set of charters is never complete, and new ones come out of every session.
2. Write each charter. Hendrickson's lightweight format, as the ISTQB Test Analyst syllabus gives it, is "Explore [target] With [resources] To discover [information]". Add the scope, the planned duration, the focus areas in priority order and what is out of scope. The syllabus lists further optional contents: exit criteria, test ideas and techniques, entry criteria, the test environment and limitations (what the product must never do). Stating what the system definitely cannot do lowers the chance of false-positive reports; naming the techniques to use can constrain the tester.
3. Size it. A charter that lists the tests to run is a different way of writing scripted tests; one whose target is too big gives no way to tell when exploring is done. Split a big area into several charters, each on one area or one kind of problem.
4. Choose the coverage. The product elements of the Heuristic Test Strategy Model (structure, function, data, interfaces, platform, operations, time) outline what a session can cover. Whittaker's landmark tour picks the landmark features in advance, shuffles them and tours from one to the next. ISO/IEC/IEEE 29119-1 names tours, attacks and error taxonomies as forms of experience-based testing.
5. Set the time box and the step cap. The duration is the time the team is prepared to spend, not a forecast. Keep each pass within the hard cap of 25 browser steps. Session-based test management, as first published, used sessions of about ninety minutes, loosely timed; Lyndsay reports 10 to 120 minutes. Neither figure rests on a study.
6. Run the session. Design each next test from what the last ones showed, and stay on the site's own origin. Keep findings inside the charter's ranked focus areas and respect its "leave alone" rules: an anomaly in an excluded area is reported as out-of-charter rather than raised as a finding. When an area off the charter looks important, the time spent there is opportunity time; when an area merely tempts, it goes on the list as a later charter. If the session gets nowhere, abort it and run a different one.
7. Keep the session sheet as you go: the charter, then bugs, issues and notes in their own sections, with the steps followed and the discoveries made. A session tool can do some of this: Azure Test Plans' Test & Feedback extension files bugs from the session, keeps an action log of the steps that led to an issue, searches for existing bugs with a similar title as a new one is filed, and exports a session report.
8. Write each finding: where it was seen, what was observed, what was expected instead, stated specifically rather than vacuously, and also why the behaviour is a problem where that is not obvious, the steps and data, the test object and environment, and whether it was retried and how often it happened. One problem per finding. If a puzzling bug resists about ten minutes of investigation, check in with a developer.
9. Debrief. Session-based test management's PROOF checklist asks about the Past (what happened), Results (what was achieved), Obstacles (what got in the way), Outlook (what still needs to be done) and Feelings (how the tester feels about it). The debrief is also where a charter is narrowed or more sessions are added.
10. Report the session, found problems or not: what was covered and how, what was not tested and why, and why the coverage was good enough. A pass that found nothing says so plainly and reports the areas actually covered; it is neither padded with severity-free observations nor returned as a silent empty result.

## Examples

This section is informative; the charter, finding and report below are illustrations, not a required format.

A charter:

```text
Explore the checkout flow
With saved payment methods, a slow network profile and a second browser tab
To discover how the order total and payment state hold up when the cart changes mid-checkout

Scope: cart review, payment entry and order confirmation
Duration: 60 minutes (the time budgeted, not an estimate)
Focus, in priority order: 1. order total  2. payment retries  3. confirmation page
Out of scope: account settings, promotional banners
Limitation: the product never charges a card twice for one order
```

A finding:

```text
Where: /checkout/confirmation
Observed: after removing an item in a second tab and returning, the confirmation page showed
  the old total (3 items, 42.00); the receipt email showed the new total (2 items, 30.00).
Expected: the confirmation page shows the current cart total, 2 items, 30.00.
Oracle: the confirmation page and the receipt disagree for the same order.
Steps: 1. add three items to the cart  2. open the cart in a second tab and remove one item
  3. return to the first tab and confirm the order
Environment: build 2.14.0, Firefox 133 on macOS 15
Repeatability: retried four times with the same steps; reproduced three times.
```

A session report with no problems found:

```text
Result: no problems found.
Covered: cart review and payment entry with saved cards and a slow network profile,
  operated in two browser tabs; observed the totals, the network log and the receipt emails.
Not tested: the confirmation page on mobile browsers (no device available this session).
Good enough because: the order total, the highest-priority focus area, was checked on every
  path the charter names.
Time: 50 minutes on charter, 10 on opportunity (the order-history page linked from the confirmation).
New charter noted: explore the order-history page for orders whose cart changed mid-checkout.
```

## What a reviewer looks for

Checks that each session has a charter stating its target, resources and information sought, with its scope, planned duration, ranked focus areas and what it leaves out, and that the charter gives direction without listing tests and is narrow enough to tell when it is done. Checks that the tester treated what documentation says as unconfirmed until the product was tried. Checks that charters were framed with the people who act on the results and that the set is kept open. Checks that each session was time-boxed, kept within 25 browser steps per pass and on the site's own origin, recorded on a sheet with bugs, issues and notes apart, debriefed, and that off-charter time was logged as opportunity while out-of-charter anomalies were handled as the charter rules require. Checks that each finding rests on observed behaviour, records where it was seen as a URL or path, what was observed and what was expected, gives steps to reproduce, the test object and environment, and the retries and frequency, reports one problem, says why it is a problem unless obvious, and carries no vacuous expected result. Checks that every session report, clean or not, states what was covered, how, what was not tested and why it was enough, and that a clean session says so plainly, is not padded with severity-free observations and is never returned as a silent empty result.

## A complete review must establish

- Each MUST rule is kept, with no exception: `session-has-hard-step-cap`, `stay-on-charter-origin`, `findings-stay-inside-charter`, `anomaly-carries-all-four-parts`, `clean-pass-reports-coverage`.
- Each SHOULD rule is kept or its departure is stated: `look-for-what-specs-cannot-anticipate`, `treat-documentation-as-unconfirmed`, `exploration-designs-runs-and-learns-together`, `charter-states-target-resources-and-information-sought`, `charter-names-scope-cap-focus-and-exclusions`, `charter-gives-direction-not-tests`, `charter-target-is-finishable`, `split-large-areas-into-focused-charters`, `charters-framed-with-stakeholders`, `charter-set-kept-open`, `session-is-time-boxed`, `session-is-debriefed`, `session-sheet-keeps-bugs-issues-and-notes`, `off-charter-work-logged-as-opportunity`, `off-charter-ideas-become-new-charters`, `report-anomaly-where-what-expected-repeatable`, `finding-gives-steps-to-reproduce`, `finding-records-environment`, `repeatability-states-retry`, `occasional-finding-carries-more-information`, `one-problem-per-finding`, `finding-is-observed-not-inferred`, `finding-states-its-oracle`, `no-vacuous-expected-result`, `clean-session-reports-coverage-and-gaps`, `no-anomalies-said-plainly`.
- Each MAY rule is noted where it was used: `use-product-element-heuristics-and-tours`, `charter-may-carry-optional-contents`, `session-length-within-reported-range`, `abort-a-session-that-gets-nowhere`, `dispatch-sessions-as-todo-charters`, `session-sheet-records-steps-and-discoveries`, `record-sessions-with-a-session-tool`, `oracle-strength-may-be-stated`, `check-for-duplicate-before-filing`, `time-box-puzzling-bug-investigation`.

## A build must establish

- `look-for-what-specs-cannot-anticipate`: the session targets what the specification and scripted tests do not cover.
- `treat-documentation-as-unconfirmed`: each claim documentation makes about the product was checked against the product before it was relied on.
- `exploration-designs-runs-and-learns-together`: tests were designed during the session from what earlier tests showed, not run from a fixed list.
- `use-product-element-heuristics-and-tours`: where used, the heuristic or tour that chose the coverage is named.
- `charter-states-target-resources-and-information-sought`: each charter states its target, resources and information sought.
- `charter-names-scope-cap-focus-and-exclusions`: each charter states its scope, planned duration as a time budget, ranked focus areas and what is out of scope.
- `charter-may-carry-optional-contents`: where used, each optional content (exit criteria, test ideas or techniques, entry criteria, environment, limitations) is stated in the charter.
- `charter-gives-direction-not-tests`: no charter lists the individual tests or test actions to run.
- `charter-target-is-finishable`: each charter has a target focused enough that the tester can tell when it has been explored.
- `split-large-areas-into-focused-charters`: each area too large for one charter is covered by several focused charters.
- `charters-framed-with-stakeholders`: each charter traces to a question raised with the stakeholders who act on the results.
- `charter-set-kept-open`: new questions raised by sessions were added to the set of charters.
- `session-is-time-boxed`: each session ran as one uninterrupted block within a time box set beforehand.
- `session-length-within-reported-range`: where used, each time box is between about 10 and about 120 minutes.
- `session-has-hard-step-cap`: no pass exceeds 25 browser steps.
- `stay-on-charter-origin`: no step leaves the site's own origin.
- `abort-a-session-that-gets-nowhere`: where used, each aborted session is recorded as aborted and replaced by a different session.
- `session-is-debriefed`: each session has a debrief covering past, results, obstacles, outlook and feelings.
- `dispatch-sessions-as-todo-charters`: where used, each to-do session sheet carries a charter and blank other sections.
- `session-sheet-keeps-bugs-issues-and-notes`: each session sheet keeps bugs, issues and notes in separate sections.
- `session-sheet-records-steps-and-discoveries`: where used, the session sheet lists the steps followed and the discoveries made.
- `record-sessions-with-a-session-tool`: where used, the tool's filed bugs, action logs and session report are kept with the session.
- `off-charter-work-logged-as-opportunity`: each session record splits its time into on charter and on opportunity.
- `off-charter-ideas-become-new-charters`: each tempting off-charter area is noted as a later charter.
- `findings-stay-inside-charter`: each anomaly in an excluded area is reported as out-of-charter, not raised as a finding.
- `report-anomaly-where-what-expected-repeatable`: each finding records where it was seen, what was observed, what was expected and how repeatable it was.
- `anomaly-carries-all-four-parts`: each reported anomaly carries where (URL or path), what was seen, what was expected and how repeatable it appeared.
- `finding-gives-steps-to-reproduce`: each finding gives steps detailed enough for someone else to reproduce it, with any logs, screenshots or recordings.
- `finding-records-environment`: each finding identifies the test object and its environment.
- `repeatability-states-retry`: each finding states whether and how reproduction was tried, and whether it reproduced at will, occasionally or not at all.
- `occasional-finding-carries-more-information`: each occasional finding carries information beyond its steps, such as other sightings and frequency.
- `one-problem-per-finding`: no finding reports more than one problem.
- `finding-is-observed-not-inferred`: each finding rests on observed behaviour, with inference and speculation kept apart and no finding resting on opinion or documentation alone.
- `finding-states-its-oracle`: each finding whose problem is not obvious names its oracle.
- `no-vacuous-expected-result`: no finding carries a vacuous or common-knowledge expected result.
- `oracle-strength-may-be-stated`: where used, each stated oracle strength is given beside its oracle.
- `check-for-duplicate-before-filing`: where used, the duplicate search was run before the bug was filed.
- `time-box-puzzling-bug-investigation`: where used, a puzzling bug was taken to a developer after about ten minutes.
- `clean-session-reports-coverage-and-gaps`: each session report states what was covered and how, what was not tested, and why that was good enough.
- `no-anomalies-said-plainly`: each session that found no problem says so explicitly.
- `clean-pass-reports-coverage`: each clean pass says so plainly and reports the areas covered, with no padding and no silent empty result.

## Rationale

This section is informative.

Exploratory testing is defined by ISO/IEC/IEEE 29119-1 and the ISTQB Foundation syllabus as testing in which tests are designed, run and evaluated together while the tester learns the product, and both place it beside the formal techniques, hunting for hidden properties those techniques miss. That is why a session aims at what the specification does not anticipate and designs its next test from its last one. Bolton's advice to treat what documentation says as rumour until the product has been engaged points the same way, and it also grounds each finding in the product rather than in a document.

The charter rules come from the ISTQB Test Analyst syllabus, which gives a charter the session's mission (scope, objectives, limitations, timelines, risks) and Hendrickson's "Explore, With, To discover" format, and lists the further contents a charter may hold, drawn from Ghazi et al.'s study. The syllabus introduces that list with "may contain but are not limited to", so those contents are options here. Lyndsay treats a charter's duration as a budget rather than an estimate; Whittaker's advice to concentrate testing on the landmark features that draw users supports ranking the focus areas. Hendrickson's warnings against charters too specific or too broad, her advice to split a big target, to frame charters with stakeholders and to treat chartering as ongoing, and Lyndsay's view that a set of charters is always incomplete give the sizing and framing rules. Lyndsay's relay of Hendrickson's template, Bach's session-sheet section list and the HTSM and Bolton product-element accounts were each found by the second check to support only part of their claims, so the rules citing them stop short of MUST.

Session-based test management, as Jonathan Bach first published it, defines a session as an uninterrupted block of reviewable, chartered effort, debriefs every session against the PROOF checklist, and keeps bugs, issues and notes apart on the session sheet; dropping debriefs led his team to poor session sheets and meaningless metrics. The ISTQB Foundation syllabus states the same time box, charter and debrief independently. No study backs any session length: ninety minutes is one team's practice and 10 to 120 minutes is one practitioner's range, so the length is a MAY. The abort rule rests on the standing order to abort a session that gets nowhere; the second check found its quote covers the abort only, so the rule stops there.

Session-based test management asks testers to log time on charter against time on opportunity and encourages them to divert to an off-charter problem that looks important; Hendrickson turns the temptation to wander into new charters. These give the opportunity-time and new-charter rules.

The finding rules follow the bug-report guidance of ISTQB (expected and actual results, the test object and environment, the steps that found the anomaly, enough information to resolve it), Mozilla (observed and expected result, reproducibility at will, occasionally or not at all, facts apart from speculation, steps as the most important part), Apple (detailed steps, one issue per report), Android (steps to reproduce; "it isn't working" needs more information), and the Rapid Software Testing guide and Bolton's Problem-Example-Oracle checklist (direct observation, the oracle, the environment, whether and how the problem was reproduced, one problem per report). The Rapid Software Testing guide also asks testers to be judicious about an "Expected:" line and names a common-knowledge expectation as pedantic reporting, which is why the oracle is stated unless the problem is obvious and a vacuous expected result is avoided. Its ten-minute heuristic and Azure Test Plans' duplicate search are a single heuristic and a single tool feature, so both are MAY.

The reporting rules come from Bolton's two stories, one of the product and one of the testing, the testing story covering how the product was operated and observed, what was not tested and why the work was good enough, and from the Heuristic Test Strategy Model, whose result of testing is an assessment told as a story including bugs and curios.

The research weighs this topic against a how-to bar of broad independent consensus and holds its recommendations at SHOULD. Many of them gather several independent publishers: the steps-to-reproduce rule draws on ISTQB, Mozilla, Apple, Android, the Rapid Software Testing guide and Microsoft, and the time-box rule on ISTQB, session-based test management and Lyndsay. They stay recommendations because the sources give them as reporting or method guidance, which a team may depart from where it states why, for example a session with no stakeholders to frame its charter. Some rest on one publisher alone: the opportunity-time and to-do-sheet rules on session-based test management, the finishable-target, splitting, stakeholder and new-charter rules on Hendrickson, the documentation rule on Bolton, and the vacuous-expectation rule on the Rapid Software Testing guide. Five prior rules are kept as the owner's text, which the research could not support or found against: no source bounds a session by a step count, no testing source speaks to staying on one origin, the Rapid Software Testing guide makes the stated expectation conditional on the problem not being obvious, session-based test management encourages pursuing an important off-charter problem, and no source supports failing a clean session for keeping notes beside its result. The questions they raise are the owner's to settle.

## References

This section is informative; every reference below is informative, and none is normative.

- ISO/IEC JTC 1/SC 7 and IEEE, *ISO/IEC/IEEE 29119-1:2021 Software testing, Part 1: General concepts* (public preview): https://cdn.standards.iteh.ai/samples/81291/2e08edad03eb48e882e398015d0120fa/ISO-IEC-IEEE-PRF-29119-1.pdf
- ISTQB, *Certified Tester Foundation Level Syllabus v4.0.1*: https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
- ISTQB, *Certified Tester Advanced Level Test Analyst Syllabus v4.0*: https://www.istqb.org/wp-content/uploads/sdm-uploads/ISTQB-CTAL-TA-Syllabus-v4.0-EN-4.pdf
- Jonathan Bach, *Session-Based Test Management*: https://www.ida.liu.se/~TDDD04/labs/2019/exploratory_testing/stqe-sbtm.pdf
- James Lyndsay, *Shaping Testing With Charters*: https://www.workroom-productions.com/shaping-testing-with-charters/
- Pete Walen and Justin Rohrman, Association for Software Testing, *Chartering*: https://whose.associationforsoftwaretesting.org/docs/communication/chartering/
- Ghazi, Garigapati and Petersen, *Checklists to Support Test Charter Design in Exploratory Testing*: https://arxiv.org/abs/1704.00988
- Ghazi, Petersen, Bjarnason and Runeson, *Exploratory Testing: One Size Doesn't Fit All*: https://arxiv.org/abs/1704.00537
- Cem Kaner, *A Tutorial in Exploratory Testing*: http://kaner.com/pdfs/QAIExploring.pdf
- James Bach, *Heuristic Test Strategy Model v6.0*: https://www.developsense.com/resource/htsm.pdf
- Michael Bolton, *How Models Change*: https://developsense.com/?p=1773
- James Whittaker, *Tour of the month: the landmark tour*: https://learn.microsoft.com/en-us/archive/blogs/james_whittaker/tour-of-the-month-the-landmark-tour
- Microsoft, *Install and use the Test & Feedback extension* and *Use the Test & Feedback extension in Connected mode*: https://learn.microsoft.com/en-us/azure/devops/test/perform-exploratory-tests, https://learn.microsoft.com/en-us/azure/devops/test/connected-mode-exploratory-testing
- Mozilla, *Bug Writing Guidelines*: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
- Apple, *Bug Reporting*: https://developer.apple.com/bug-reporting/
- Android Open Source Project, *Report bugs*: https://source.android.com/docs/setup/contribute/report-bugs
- Michael Bolton, *Problem, Example, Oracle: A Quick Checklist for Bug Reports*: https://developsense.com/?p=11835
- James Bach and Michael Bolton, *Rapid Software Testing Guide to Making Good Bug Reports*: https://www.satisfice.com/download/rapid-testing-guide-to-making-good-bug-reports
- Elisabeth Hendrickson, *Explore It!* (excerpt: Charters): https://media.pragprog.com/titles/ehxta/charters.pdf
- Michael Bolton, *Test Framing*: https://developsense.com/presentations/2011-05-STAREast-TestFraming.pdf
- Michael Bolton, *What Exploratory Testing Is Not (Part 5): Undocumented Testing*: https://developsense.com/blog/2011/12/what-exploratory-testing-is-not-part-5-undocumented-testing
- James Bach and Michael Bolton, *Exploratory Testing 3.0*: https://www.satisfice.com/blog/archives/1509

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-24 | Mike Fullerton | Initial creation, written from research |
