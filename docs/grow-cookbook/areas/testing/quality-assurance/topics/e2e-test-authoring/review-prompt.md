You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-24. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/e2e-test-authoring/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/e2e-test-authoring/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/e2e-test-authoring/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/e2e-test-authoring/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/e2e-test-authoring/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/e2e-test-authoring/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/e2e-test-authoring/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook roles check cookbook/guidelines/testing/quality-assurance/e2e-test-authoring`.

This is round 2 of at most 3: a scoped re-review, not a
fresh one.

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

The findings still open, to rule on:
- R1.1: `rules.md`, `a-build-must-establish.md`, `a-complete-review-must-establish.md`: the rule `e2e-test-id-where-no-user-facing-locator` renames the verdict's rule `e2e-test-id-only-when-no-user-facing-locator`. Criterion 4 fixes the names the verdicts key on; it is the only verdict name that has no rule of that name (checked for all 21 verdicts). Fix: name the rule `e2e-test-id-only-when-no-user-facing-locator` in all three files.
- R1.2: Open question settled (owner-list.md: "Whether a test id may be a first-choice locator ... the owner decides which order the cookbook adopts"). The text adopts Testing Library's order in every place it talks about locator order: `rules.md` `e2e-locators-user-facing-first` ("first by user-facing attributes"); `rules.md` `e2e-test-id-where-no-user-facing-locator` ("Where no role or text match fits, a spec MAY"); `a-build-must-establish.md` line for that rule ("each test id locates an element no role or text match fits"); `what-a-reviewer-looks-for.md` ("with a test id only where nothing user-facing fits"); `writing-a-spec.md` step 2 ("Where nothing user-facing fits, add a test id"). The rationale then says the question is left open, which the rules contradict. `e2e-locators-user-facing-first` also drops part of the claim it cites: pg-pw-prioritize-user-facing recommends "user-facing attributes and explicit contracts", and Playwright's explicit contracts include test ids. Fix: say that user-facing locators and test ids are both preferred over structural locators, without ranking one above the other, in the rule, its build line, the reviewer text and step 2. Make the test-id rule a plain MAY with no "where nothing fits" condition. Keep the rationale's statement that the order is the owner's.
- R1.3: Rules and prose repeat what the second check refuted (second-check.md notes), so the text does not follow from the claims it cites. Every instance:
    (a) `e2e-dedicated-test-accounts` rests only on bp-owasp-standard-test-secrets. The second check says standard test secrets are there to cut secret-scanner false positives, "not to tell tests to use fake secrets instead of real ones", and the quote does not mention dedicated test accounts. The rule says what was refuted, and so do its build line, `writing-a-spec.md` step 7 ("Use dedicated test accounts"), `what-a-reviewer-looks-for.md` ("accounts are dedicated test accounts") and `rationale.md` ("OWASP's advice on standard test secrets is community guidance"). Fix: base the test-account half on claims that state it (ks-pw-account-per-worker's "multiple testing accounts", ks-pw-auth-state-sensitive's "your test account"). Reword the standard-test-secrets half to say what OWASP says, or drop it. Correct the rationale.
    (b) `e2e-gate-live-specs-needing-secrets` says "CI secrets" and that "the secrets are withheld". The second check says ks-gha-secrets-forks covers GitHub Actions only and leaves GITHUB_TOKEN out of the withholding. Fix: limit the rule to GitHub Actions and note the GITHUB_TOKEN exception. Add the exception to the matching rationale sentence.
    (c) `e2e-test-id-where-no-user-facing-locator` names "an `accessibilityIdentifier` on Apple platforms", but the second check says the page is UIKit's, not all Apple platforms. It names "a test tag in Compose", but pg-android-compose-semantics' quote does not mention test tags. The same wording is in `writing-a-spec.md` step 2 ("`accessibilityIdentifier` in UIKit or SwiftUI, a test tag in Compose"). Fix: write UIKit's `accessibilityIdentifier`, and drop the Compose test tag or describe it as finding a node in the semantics tree.
    (d) `e2e-hermetic-by-default-live-for-critical-paths` says real-server specs are "used sparingly, for the critical paths". The second check says the Cypress quote calls them "Great for" critical paths, not kept only for them; that "Use sparingly" is not in the quote; and that the source also recommends a test around each feature's happy path. "Most" and "sparingly" are also unanchored relative terms (behavioral-requirements `should-not-use-unanchored-relative-terms`). The same restriction is in the build line ("live specs cover critical paths"), `writing-a-spec.md` step 5 ("Keep a few specs against the real server for the critical paths") and `rationale.md` ("keeps real-server tests for the critical paths"). `rationale.md` also has "stubbed responses carry no guarantee ... so it keeps one true end-to-end test"; that "so" is the inference the second check refuted for ks-cy-stub-drift. Fix: say that specs stub the network in the main and that real-server specs suit the critical paths, with no "sparingly" or "only" (the count belongs to test-pyramid and the owner). Give drift as a downside Cypress lists, not as its reason.
    (e) `e2e-page-objects-hold-no-assertions` and its build line ("no page object makes a verification or assertion") are absolute. The second check records Selenium's exception (a page object may check that its page loaded) and Fowler's footnote (assertions on a page's invariants are fine). Fix: add that exception to the rule, the build line and the reviewer text.
    (f) `rationale.md` ("Testing Library's query priority and WebdriverIO's selector guide, which put role and accessible name first") and `writing-a-spec.md` ("WebdriverIO puts role plus accessible name first among its selectors"). The second check says the WebdriverIO page makes no such recommendation and rates `button=Submit` "Always / Best" and `aria/` only "Good". Fix: say only what ks-wdio-role-selector holds, that role plus name keeps matching through class, test-id and DOM changes.
    (g) `rationale.md`: "role locators rest on the accessibility tree and the accessible name WAI-ARIA defines". The second check says WAI-ARIA says nothing about role locators and never says they match on the accessible name. Fix: take the role-locator link from Playwright's `getByRole` (pg-pw-getbyrole) and Testing Library (pg-tl-byrole-top), and cite WAI-ARIA only for the definitions.
- R1.4: `rationale.md`, locator paragraph: "Several of the claims these rules cite were refuted in part by the second check, so none of the locator rules is a MUST." This is wrong for `e2e-test-what-the-user-sees`, `e2e-scope-automation-id-by-container`, `e2e-avoid-dom-structure-locators` and `e2e-prefer-unique-id-to-css-to-xpath`, none of which cites a refuted claim. Their SHOULD comes from the sources' recommending wording ("should", "recommend", "not recommended", "preferred"). The SHOULD rationale is therefore inaccurate (behavioral-requirements `must-explain-rationale-for-should-requirements`). Fix: give the actual reason for each SHOULD, and name the refuted claims only for the rules that cite them (`e2e-locators-user-facing-first`, `e2e-test-id-where-no-user-facing-locator`).
- R1.5: `rules.md` `e2e-trace-on-ci-failure`: "A failing E2E test on CI SHOULD be debugged from a recorded trace" governs how a person debugs, which no change or build can show (behavioral-requirements `must-be-independently-testable`, `must-describe-observable-behavior`). Its build line checks something else ("leaves a trace to debug from"). Fix: write the rule as the observable outcome the build line checks, for example "A suite SHOULD record a trace for each E2E test that fails on CI, to debug from instead of videos and screenshots", and keep the build line in step with it.
- R1.6: `artifact.json` `platforms` is `[]`, but the guideline's intro scopes it to the web, Apple platforms, Android and Windows, and its rules name Espresso, UIKit and Windows UI Automation. Criterion 6 asks for platforms that match the text, and template-conformance `must-make-platforms-a-sequence` asks for one or more canonical identifiers. Fix: set `platforms` to the cookbook's canonical names for the platforms covered, `web`, `ios`, `macos`, `android` and `windows` (drop `macos` if the Apple text stays UIKit-only).
- R1.7: Strength conflict with accepted guidelines (cookbook-compliance `must-be-at-least-as-strict-as-guideline-musts`), and the guidelines are not linked. `testing/properties-of-good-tests` has `must-be-isolated` and `must-be-deterministic`, and `testing/flaky-test-prevention` has `must-not-share-mutable-state`, `must-not-depend-on-execution-order` and `must-not-ignore-flaky-tests`, all MUST or MUST NOT. This guideline states the same things at SHOULD: `write-deterministic-specs`, `e2e-isolate-test-state`, `e2e-no-shared-test-data` and `e2e-fix-flaky-tests`. Neither guideline is in `related` or the intro's scope list. Fix for this topic: add `e5af9ba5-f484-40c3-9738-470090f5241c` (properties-of-good-tests) and `05d00147-5c49-42d8-bdbd-cf8fd7dc2379` (flaky-test-prevention) to `related`, and say in the Rationale that this guideline's research supports SHOULD where those guidelines state MUST. The orchestrator routes the strength question to properties-of-good-tests and flaky-test-prevention.

1. Rule on every open finding above, in `## Rulings`, one line each:
   `- <id>: fixed|disputed-accepted|routed|open — <reason>`.
   - `fixed`: the change resolves it.
   - `disputed-accepted`: the author disputed it in disputes.md and is
     right. A dispute you reject is `open`, with why.
   - `routed`: the finding belongs to a named sibling topic and was recorded
     in that sibling's write-brief.md if it has not passed stage 4, or in its
     integrate.md if it has. Name the sibling in the reason.
   - `open`: it still stands.
2. Raise a new finding only on text the diff shows changed this round, or for
   a factual error against a cited claim (name the claim). Nothing else is
   reviewed again.
3. Never ask to reverse a fix an earlier round asked for unless you cite the
   claim that makes that fix wrong.
A new finding names every instance of its class in the changed text.

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/e2e-test-authoring, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/e2e-test-authoring/review.md:
- `# Review: e2e-test-authoring`
- `## Findings`: new findings only, one top-level `- ` bullet each: the file,
  the rule or line, what is wrong (every instance), and the fix. Write `none`
  if there are none.
- `## Checked`: what you checked and found right, one bullet each.
- `## Rulings`: one line per open finding, as above.
- `## Lint`: the /lint-artifact result, then, as the section's last line,
  exactly `lint: clean` (no lint error) or `lint: fail <n>` (n lint errors).
  A script reads only that line; without it the round counts as a lint
  failure.
- last, a line of its own, exactly `verdict: pass` or `verdict: fail`.
  `fail` when a new finding, a ruling of `open`, or a lint error stands.
Reply with the verdict line only.
