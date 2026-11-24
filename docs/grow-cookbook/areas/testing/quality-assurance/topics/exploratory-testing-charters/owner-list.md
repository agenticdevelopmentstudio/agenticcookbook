# Owner list: exploratory-testing-charters

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
