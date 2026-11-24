# exploratory-testing-charters: research agent run (fallback)

team_probe: researchteam not runnable (missing distributions: PyYAML, aiohttp, mcp, websockets); one fresh Opus
agent ran the filled research prompt. Its reply, verbatim:

I wrote both research files, and the validator prints `Research passed.` Nothing is committed.

**Files:**
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters/research/research.json`
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters/research/research.md`

**Claims per question (93 in all):**
- best-practices: 24 (19 sourced, plus the 5 `-prior` claims)
- known-solutions: 21
- platform-guidelines: 13
- experts-view: 35

**Quote checks:**
- I checked every quote against the downloaded source texts. Two needed fixing: a stray space in Bolton's product-elements quote, and the Ghazi checklist quote, which I cut back to the sentence I had confirmed.
- These quotes come from WebFetch readings only, so there is no local copy to check them against: Mozilla, Apple and Android, plus the two arXiv abstracts. `limitations` records this for the Mozilla, Apple and Android pages; the arXiv abstracts are covered only as "read as abstract".
- Kaner's quote joins the words of a bulleted slide into one sentence, and its trust basis says so.

**Verdicts, existing rules (rule, verdict, claim ids):**
- charter-names-scope-cap-focus-and-exclusions, supported (SHOULD): charter-mission-scope-limitations, charter-optional-contents, charter-states-what-product-must-never-do, sbtm-session-sheet-sections, charter-is-unit-of-work, whittaker-landmark-concentrate, charter-detail-trade-off. The "cap" holds only as a planned duration, never as a step count.
- look-for-what-specs-cannot-anticipate, supported (SHOULD): iso-et-hunts-hidden-properties, et-explores-untested-areas, et-complements-formal-techniques, bolton-documentation-is-rumour, htsm-cover-what-matters
- session-has-hard-step-cap, unsupported: session-has-hard-step-cap-prior, session-is-chartered-time-box, sbtm-session-length-ninety-minutes, session-length-range
- stay-on-charter-origin, unsupported: stay-on-charter-origin-prior
- report-anomaly-where-what-expected-repeatable, supported (SHOULD): defect-report-expected-and-actual, defect-report-identifies-object-and-environment, defect-report-enables-reproduction, iso-incident-report-definition, mozilla-observed-and-expected, mozilla-reproducibility-at-will, apple-expected-results, bolton-peo-example, rst-seen-more-than-once, rst-frequency
- no-anomalies-said-plainly, supported (SHOULD): bolton-two-stories, bolton-story-of-untested, htsm-quality-story, sbtm-proof-debrief
- anomaly-carries-all-four-parts, contradicted: anomaly-carries-all-four-parts-prior, rst-judicious-expected, rst-pedantic-reporting, rst-indicate-oracles-unless-obvious
- finding-is-observed-not-inferred, supported: rst-grounded-in-observation, mozilla-facts-vs-speculation, bolton-peo-example, rst-unsupported-opinion, bolton-documentation-is-rumour, et3-testing-definition
- findings-stay-inside-charter, contradicted: findings-stay-inside-charter-prior, sbtm-on-charter-vs-opportunity
- clean-pass-reports-coverage, unsupported: clean-pass-reports-coverage-prior, bolton-story-of-untested, htsm-quality-story, sbtm-bugs-issues-notes
- repeatability-states-retry, supported: rst-tried-to-reproduce, rst-seen-more-than-once, mozilla-occasional-needs-more-info, mozilla-reproducibility-at-will

**Verdicts, new rules (all `new`):**
- charter-states-target-resources-and-information-sought (SHOULD): charter-format-explore-with-to-discover, hendrickson-template-via-lyndsay, ast-charter-definition, sbtm-session-definition, ghazi-charter-checklists, ghazi-levels-of-exploration
- charter-neither-too-narrow-nor-too-broad (SHOULD): hendrickson-direction-without-overspecifying, hendrickson-too-specific, hendrickson-too-broad, hendrickson-multiple-focused-charters, charter-does-not-list-tests, charter-detail-trade-off
- charters-framed-with-stakeholders-and-kept-open (SHOULD): hendrickson-work-with-stakeholders, hendrickson-actionable-information, hendrickson-chartering-ongoing, lyndsay-charters-incomplete, sbtm-todo-session-sheets
- session-is-time-boxed (SHOULD): session-is-chartered-time-box, sbtm-session-definition, sbtm-session-length-ninety-minutes, session-length-range, charter-is-unit-of-work
- session-is-debriefed (SHOULD): session-is-chartered-time-box, sbtm-debrief-each-session, sbtm-proof-debrief, sbtm-dropping-debriefs-hurt, sbtm-abort-or-rescope, et3-accountability
- session-sheet-keeps-bugs-issues-and-notes (SHOULD): sbtm-session-sheet-sections, sbtm-bugs-issues-notes, session-sheet-records-steps, session-sheet-logs-questions-observations, azure-test-feedback-extension, bolton-risk-of-not-documenting
- off-charter-work-logged-as-opportunity (SHOULD): sbtm-on-charter-vs-opportunity, hendrickson-temptations-new-charters
- clean-session-reports-coverage-and-gaps (SHOULD): bolton-two-stories, bolton-story-of-untested, htsm-quality-story, sbtm-proof-debrief, htsm-cover-what-matters
- finding-states-its-oracle (SHOULD): bolton-peo-problem, bolton-peo-oracle, rst-all-reports-based-on-oracle, rst-indicate-oracles-unless-obvious, rst-judicious-expected, bolton-oracles-vary-strength
- finding-gives-steps-to-reproduce (SHOULD): defect-report-enables-reproduction, defect-report-sufficient-information, mozilla-steps-most-important, apple-steps-to-reproduce, android-steps-to-reproduce, android-not-working-insufficient, rst-not-enough-to-reproduce, azure-action-log-reproduce
- finding-records-environment (SHOULD): defect-report-identifies-object-and-environment, rst-environment
- one-problem-per-finding (SHOULD): apple-one-issue-per-report, rst-one-problem-per-report
- use-product-element-heuristics-and-tours (MAY): htsm-model-purpose, htsm-product-elements, bolton-time-added-to-product-elements, whittaker-landmark-tour, iso-experience-based-tours-attacks
- exploration-designs-runs-and-learns-together (SHOULD): iso-et-definition, et-explores-untested-areas, kaner-et-definition, et3-testing-definition
- check-for-duplicate-before-filing (MAY): azure-duplicate-search
- time-box-puzzling-bug-investigation (MAY): rst-ten-minute-heuristic

`open_questions` holds six owner decisions, one entry each:
- whether to keep a step cap, and with what number
- whether to keep the same-origin policy
- how off-charter anomalies are filed
- whether the expectation stays mandatory or becomes "state the oracle unless obvious"
- whether padding a clean session stays a fail
- what "intermittent" requires as a stated retry
