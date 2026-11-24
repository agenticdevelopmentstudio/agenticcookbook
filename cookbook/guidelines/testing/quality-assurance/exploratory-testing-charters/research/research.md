# exploratory-testing-charters: research

This record covers three things: how exploratory testing is chartered, how a session is bounded and debriefed, and what each finding records. The standards and certification bodies come first: ISO/IEC/IEEE 29119-1 and the ISTQB Foundation and Test Analyst syllabi. The method owners come next: session-based test management, the Heuristic Test Strategy Model and Hendrickson's *Explore It!*. Then come the platform owners' bug-reporting guidance (Apple, Android, Microsoft, and Mozilla for the web), and last the practitioners of Rapid Software Testing and others. Every finding names the claim in `research.json` it rests on. Of the prior rules, seven hold, three are unsupported and two are contradicted. The research adds fifteen new rules.

## Best practices

- Exploratory testing designs, runs and evaluates tests together while the tester learns the product. ISO 29119-1 and ISTQB define it that way (`iso-et-definition`, `et-explores-untested-areas`). It hunts for hidden properties that formal techniques miss and complements them rather than replacing them (`iso-et-hunts-hidden-properties`, `et-complements-formal-techniques`). **look-for-what-specs-cannot-anticipate** therefore holds at SHOULD, and **exploration-designs-runs-and-learns-together** is new at SHOULD.
- A session runs within a defined time box, is guided by a charter of test objectives, and is usually followed by a debriefing (`session-is-chartered-time-box`). This supports **session-is-time-boxed** (new, SHOULD) and **session-is-debriefed** (new, SHOULD).
- A charter gives the session its mission: its scope, objectives, limitations, timelines and risks (`charter-mission-scope-limitations`). Its permitted contents are:
  - duration
  - areas of interest
  - priorities
  - exit criteria
  - what will not be tested
  - what the product must never do

  The sources for these are `charter-optional-contents` and `charter-states-what-product-must-never-do`. **charter-names-scope-cap-focus-and-exclusions** therefore holds at SHOULD for scope, ranked focus and exclusions. Its "cap" holds only as a planned duration, never as a step count.
- The lightweight charter format is "Explore [target] With [resources] To discover [information]" (`charter-format-explore-with-to-discover`). This supports **charter-states-target-resources-and-information-sought** (new, SHOULD).
- A charter does not list the tests to run (`charter-does-not-list-tests`). Bare objectives leave room to explore, while stating what the system cannot do cuts false positives (`charter-detail-trade-off`).
- A session sheet records the steps followed, the discoveries made, and the questions, observations and ideas for later testing (`session-sheet-records-steps`, `session-sheet-logs-questions-observations`).
- A defect report, called an incident or anomaly report in ISO's terms (`iso-incident-report-definition`), typically carries the following:
  - the test object and environment (`defect-report-identifies-object-and-environment`)
  - expected and actual results (`defect-report-expected-and-actual`)
  - the steps that found it, with logs or screenshots (`defect-report-enables-reproduction`)
  - enough information to resolve it (`defect-report-sufficient-information`)

  **report-anomaly-where-what-expected-repeatable** therefore holds at SHOULD.
- Session limits:
  - **session-has-hard-step-cap** is unsupported (`session-has-hard-step-cap-prior`). Every source bounds a session by time, and no source gives a step count.
  - **stay-on-charter-origin** is unsupported (`stay-on-charter-origin-prior`). No testing source speaks to origin restrictions, so the rule would rest on an owner's policy decision.
- Prior rules on findings:
  - **anomaly-carries-all-four-parts** is contradicted as a hard fail (`anomaly-carries-all-four-parts-prior`). See the expert's view.
  - **findings-stay-inside-charter** is contradicted (`findings-stay-inside-charter-prior`). See Known solutions.
  - **clean-pass-reports-coverage** is unsupported as written (`clean-pass-reports-coverage-prior`).

## Known solutions

- **Session-based test management** is the reference method:
  - A session is an uninterrupted block of reviewable, chartered effort tied to a mission (`sbtm-session-definition`).
  - Sessions last about ninety minutes, loosely timed (`sbtm-session-length-ninety-minutes`). This is one team's practice, not a measured optimum.
  - Every session is debriefed against the PROOF checklist: past, results, obstacles, outlook, feelings (`sbtm-debrief-each-session`, `sbtm-proof-debrief`).
  - The session sheet carries the charter and keeps bugs, issues and notes apart (`sbtm-session-sheet-sections`, `sbtm-bugs-issues-notes`). This supports **session-sheet-keeps-bugs-issues-and-notes** (new, SHOULD).
  - A tester who gets nowhere aborts the session, and the debrief narrows or splits the charter (`sbtm-abort-or-rescope`).
  - Testers are dispatched with to-do sheets that carry only a charter (`sbtm-todo-session-sheets`).
- **Off-charter work.** Session-based test management asks testers to report time on charter against time on opportunity. It encourages them to divert to an off-charter problem that looks important (`sbtm-on-charter-vs-opportunity`). Hendrickson adds that the temptation to wander should become new charters (`hendrickson-temptations-new-charters`). This contradicts **findings-stay-inside-charter**'s "out-of-charter rather than raised" and supports **off-charter-work-logged-as-opportunity** (new, SHOULD).
- **Charter templates and definitions:**
  - Lyndsay relays Hendrickson's target / resources / information template (`hendrickson-template-via-lyndsay`).
  - The Association for Software Testing defines a charter as what to test, how, and what problems to look for (`ast-charter-definition`).
  - Ghazi et al. derive charter checklists of factors and content elements from interviews (`ghazi-charter-checklists`). They also propose levels of exploration that can guide charter structure (`ghazi-levels-of-exploration`).
  - Lyndsay treats a charter's duration as a budget of time, not an estimate (`charter-is-unit-of-work`). Sessions typically run 10 to 120 minutes (`session-length-range`).
- **Coverage heuristics.** The Heuristic Test Strategy Model reminds testers what to think about (`htsm-model-purpose`). Its product elements are structure, function, data, interfaces, platform, operations and time, used to outline coverage (`htsm-product-elements`, `bolton-time-added-to-product-elements`).
- **Tours.** Whittaker's landmark tour visits the features that draw users, in shuffled order, and concentrates testing there (`whittaker-landmark-tour`, `whittaker-landmark-concentrate`). ISO names tours and attacks as forms of experience-based testing (`iso-experience-based-tours-attacks`). Together these support **use-product-element-heuristics-and-tours** (new, MAY).
- Kaner, who coined the term, defines exploratory testing as a style built on the tester's freedom and responsibility (`kaner-et-definition`).

## Platform guidelines

Apple, Android and Windows have little bearing on the topic beyond their bug-report guidance.

- **Web (Mozilla):**
  - Give the observed and the expected result after the steps (`mozilla-observed-and-expected`).
  - Say whether the bug reproduces at will, occasionally, or not at all (`mozilla-reproducibility-at-will`). An occasional bug must come with more information (`mozilla-occasional-needs-more-info`).
  - Keep facts apart from speculation (`mozilla-facts-vs-speculation`).
  - Steps to reproduce are the most important part (`mozilla-steps-most-important`).
- **Apple:**
  - Give detailed steps to reproduce (`apple-steps-to-reproduce`).
  - Its example report shows an expected-results line (`apple-expected-results`).
  - File one issue per report (`apple-one-issue-per-report`).
- **Android:**
  - Include the steps to reproduce (`android-steps-to-reproduce`).
  - A report that only says something isn't working will need more information (`android-not-working-insufficient`).
- **Windows / Microsoft:** Azure Test Plans' Test & Feedback extension runs exploratory sessions. It files bugs, captures screenshots and recordings, and exports a session report (`azure-test-feedback-extension`). It records an action log for reproducing an issue (`azure-action-log-reproduce`) and searches for duplicate bugs by title (`azure-duplicate-search`). These support **finding-gives-steps-to-reproduce** (new, SHOULD), **one-problem-per-finding** (new, SHOULD) and **check-for-duplicate-before-filing** (new, MAY).

## The expert's view

- **Ground every finding in the product.**
  - A bug ought to rest on direct observation of the product, with its steps and data (`rst-grounded-in-observation`).
  - An unsupported opinion is no basis for a report (`rst-unsupported-opinion`).
  - Documentation is rumour until the product has been engaged (`bolton-documentation-is-rumour`).
  - The Example part of Bolton's checklist asks for what was observed (`bolton-peo-example`).
  - Inference still guides testing (`et3-testing-definition`); observation is what grounds the report.

  **finding-is-observed-not-inferred** therefore holds.
- **State the oracle; don't recite the obvious.**
  - Every report rests on an oracle (`rst-all-reports-based-on-oracle`, `bolton-peo-oracle`), starting from the problem perceived (`bolton-peo-problem`).
  - Say why it is a bug "unless it is obvious" (`rst-indicate-oracles-unless-obvious`).
  - Be judicious about "expected:", and never write a vacuous one (`rst-judicious-expected`). "Expected: product doesn't crash" is named as pedantic reporting (`rst-pedantic-reporting`).
  - Oracles vary in strength (`bolton-oracles-vary-strength`).

  This contradicts **anomaly-carries-all-four-parts**, which fails any anomaly missing its expectation. It supports **finding-states-its-oracle** (new, SHOULD) instead.
- **Say what was retried.**
  - Ask whether the problem has been seen more than once (`rst-seen-more-than-once`), how often, and how easy it is to make happen (`rst-frequency`).
  - Ask whether reproduction was tried, and with what steps (`rst-tried-to-reproduce`).

  **repeatability-states-retry** holds.
- **Avoid these common mistakes:**
  - not enough information to reproduce (`rst-not-enough-to-reproduce`)
  - several problems in one report (`rst-one-problem-per-report`)
  - a missing environment (`rst-environment`), which supports **finding-records-environment** (new, SHOULD)
  - over-investigating a puzzling bug, against the ten-minute heuristic for checking in with a developer (`rst-ten-minute-heuristic`), which supports **time-box-puzzling-bug-investigation** (new, MAY)
- **Size charters right.**
  - Give direction without overspecifying test actions (`hendrickson-direction-without-overspecifying`).
  - A charter too specific becomes a weird way of writing tests (`hendrickson-too-specific`). One too broad gives no stopping point (`hendrickson-too-broad`).
  - Prefer several focused charters to one huge one (`hendrickson-multiple-focused-charters`).

  This supports **charter-neither-too-narrow-nor-too-broad** (new, SHOULD).
- **Frame charters with stakeholders and keep them open.**
  - Work with stakeholders on the most valuable questions (`hendrickson-work-with-stakeholders`).
  - Don't chase information nobody will act on (`hendrickson-actionable-information`).
  - Chartering is ongoing (`hendrickson-chartering-ongoing`), and a set of charters is always incomplete (`lyndsay-charters-incomplete`).

  This supports **charters-framed-with-stakeholders-and-kept-open** (new, SHOULD).
- **Tell the testing story, clean or not.**
  - Testing composes two stories, one of the product and one of the testing (`bolton-two-stories`).
  - The testing story covers how the product was operated and observed, what was not tested, and why the work was good enough (`bolton-story-of-untested`).
  - The result of testing is an assessment told as a story "including bugs, curios, etc." (`htsm-quality-story`).
  - Cover everything that matters, not just what is easy to see (`htsm-cover-what-matters`).

  **no-anomalies-said-plainly** therefore holds at SHOULD, and **clean-session-reports-coverage-and-gaps** is new at SHOULD. **clean-pass-reports-coverage**'s ban on padding a clean pass with observations has no source behind it. Session sheets and the quality story both keep notes and curios beside bugs (`sbtm-bugs-issues-notes`), so that part of the rule is unsupported.
- **Debrief, and document as you go.**
  - Dropping debriefs led to poor session sheets and meaningless metrics (`sbtm-dropping-debriefs-hurt`).
  - The method exists to bring accountability to informal exploratory work (`et3-accountability`).
  - The standing risk is failing to document something important (`bolton-risk-of-not-documenting`).
