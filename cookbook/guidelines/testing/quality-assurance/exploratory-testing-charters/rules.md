
### What exploration looks for

- **look-for-what-specs-cannot-anticipate**: An exploratory session SHOULD aim at what the specification and the scripted tests do not cover, such as hidden behaviours, interactions between features and untested areas, and SHOULD treat what documentation says about the product as unconfirmed until the product has been tried. (claims: iso-et-hunts-hidden-properties, et-explores-untested-areas, et-complements-formal-techniques, bolton-documentation-is-rumour, htsm-cover-what-matters)
- **exploration-designs-runs-and-learns-together**: Within a session the tester SHOULD design each next test from what the tests already run have shown about the product, rather than run a list of tests fixed before the session. (claims: iso-et-definition, et-explores-untested-areas, kaner-et-definition, et3-testing-definition)
- **use-product-element-heuristics-and-tours**: A tester MAY choose what a session covers with a coverage heuristic, such as the product elements structure, function, data, interfaces, platform, operations and time, or with a tour, such as the landmark tour that visits the features drawing users in a shuffled order. (claims: htsm-model-purpose, htsm-product-elements, bolton-time-added-to-product-elements, whittaker-landmark-tour, iso-experience-based-tours-attacks)

### Charters

- **charter-states-target-resources-and-information-sought**: A charter SHOULD state the target the session explores, the resources it brings to the target, and the information it seeks. (claims: charter-format-explore-with-to-discover, hendrickson-template-via-lyndsay, ast-charter-definition, sbtm-session-definition, ghazi-charter-checklists, ghazi-levels-of-exploration)
- **charter-names-scope-cap-focus-and-exclusions**: A charter SHOULD state the session's scope, its planned duration as the time the team is prepared to spend rather than an estimate or a step count, its focus areas in priority order with the features users rely on most ranked highest, and the areas the session leaves out of scope. (claims: charter-mission-scope-limitations, charter-is-unit-of-work, whittaker-landmark-concentrate, sbtm-session-sheet-sections)
- **charter-may-carry-optional-contents**: A charter MAY also carry exit criteria, test ideas or techniques, entry criteria, the test environment, and limitations stating what the product must never do. (claims: charter-optional-contents, charter-states-what-product-must-never-do, ghazi-charter-checklists)
- **charter-neither-too-narrow-nor-too-broad**: A charter SHOULD give the session a direction without specifying the individual tests or test actions to run, and SHOULD be focused enough that the tester can tell when its target has been explored. (claims: hendrickson-direction-without-overspecifying, hendrickson-too-specific, hendrickson-too-broad, charter-does-not-list-tests, charter-detail-trade-off)
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

