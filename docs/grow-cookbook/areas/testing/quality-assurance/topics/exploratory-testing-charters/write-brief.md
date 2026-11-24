# Write brief: exploratory-testing-charters

Today is 2026-11-24.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/exploratory-testing-charters/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/exploratory-testing-charters/owner-list.md.
cookr, this checkout's own (never an installed one): PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>

Review criteria. Stage 4 reviews against exactly these, and the author writes to them:

1. Every guideline in /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/recipe-quality/:
   behavioral-requirements, completeness, cookbook-compliance,
   cross-recipe-consistency, source-fidelity and template-conformance.
2. Source fidelity means fidelity to the research:
   - every rule follows from the claims it cites, at the strength it states;
   - no claim with a `supported` or `new` verdict is left without a rule;
   - every rule ends with its citation, and every cited claim exists.
3. The strength rule: each rule is at the strength of the weakest claim it
   cites. A claim the second check refuted (listed under "Second-check
   corrections, refuted" in the write brief; its `trust.basis` says "Second
   check … refuted") cannot carry MUST. A claim that only lost a citation
   whose source lacked the quote (listed under "citation dropped") is still
   supported, and its strength is unchanged.
4. A rule's citations are authoritative. A verdict's `claims` list is stage
   2's record of the old rule: nobody compares it with the rule's citations,
   and research is not edited after stage 2. A rule may cite any claim of
   research.json that some verdict names. Prior rule names (the names the
   verdicts key on) are fixed; new rules may be named and renamed freely.
5. The owner list (owner-list.md): a prior rule listed there keeps its prior
   text word for word, citing `<rule>-prior`. Only its wording is exempt from
   review, nothing else. Where the prior text has no RFC keyword, one lead-in
   in front of it carries the keyword the old text implied ("In TypeScript,
   the panel MUST be reached this way:"); owner-list.md lists the lead-in, and
   it is the one change accepted. An open question listed there is the
   owner's: the text does not settle it, and it is never a finding.
6. Frontmatter: the author updates `summary` (160 characters or fewer,
   describing the new text), `tags`, `platforms` and `related` to match the
   new guideline. `version`, `modified` and Change History are left for stage
   5's `cookr bump`: a stale version, modified date or history is never a
   finding.
7. One topic at a time: a finding about a sibling topic's guideline names the
   sibling, and the orchestrator routes it there; it is not this topic's to
   fix.

Write one roled guideline, as a single markdown doc with frontmatter, that:
- keeps every rule whose verdict is `supported`, reworded only where the
  research says it is wrong or unclear, at the strength of its weakest cited
  claim;
- adds a named rule for every `new` verdict, at the strength of its weakest
  cited claim;
- leaves every rule on the owner list below worded exactly as its prior
  text, citing its `<rule-name>-prior` claim: `(claim: <rule-name>-prior)`.
  Where the prior text has no MUST, SHOULD or MAY, put one lead-in in front of
  it carrying the keyword the old text implied, and keep the text after it
  word for word;
- settles none of the open questions on the owner list;
- follows /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/guideline-formatting/rules.md,
  gf-roled-parts and gf-named-rules: an intro; a `## Rules` section of
  named rules `- **kebab-name**: … MUST|SHOULD|MAY …`; how-to and example
  sections; `## What a reviewer looks for`;
  `## A complete review must establish`; `## A build must establish`;
  `## Rationale`; `## References`; `## Change History`;
- gives `## A build must establish` exactly one line per named rule,
  `` - `rule-name`: … ``, and no line naming anything that is not a named
  rule of `## Rules` (`cookr roles check` refuses a rule with no line and a
  line naming no rule);
- cites research exactly as `cookr validate` enforces it: every named rule
  ends with one citation, `(claim: <id>)` or `(claims: <id>, <id>)`, with
  nothing after it, not even a full stop; only one citation per rule;
  every id is a claim `id` in research.json that some verdict names
  (gf-rule-cites-research);
- updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` to match the new text, and leaves `version`, `modified` and Change History to stage 5's `cookr bump`.

Edit only the draft. Never edit research, the owner list or another topic.
A finding you think is wrong is disputed, not obeyed: see the round sections
below, when there are any.

Verdicts:
- charter-names-scope-cap-focus-and-exclusions: supported (claims: charter-mission-scope-limitations, charter-optional-contents, charter-states-what-product-must-never-do, sbtm-session-sheet-sections, charter-is-unit-of-work, whittaker-landmark-concentrate, charter-detail-trade-off)
- look-for-what-specs-cannot-anticipate: supported (claims: iso-et-hunts-hidden-properties, et-explores-untested-areas, et-complements-formal-techniques, bolton-documentation-is-rumour, htsm-cover-what-matters)
- session-has-hard-step-cap: unsupported (claims: session-has-hard-step-cap-prior, session-is-chartered-time-box, sbtm-session-length-ninety-minutes, session-length-range)
- stay-on-charter-origin: unsupported (claims: stay-on-charter-origin-prior)
- report-anomaly-where-what-expected-repeatable: supported (claims: defect-report-expected-and-actual, defect-report-identifies-object-and-environment, defect-report-enables-reproduction, iso-incident-report-definition, mozilla-observed-and-expected, mozilla-reproducibility-at-will, apple-expected-results, bolton-peo-example, rst-seen-more-than-once, rst-frequency)
- no-anomalies-said-plainly: supported (claims: bolton-two-stories, bolton-story-of-untested, htsm-quality-story, sbtm-proof-debrief)
- anomaly-carries-all-four-parts: contradicted (claims: anomaly-carries-all-four-parts-prior, rst-judicious-expected, rst-pedantic-reporting, rst-indicate-oracles-unless-obvious)
- finding-is-observed-not-inferred: supported (claims: rst-grounded-in-observation, mozilla-facts-vs-speculation, bolton-peo-example, rst-unsupported-opinion, bolton-documentation-is-rumour, et3-testing-definition)
- findings-stay-inside-charter: contradicted (claims: findings-stay-inside-charter-prior, sbtm-on-charter-vs-opportunity)
- clean-pass-reports-coverage: unsupported (claims: clean-pass-reports-coverage-prior, bolton-story-of-untested, htsm-quality-story, sbtm-bugs-issues-notes)
- repeatability-states-retry: supported (claims: rst-tried-to-reproduce, rst-seen-more-than-once, mozilla-occasional-needs-more-info, mozilla-reproducibility-at-will)
- charter-states-target-resources-and-information-sought: new (claims: charter-format-explore-with-to-discover, hendrickson-template-via-lyndsay, ast-charter-definition, sbtm-session-definition, ghazi-charter-checklists, ghazi-levels-of-exploration)
- charter-neither-too-narrow-nor-too-broad: new (claims: hendrickson-direction-without-overspecifying, hendrickson-too-specific, hendrickson-too-broad, hendrickson-multiple-focused-charters, charter-does-not-list-tests, charter-detail-trade-off)
- charters-framed-with-stakeholders-and-kept-open: new (claims: hendrickson-work-with-stakeholders, hendrickson-actionable-information, hendrickson-chartering-ongoing, lyndsay-charters-incomplete, sbtm-todo-session-sheets)
- session-is-time-boxed: new (claims: session-is-chartered-time-box, sbtm-session-definition, sbtm-session-length-ninety-minutes, session-length-range, charter-is-unit-of-work)
- session-is-debriefed: new (claims: session-is-chartered-time-box, sbtm-debrief-each-session, sbtm-proof-debrief, sbtm-dropping-debriefs-hurt, sbtm-abort-or-rescope, et3-accountability)
- session-sheet-keeps-bugs-issues-and-notes: new (claims: sbtm-session-sheet-sections, sbtm-bugs-issues-notes, session-sheet-records-steps, session-sheet-logs-questions-observations, azure-test-feedback-extension, bolton-risk-of-not-documenting)
- off-charter-work-logged-as-opportunity: new (claims: sbtm-on-charter-vs-opportunity, hendrickson-temptations-new-charters)
- clean-session-reports-coverage-and-gaps: new (claims: bolton-two-stories, bolton-story-of-untested, htsm-quality-story, sbtm-proof-debrief, htsm-cover-what-matters)
- finding-states-its-oracle: new (claims: bolton-peo-problem, bolton-peo-oracle, rst-all-reports-based-on-oracle, rst-indicate-oracles-unless-obvious, rst-judicious-expected, bolton-oracles-vary-strength)
- finding-gives-steps-to-reproduce: new (claims: defect-report-enables-reproduction, defect-report-sufficient-information, mozilla-steps-most-important, apple-steps-to-reproduce, android-steps-to-reproduce, android-not-working-insufficient, rst-not-enough-to-reproduce, azure-action-log-reproduce)
- finding-records-environment: new (claims: defect-report-identifies-object-and-environment, rst-environment)
- one-problem-per-finding: new (claims: apple-one-issue-per-report, rst-one-problem-per-report)
- use-product-element-heuristics-and-tours: new (claims: htsm-model-purpose, htsm-product-elements, bolton-time-added-to-product-elements, whittaker-landmark-tour, iso-experience-based-tours-attacks)
- exploration-designs-runs-and-learns-together: new (claims: iso-et-definition, et-explores-untested-areas, kaner-et-definition, et3-testing-definition)
- check-for-duplicate-before-filing: new (claims: azure-duplicate-search)
- time-box-puzzling-bug-investigation: new (claims: rst-ten-minute-heuristic)

Second-check corrections, refuted (criteria 3 applies to these claims):
- hendrickson-template-via-lyndsay: refuted (quote-found yes, supports-claim partly); trust 55 -> 35; a rule citing it cannot carry MUST
- sbtm-abort-or-rescope: refuted (quote-found yes, supports-claim partly); trust 60 -> 40; a rule citing it cannot carry MUST
- sbtm-session-sheet-sections: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST
- azure-test-feedback-extension: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST
- bolton-risk-of-not-documenting: refuted (quote-found yes, supports-claim partly); trust 55 -> 35; a rule citing it cannot carry MUST
- bolton-two-stories: refuted (quote-found yes, supports-claim partly); trust 55 -> 35; a rule citing it cannot carry MUST
- htsm-product-elements: refuted (quote-found yes, supports-claim partly); trust 60 -> 40; a rule citing it cannot carry MUST
- bolton-time-added-to-product-elements: refuted (quote-found yes, supports-claim partly); trust 55 -> 35; a rule citing it cannot carry MUST
- kaner-et-definition: refuted (quote-found yes, supports-claim partly); trust 60 -> 40; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **session-has-hard-step-cap** — verdict `unsupported` (claims: session-has-hard-step-cap-prior, session-is-chartered-time-box, sbtm-session-length-ninety-minutes, session-length-range). Prior text, kept word for word: "Hard cap: 25 browser steps per pass." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: The ISTQB Foundation syllabus says session-based exploratory testing runs within a defined time box, is guided by a charter of test objectives, and is usually followed by a debriefing with the stakeholders.
  - against: In session-based test management as first published, sessions last about ninety minutes, deliberately loosely timed, with short sessions near forty-five minutes and long ones near two hours.
  - against: Lyndsay describes a session as a unit of time, typically 10 to 120 minutes, long enough to be useful and short enough to finish in one piece.
- **stay-on-charter-origin** — verdict `unsupported` (claims: stay-on-charter-origin-prior). Prior text, kept word for word: "Stay on the site's own origin." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **anomaly-carries-all-four-parts** — verdict `contradicted` (claims: anomaly-carries-all-four-parts-prior, rst-judicious-expected, rst-pedantic-reporting, rst-indicate-oracles-unless-obvious). Prior text, kept word for word: "Every reported anomaly carries all four parts: where (URL or path), what was seen, what was expected instead, and how repeatable it appeared. An anomaly missing the expectation is a fail — without it there is no claim of wrongness." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: The Rapid Software Testing guide asks testers to be judicious about an 'expected:' line and never to write a vacuous one such as 'the product should give the correct result'.
  - against: The Rapid Software Testing guide names pedantic reporting, such as 'Expected: product doesn't crash', as a common bug-report mistake.
  - against: The Rapid Software Testing guide asks the reporter to say why the behaviour is a bug unless it is obvious.
- **findings-stay-inside-charter** — verdict `contradicted` (claims: findings-stay-inside-charter-prior, sbtm-on-charter-vs-opportunity). Prior text, kept word for word: "Findings stay inside the charter's ranked focus areas and respect its "leave alone" rules; an anomaly in an excluded area is reported as out-of-charter rather than raised as a finding." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Session-based test management has testers report time on charter versus on opportunity, and encourages them to divert from the charter when they stumble on an off-charter problem that looks important.
- **clean-pass-reports-coverage** — verdict `unsupported` (claims: clean-pass-reports-coverage-prior, bolton-story-of-untested, htsm-quality-story, sbtm-bugs-issues-notes). Prior text, kept word for word: "A pass that found nothing says so plainly and reports the areas actually covered. Padding a clean pass with severity-free observations is a fail, and so is a silent empty result." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Bolton says the testing story covers how the product was configured, operated and observed, what has not been tested yet, what won't be, and why the work was good enough.
  - against: The Heuristic Test Strategy Model says the result of testing is an assessment told as a story, including bugs and curios, not a verification of quality.
  - against: A session sheet keeps bugs (product quality concerns), issues (questions about the test process or project) and notes (anything else, such as test ideas and risk lists) apart.

## Open questions

- Whether an automated session keeps a step cap at all, keeps it beside a time box, or replaces it with a time box as every source uses; and, if kept, what number (no source gives 25 or any step count).
- Whether 'stay on the system under test's own origin' is kept as a safety or authorization policy of the house; no testing source states it, so it would rest on the owner's decision alone.
- Whether an anomaly found outside the charter is raised as a finding and its time logged as opportunity (as session-based test management does) or only listed as out-of-charter (as the current Verify rule has it).
- Whether the expectation stays a mandatory fourth part of every finding, or the finding must state its oracle only when the problem is not obvious, as the Rapid Software Testing guide advises.
- Whether padding a clean session with severity-free observations stays a fail, given that session sheets and the HTSM quality story both keep notes and curios beside bugs.
- Whether 'intermittent' requires one stated second attempt or a stated count of attempts and successes; Mozilla asks for 'at will, occasionally, or not at all' and more information when occasional, but no source fixes a number.

## Round 1 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R1.1: `examples.md`, `running-a-chartered-session.md` step 8, `intro.md` paragraph 1: the text drops or makes conditional the expectation that the MUST rule `anomaly-carries-all-four-parts` requires on every anomaly ("where (URL or path), what was seen, what was expected instead, and how repeatable it appeared. An anomaly missing the expectation is a fail"). There are three instances. (1) The example finding has no `Expected:` line, only `Oracle:`, and its `Where: checkout, order confirmation page` is neither a URL nor a path, so the guideline's own illustration fails one of its MUST rules. (2) How-to step 8 says "what was expected (where that is not obvious) or why the behaviour is a problem". That makes the expectation optional, so following the how-to breaks the MUST, and it settles the owner's open question on whether the expectation stays a mandatory fourth part. (3) The intro's summary of a finding lists "where it was seen, the steps to reproduce it, the environment, why it is a problem, and how repeatable it was" and leaves out what was expected. Fix: give the example finding a path (for example `Where: /checkout/confirmation`) and an `Expected:` line (for example "the confirmation page shows the current cart total, 2 items, 30.00"), and keep the `Oracle:` line if wanted. In step 8, list what was expected unconditionally and give why the behaviour is a problem as an addition, not an alternative. Add "what was expected" to the intro's list.
- R1.2: `examples.md`, the session report with no problems found: the line `Time: 50 minutes on charter, 10 on opportunity (an unexpected currency switch in settings)` records an unexpected behaviour inside a report whose result is "no problems found". The charter puts "account settings" out of scope, and the report neither reports the behaviour as out-of-charter (MUST `findings-stay-inside-charter`) nor leaves it out of the clean result (MUST `clean-pass-reports-coverage`: "Padding a clean pass with severity-free observations is a fail"). The illustration takes a side on two owner open questions: whether an out-of-charter anomaly is raised or only listed as out-of-charter, and whether observations beside a clean result are a fail. Fix: make the opportunity time an off-charter area that held no anomaly and is not excluded by the charter (for example "10 on opportunity (the order-history page linked from the confirmation)"), and change the `New charter noted:` line to match.
- R1.3: `what-a-reviewer-looks-for.md`: the review focus weakens or leaves out MUST rules. There are three instances. (1) "kept within any step cap" treats the MUST `session-has-hard-step-cap` (25 browser steps per pass) as optional, which leans on the owner's open question on whether a step cap is kept at all. (2) "on the system's own origin" restates `stay-on-charter-origin` ("the site's own origin") in the open question's alternative wording. (3) Nothing checks the `clean-pass-reports-coverage` fail conditions (padding a clean pass with severity-free observations, a silent empty result) or the "URL or path" form of where in `anomaly-carries-all-four-parts`. Fix: write "kept within 25 browser steps per pass and on the site's own origin", and add checks that a clean pass is neither padded with severity-free observations nor returned empty, and that each anomaly gives where as a URL or path.
- R1.4: `running-a-chartered-session.md`: the how-to says it "shows one way to keep the rules", but none of its ten steps mentions four of the five MUST rules: `session-has-hard-step-cap` (step 5 sets only a time box), `stay-on-charter-origin` (step 6), `findings-stay-inside-charter` (step 6 covers only opportunity time and new charters, not reporting an anomaly in an excluded area as out-of-charter) and `clean-pass-reports-coverage` (step 10 does not say a clean pass is reported without padding and never as an empty result). Following the how-to as written therefore does not keep the rules it claims to show (completeness). Fix: add the 25-step cap per pass to step 5, the own-origin limit and the out-of-charter handling to step 6, and the no-padding, no-empty-result requirement to step 10, worded so that no open question is settled.
- R1.5: `rules.md`, two rules bundle independently testable behaviours under separate RFC keywords (recipe-quality behavioral-requirements, must-not-bundle-behaviors-into-one-requirement). (1) `look-for-what-specs-cannot-anticipate` asks a session to aim at what specifications and scripted tests do not cover, and also to treat documentation as unconfirmed until the product has been tried. A session can pass one and fail the other. (2) `charter-neither-too-narrow-nor-too-broad` asks a charter not to list individual tests, and also to be focused enough that the tester can tell when its target has been explored. Its build-bar line already checks the two separately. `finding-is-observed-not-inferred` is not an instance: its SHOULD and SHOULD NOT state one behaviour, positively and negatively. Fix: keep the prior name `look-for-what-specs-cannot-anticipate` for the first clause and move the documentation clause into a new SHOULD rule (for example `treat-documentation-as-unconfirmed`, citing `bolton-documentation-is-rumour`). Split `charter-neither-too-narrow-nor-too-broad` (a new rule, so it may be renamed) into two SHOULD rules, for example `charter-does-not-list-tests` and `charter-target-is-finishable`, each citing its claims. Add a build-bar line and a review-bar entry for each new rule.
- R1.6: `rationale.md`, last paragraph: "Most rules are recommendations because each rests on a single publisher's method, syllabus or guidance" is false for many of the SHOULD rules, which cite several independent publishers. Examples: `finding-gives-steps-to-reproduce` (ISTQB, Mozilla, Apple, Android, Rapid Software Testing, Microsoft), `report-anomaly-where-what-expected-repeatable` (ISTQB, ISO, Mozilla, Apple, Bolton, Rapid Software Testing), `session-is-time-boxed` (ISTQB, session-based test management, Lyndsay), `look-for-what-specs-cannot-anticipate` (ISO, ISTQB, Bolton, HTSM), `session-is-debriefed` (ISTQB, session-based test management), `finding-is-observed-not-inferred` (Rapid Software Testing, Mozilla, Bolton), `repeatability-states-retry` (Rapid Software Testing, Mozilla), `one-problem-per-finding` (Apple, Rapid Software Testing) and `finding-records-environment` (ISTQB, Rapid Software Testing). This is a source-fidelity error in the stated justification. Fix: give the reason the research actually gives: the research holds these rules at SHOULD against a practitioner-consensus bar, and the sources state them as reporting or method guidance a team can justifiably depart from. Drop the single-publisher claim, or limit it to the rules it is true of (for example `off-charter-work-logged-as-opportunity`, `dispatch-sessions-as-todo-charters`, `charter-set-kept-open`).
