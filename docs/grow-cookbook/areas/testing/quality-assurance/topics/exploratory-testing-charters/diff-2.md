--- draft-1.md
+++ draft.md
@@ -10,7 +10,7 @@
 author: Mike Fullerton
 copyright: 2026 Mike Fullerton
 license: MIT
-summary: "Exploratory testing: charter each session, time-box and debrief it, and report each finding with its steps, oracle and repeatability, and what went untested."
+summary: "Exploratory testing: charter, time-box and debrief each session; report each finding with its expectation, steps and repeatability, and what went untested."
 platforms: []
 tags:
   - testing
@@ -54,7 +54,7 @@
 
 # Exploratory Testing Charters
 
-Give every exploratory session a charter that names the target it explores, the resources it brings and the information it seeks, with its scope, its time budget, its focus areas in priority order and what it leaves alone. Run the session as one time-boxed block, keep a session sheet with bugs, issues and notes apart, and debrief it. Report each finding from what was observed in the product, with where it was seen, the steps to reproduce it, the environment, why it is a problem, and how repeatable it was; and report what the session covered and left untested, also when it found nothing.
+Give every exploratory session a charter that names the target it explores, the resources it brings and the information it seeks, with its scope, its time budget, its focus areas in priority order and what it leaves alone. Run the session as one time-boxed block, keep a session sheet with bugs, issues and notes apart, and debrief it. Report each finding from what was observed in the product, with where it was seen (its URL or path), what was observed, what was expected instead, the steps to reproduce it, the environment, why it is a problem, and how repeatable it was; and report what the session covered and left untested, also when it found nothing.
 
 This guideline covers how any team plans, runs and reports exploratory testing: what a charter holds and how one is sized and chosen, how a session is bounded, recorded and debriefed under session-based test management, and what each finding records. Writing scripted end-to-end tests belongs to [adc.guideline.testing.quality-assurance.e2e-test-authoring](cookbook:eb82d5d7-4f42-4417-8104-a14f6a27899f); classifying a failed automated test belongs to [adc.guideline.testing.quality-assurance.test-failure-triage](cookbook:4825088c-7d3a-4ef3-8c1b-c5b70b88da0d); the conventions of the issue tracker a finding is filed in belong to [adc.guideline.planning.project-management.issue-tracking](cookbook:f77eeffe-2699-4028-9195-4bfc23c75e91). Following this guideline means keeping every MUST rule below, keeping each SHOULD rule or stating why a session departs from it, and using each MAY rule where it helps.
 
@@ -62,7 +62,8 @@
 
 ### What exploration looks for
 
-- **look-for-what-specs-cannot-anticipate**: An exploratory session SHOULD aim at what the specification and the scripted tests do not cover, such as hidden behaviours, interactions between features and untested areas, and SHOULD treat what documentation says about the product as unconfirmed until the product has been tried. (claims: iso-et-hunts-hidden-properties, et-explores-untested-areas, et-complements-formal-techniques, bolton-documentation-is-rumour, htsm-cover-what-matters)
+- **look-for-what-specs-cannot-anticipate**: An exploratory session SHOULD aim at what the specification and the scripted tests do not cover, such as hidden behaviours, interactions between features and untested areas. (claims: iso-et-hunts-hidden-properties, et-explores-untested-areas, et-complements-formal-techniques, htsm-cover-what-matters)
+- **treat-documentation-as-unconfirmed**: A tester SHOULD treat what documentation says about the product as unconfirmed until the product itself has been tried. (claim: bolton-documentation-is-rumour)
 - **exploration-designs-runs-and-learns-together**: Within a session the tester SHOULD design each next test from what the tests already run have shown about the product, rather than run a list of tests fixed before the session. (claims: iso-et-definition, et-explores-untested-areas, kaner-et-definition, et3-testing-definition)
 - **use-product-element-heuristics-and-tours**: A tester MAY choose what a session covers with a coverage heuristic, such as the product elements structure, function, data, interfaces, platform, operations and time, or with a tour, such as the landmark tour that visits the features drawing users in a shuffled order. (claims: htsm-model-purpose, htsm-product-elements, bolton-time-added-to-product-elements, whittaker-landmark-tour, iso-experience-based-tours-attacks)
 
@@ -71,7 +72,8 @@
 - **charter-states-target-resources-and-information-sought**: A charter SHOULD state the target the session explores, the resources it brings to the target, and the information it seeks. (claims: charter-format-explore-with-to-discover, hendrickson-template-via-lyndsay, ast-charter-definition, sbtm-session-definition, ghazi-charter-checklists, ghazi-levels-of-exploration)
 - **charter-names-scope-cap-focus-and-exclusions**: A charter SHOULD state the session's scope, its planned duration as the time the team is prepared to spend rather than an estimate or a step count, its focus areas in priority order with the features users rely on most ranked highest, and the areas the session leaves out of scope. (claims: charter-mission-scope-limitations, charter-is-unit-of-work, whittaker-landmark-concentrate, sbtm-session-sheet-sections)
 - **charter-may-carry-optional-contents**: A charter MAY also carry exit criteria, test ideas or techniques, entry criteria, the test environment, and limitations stating what the product must never do. (claims: charter-optional-contents, charter-states-what-product-must-never-do, ghazi-charter-checklists)
-- **charter-neither-too-narrow-nor-too-broad**: A charter SHOULD give the session a direction without specifying the individual tests or test actions to run, and SHOULD be focused enough that the tester can tell when its target has been explored. (claims: hendrickson-direction-without-overspecifying, hendrickson-too-specific, hendrickson-too-broad, charter-does-not-list-tests, charter-detail-trade-off)
+- **charter-gives-direction-not-tests**: A charter SHOULD give the session a direction without specifying the individual tests or test actions to run. (claims: hendrickson-direction-without-overspecifying, hendrickson-too-specific, charter-does-not-list-tests, charter-detail-trade-off)
+- **charter-target-is-finishable**: A charter SHOULD be focused enough that the tester can tell when its target has been explored. (claim: hendrickson-too-broad)
 - **split-large-areas-into-focused-charters**: An area too large for one charter SHOULD be covered by several charters, each focused on one area or one kind of problem. (claims: hendrickson-multiple-focused-charters, hendrickson-too-broad)
 - **charters-framed-with-stakeholders**: Charters SHOULD be framed with the stakeholders who will act on what the sessions find, aimed at the questions those stakeholders find most valuable. (claims: hendrickson-work-with-stakeholders, hendrickson-actionable-information)
 - **charter-set-kept-open**: A team SHOULD treat its set of charters as incomplete and add to it as sessions raise new questions. (claims: hendrickson-chartering-ongoing, lyndsay-charters-incomplete)
@@ -128,12 +130,12 @@
 2. Write each charter. Hendrickson's lightweight format, as the ISTQB Test Analyst syllabus gives it, is "Explore [target] With [resources] To discover [information]". Add the scope, the planned duration, the focus areas in priority order and what is out of scope. The syllabus lists further optional contents: exit criteria, test ideas and techniques, entry criteria, the test environment and limitations (what the product must never do). Stating what the system definitely cannot do lowers the chance of false-positive reports; naming the techniques to use can constrain the tester.
 3. Size it. A charter that lists the tests to run is a different way of writing scripted tests; one whose target is too big gives no way to tell when exploring is done. Split a big area into several charters, each on one area or one kind of problem.
 4. Choose the coverage. The product elements of the Heuristic Test Strategy Model (structure, function, data, interfaces, platform, operations, time) outline what a session can cover. Whittaker's landmark tour picks the landmark features in advance, shuffles them and tours from one to the next. ISO/IEC/IEEE 29119-1 names tours, attacks and error taxonomies as forms of experience-based testing.
-5. Set the time box. The duration is the time the team is prepared to spend, not a forecast. Session-based test management, as first published, used sessions of about ninety minutes, loosely timed; Lyndsay reports 10 to 120 minutes. Neither figure rests on a study.
-6. Run the session. Design each next test from what the last ones showed. When an area off the charter looks important, the time spent there is opportunity time; when an area merely tempts, it goes on the list as a later charter. If the session gets nowhere, abort it and run a different one.
+5. Set the time box and the step cap. The duration is the time the team is prepared to spend, not a forecast. Keep each pass within the hard cap of 25 browser steps. Session-based test management, as first published, used sessions of about ninety minutes, loosely timed; Lyndsay reports 10 to 120 minutes. Neither figure rests on a study.
+6. Run the session. Design each next test from what the last ones showed, and stay on the site's own origin. Keep findings inside the charter's ranked focus areas and respect its "leave alone" rules: an anomaly in an excluded area is reported as out-of-charter rather than raised as a finding. When an area off the charter looks important, the time spent there is opportunity time; when an area merely tempts, it goes on the list as a later charter. If the session gets nowhere, abort it and run a different one.
 7. Keep the session sheet as you go: the charter, then bugs, issues and notes in their own sections, with the steps followed and the discoveries made. A session tool can do some of this: Azure Test Plans' Test & Feedback extension files bugs from the session, keeps an action log of the steps that led to an issue, searches for existing bugs with a similar title as a new one is filed, and exports a session report.
-8. Write each finding: where it was seen, what was observed, what was expected (where that is not obvious) or why the behaviour is a problem, the steps and data, the test object and environment, and whether it was retried and how often it happened. One problem per finding. If a puzzling bug resists about ten minutes of investigation, check in with a developer.
+8. Write each finding: where it was seen, what was observed, what was expected instead, stated specifically rather than vacuously, and also why the behaviour is a problem where that is not obvious, the steps and data, the test object and environment, and whether it was retried and how often it happened. One problem per finding. If a puzzling bug resists about ten minutes of investigation, check in with a developer.
 9. Debrief. Session-based test management's PROOF checklist asks about the Past (what happened), Results (what was achieved), Obstacles (what got in the way), Outlook (what still needs to be done) and Feelings (how the tester feels about it). The debrief is also where a charter is narrowed or more sessions are added.
-10. Report the session, found problems or not: what was covered and how, what was not tested and why, and why the coverage was good enough.
+10. Report the session, found problems or not: what was covered and how, what was not tested and why, and why the coverage was good enough. A pass that found nothing says so plainly and reports the areas actually covered; it is neither padded with severity-free observations nor returned as a silent empty result.
 
 ## Examples
 
@@ -156,9 +158,10 @@
 A finding:
 
 ```text
-Where: checkout, order confirmation page
+Where: /checkout/confirmation
 Observed: after removing an item in a second tab and returning, the confirmation page showed
   the old total (3 items, 42.00); the receipt email showed the new total (2 items, 30.00).
+Expected: the confirmation page shows the current cart total, 2 items, 30.00.
 Oracle: the confirmation page and the receipt disagree for the same order.
 Steps: 1. add three items to the cart  2. open the cart in a second tab and remove one item
   3. return to the first tab and confirm the order
@@ -175,29 +178,31 @@
 Not tested: the confirmation page on mobile browsers (no device available this session).
 Good enough because: the order total, the highest-priority focus area, was checked on every
   path the charter names.
-Time: 50 minutes on charter, 10 on opportunity (an unexpected currency switch in settings).
-New charter noted: explore currency switching during checkout.
+Time: 50 minutes on charter, 10 on opportunity (the order-history page linked from the confirmation).
+New charter noted: explore the order-history page for orders whose cart changed mid-checkout.
 ```
 
 ## What a reviewer looks for
 
-Checks that each session has a charter stating its target, resources and information sought, with its scope, planned duration, ranked focus areas and what it leaves out, and that the charter gives direction without listing tests and is narrow enough to tell when it is done. Checks that charters were framed with the people who act on the results and that the set is kept open. Checks that each session was time-boxed, kept within any step cap and on the system's own origin, recorded on a sheet with bugs, issues and notes apart, debriefed, and that off-charter time was logged as opportunity while out-of-charter anomalies were handled as the charter rules require. Checks that each finding rests on observed behaviour, records where it was seen, what was observed and what was expected, gives steps to reproduce, the test object and environment, and the retries and frequency, reports one problem, says why it is a problem unless obvious, and carries no vacuous expected result. Checks that every session report, clean or not, states what was covered, how, what was not tested and why it was enough, and that a clean session says so plainly.
+Checks that each session has a charter stating its target, resources and information sought, with its scope, planned duration, ranked focus areas and what it leaves out, and that the charter gives direction without listing tests and is narrow enough to tell when it is done. Checks that the tester treated what documentation says as unconfirmed until the product was tried. Checks that charters were framed with the people who act on the results and that the set is kept open. Checks that each session was time-boxed, kept within 25 browser steps per pass and on the site's own origin, recorded on a sheet with bugs, issues and notes apart, debriefed, and that off-charter time was logged as opportunity while out-of-charter anomalies were handled as the charter rules require. Checks that each finding rests on observed behaviour, records where it was seen as a URL or path, what was observed and what was expected, gives steps to reproduce, the test object and environment, and the retries and frequency, reports one problem, says why it is a problem unless obvious, and carries no vacuous expected result. Checks that every session report, clean or not, states what was covered, how, what was not tested and why it was enough, and that a clean session says so plainly, is not padded with severity-free observations and is never returned as a silent empty result.
 
 ## A complete review must establish
 
 - Each MUST rule is kept, with no exception: `session-has-hard-step-cap`, `stay-on-charter-origin`, `findings-stay-inside-charter`, `anomaly-carries-all-four-parts`, `clean-pass-reports-coverage`.
-- Each SHOULD rule is kept or its departure is stated: `look-for-what-specs-cannot-anticipate`, `exploration-designs-runs-and-learns-together`, `charter-states-target-resources-and-information-sought`, `charter-names-scope-cap-focus-and-exclusions`, `charter-neither-too-narrow-nor-too-broad`, `split-large-areas-into-focused-charters`, `charters-framed-with-stakeholders`, `charter-set-kept-open`, `session-is-time-boxed`, `session-is-debriefed`, `session-sheet-keeps-bugs-issues-and-notes`, `off-charter-work-logged-as-opportunity`, `off-charter-ideas-become-new-charters`, `report-anomaly-where-what-expected-repeatable`, `finding-gives-steps-to-reproduce`, `finding-records-environment`, `repeatability-states-retry`, `occasional-finding-carries-more-information`, `one-problem-per-finding`, `finding-is-observed-not-inferred`, `finding-states-its-oracle`, `no-vacuous-expected-result`, `clean-session-reports-coverage-and-gaps`, `no-anomalies-said-plainly`.
+- Each SHOULD rule is kept or its departure is stated: `look-for-what-specs-cannot-anticipate`, `treat-documentation-as-unconfirmed`, `exploration-designs-runs-and-learns-together`, `charter-states-target-resources-and-information-sought`, `charter-names-scope-cap-focus-and-exclusions`, `charter-gives-direction-not-tests`, `charter-target-is-finishable`, `split-large-areas-into-focused-charters`, `charters-framed-with-stakeholders`, `charter-set-kept-open`, `session-is-time-boxed`, `session-is-debriefed`, `session-sheet-keeps-bugs-issues-and-notes`, `off-charter-work-logged-as-opportunity`, `off-charter-ideas-become-new-charters`, `report-anomaly-where-what-expected-repeatable`, `finding-gives-steps-to-reproduce`, `finding-records-environment`, `repeatability-states-retry`, `occasional-finding-carries-more-information`, `one-problem-per-finding`, `finding-is-observed-not-inferred`, `finding-states-its-oracle`, `no-vacuous-expected-result`, `clean-session-reports-coverage-and-gaps`, `no-anomalies-said-plainly`.
 - Each MAY rule is noted where it was used: `use-product-element-heuristics-and-tours`, `charter-may-carry-optional-contents`, `session-length-within-reported-range`, `abort-a-session-that-gets-nowhere`, `dispatch-sessions-as-todo-charters`, `session-sheet-records-steps-and-discoveries`, `record-sessions-with-a-session-tool`, `oracle-strength-may-be-stated`, `check-for-duplicate-before-filing`, `time-box-puzzling-bug-investigation`.
 
 ## A build must establish
 
-- `look-for-what-specs-cannot-anticipate`: the session targets what the specification and scripted tests do not cover, and checks documentation claims against the product.
+- `look-for-what-specs-cannot-anticipate`: the session targets what the specification and scripted tests do not cover.
+- `treat-documentation-as-unconfirmed`: each claim documentation makes about the product was checked against the product before it was relied on.
 - `exploration-designs-runs-and-learns-together`: tests were designed during the session from what earlier tests showed, not run from a fixed list.
 - `use-product-element-heuristics-and-tours`: where used, the heuristic or tour that chose the coverage is named.
 - `charter-states-target-resources-and-information-sought`: each charter states its target, resources and information sought.
 - `charter-names-scope-cap-focus-and-exclusions`: each charter states its scope, planned duration as a time budget, ranked focus areas and what is out of scope.
 - `charter-may-carry-optional-contents`: where used, each optional content (exit criteria, test ideas or techniques, entry criteria, environment, limitations) is stated in the charter.
-- `charter-neither-too-narrow-nor-too-broad`: no charter lists the individual tests to run, and each has a target the tester can finish exploring.
+- `charter-gives-direction-not-tests`: no charter lists the individual tests or test actions to run.
+- `charter-target-is-finishable`: each charter has a target focused enough that the tester can tell when it has been explored.
 - `split-large-areas-into-focused-charters`: each area too large for one charter is covered by several focused charters.
 - `charters-framed-with-stakeholders`: each charter traces to a question raised with the stakeholders who act on the results.
 - `charter-set-kept-open`: new questions raised by sessions were added to the set of charters.
@@ -247,7 +252,7 @@
 
 The reporting rules come from Bolton's two stories, one of the product and one of the testing, the testing story covering how the product was operated and observed, what was not tested and why the work was good enough, and from the Heuristic Test Strategy Model, whose result of testing is an assessment told as a story including bugs and curios.
 
-Most rules are recommendations because each rests on a single publisher's method, syllabus or guidance and the research bar for this topic is practitioner consensus: a team may depart from one where it states why, for example a session with no stakeholders to frame its charter. Five prior rules are kept as the owner's text, which the research could not support or found against: no source bounds a session by a step count, no testing source speaks to staying on one origin, the Rapid Software Testing guide makes the stated expectation conditional on the problem not being obvious, session-based test management encourages pursuing an important off-charter problem, and no source supports failing a clean session for keeping notes beside its result. The questions they raise are the owner's to settle.
+The research weighs this topic against a how-to bar of broad independent consensus and holds its recommendations at SHOULD. Many of them gather several independent publishers: the steps-to-reproduce rule draws on ISTQB, Mozilla, Apple, Android, the Rapid Software Testing guide and Microsoft, and the time-box rule on ISTQB, session-based test management and Lyndsay. They stay recommendations because the sources give them as reporting or method guidance, which a team may depart from where it states why, for example a session with no stakeholders to frame its charter. Some rest on one publisher alone: the opportunity-time and to-do-sheet rules on session-based test management, the sizing, splitting, stakeholder and new-charter rules on Hendrickson, the documentation rule on Bolton, and the vacuous-expectation rule on the Rapid Software Testing guide. Five prior rules are kept as the owner's text, which the research could not support or found against: no source bounds a session by a step count, no testing source speaks to staying on one origin, the Rapid Software Testing guide makes the stated expectation conditional on the problem not being obvious, session-based test management encourages pursuing an important off-charter problem, and no source supports failing a clean session for keeping notes beside its result. The questions they raise are the owner's to settle.
 
 ## References
 
