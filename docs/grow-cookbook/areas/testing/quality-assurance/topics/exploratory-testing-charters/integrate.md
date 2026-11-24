# Integrate: exploratory-testing-charters

Lossless: a new topic, with no base text in the cookbook (`roles lossless` reports the artifact is not in the base 77a898dbc718928bbd96ef617723c83ec69cd549); nothing to account for.

## For the owner

`cookr validate` owner-decides warnings for this topic. Each rule below cites its `-prior` claim, which the research rules unsupported or contradicted. The owner decides each rule: keep it as it is, reword it, or drop it. Each stands, word for word under the lead-in "This MUST hold:", until the owner decides.

- `session-has-hard-step-cap` (unsupported)
- `stay-on-charter-origin` (unsupported)
- `findings-stay-inside-charter` (contradicted)
- `anomaly-carries-all-four-parts` (contradicted)
- `clean-pass-reports-coverage` (unsupported)

The prior text of these rules, kept word for word as the owner list requires, carries the old team's words: "25 browser steps per pass" and "the site's own origin". The how-to and the review focus repeat them to stay consistent with the rules; a reword would make them general (a time box in place of a step count, the system under test in place of a site).

Open questions from owner-list.md:

- Whether an automated session keeps a step cap at all, keeps it beside a time box, or replaces it with a time box as every source uses; and, if kept, what number (no source gives 25 or any step count).
- Whether 'stay on the system under test's own origin' is kept as a safety or authorization policy of the house; no testing source states it, so it would rest on the owner's decision alone.
- Whether an anomaly found outside the charter is raised as a finding and its time logged as opportunity (as session-based test management does) or only listed as out-of-charter (as the current Verify rule has it).
- Whether the expectation stays a mandatory fourth part of every finding, or the finding must state its oracle only when the problem is not obvious, as the Rapid Software Testing guide advises.
- Whether padding a clean session with severity-free observations stays a fail, given that session sheets and the HTSM quality story both keep notes and curios beside bugs.
- Whether 'intermittent' requires one stated second attempt or a stated count of attempts and successes; Mozilla asks for 'at will, occasionally, or not at all' and more information when occasional, but no source fixes a number.

- from the phase 3 code review (claude-code-review/f1): `session-has-hard-step-cap` (MUST, a 25-browser-step hard cap) conflicts with `charter-names-scope-cap-focus-and-exclusions`, which bounds a session by a time budget rather than a step count, and `stay-on-charter-origin` is web-only although the intro covers any team; a 90-minute manual or desktop session sized by time fails both. The review suggests dropping or rescoping both MUSTs, for example to an agent-run browser pass only.
- from the phase 3 code review (claude-code-review/f6): `anomaly-carries-all-four-parts` (MUST) repeats the SHOULD `report-anomaly-where-what-expected-repeatable`, and `clean-pass-reports-coverage` (MUST) repeats `no-anomalies-said-plainly`, so the SHOULDs' stated-departure escape does nothing; the clean-pass MUST also fails a clean session that keeps the notes `session-sheet-keeps-bugs-issues-and-notes` asks for. The review suggests merging each pair into one rule at one strength.

integrated: 2026-11-24
