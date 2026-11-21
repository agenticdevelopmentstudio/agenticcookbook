You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-21. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/ingredient-formatting/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/ingredient-formatting/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook roles check cookbook/guidelines/cookbook/authoring/ingredient-formatting`.

This is round 2 of at most 3: a scoped re-review, not a
fresh one.

Review criteria. Stage 4 reviews against exactly these, and the author writes to them:

1. Every guideline in /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/recipe-quality/:
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
- R1.1: `rules.md` (source fidelity, strength rule): four rules that are not on the owner list carry MUST, but the weakest claim each one cites is only a recommendation or advice. Every instance:
    - `if-overview` cites `govuk-when-to-use`. That claim is an unmarked template prompt ("Briefly describe the situation(s) when to use this component"). The same template marks only the description as required (`govuk-description-required`: "It is required to display the description"), and `govuk-template-empty-fields-hidden` shows its other fields are optional. So "when to use it" is at MUST without support.
    - `if-behavioral-requirements` cites `oasis-ta-identifier` (an OASIS Committee Note; "It is recommended that the identifier be made universally unique") and `respec-conformance-lint` (a tool that only "will warn you").
    - `if-accessibility` cites `apple-strive-min-control-size` ("Strive to meet …") and `android-touch-target-48dp` ("we recommend …"). These two are the only claims behind its "minimum tap target size" item. `apg-button-role` is descriptive.
    - `if-test-vectors` cites `w3c-qa-test-assertions` (good practice GP12, "not a requirement"), `w3c-qa-template-test-assertion-section` ("advisory") and `oasis-ta-normative-source` (Committee Note).
    - Fix: in each rule, keep MUST only on the part a MUST-strength claim carries, and move the rest to SHOULD:
      - `if-overview`: MUST for what the component is (`govuk-description-required`); "when to use it" becomes SHOULD, in this rule or in `overview-states-when-not-to-use`.
      - `if-accessibility`: MUST for role, label and announced state changes (`wcag-name-role-value`); the tap-target item becomes SHOULD (`per-platform-target-sizes` already holds it at SHOULD).
      - `if-behavioral-requirements` and `if-test-vectors`: lower to SHOULD, or cite only their MUST-strength claims (`w3c-qa-conformance-clause`, `w3c-qa-consistent-requirement-style`, `w3c-qa-indicate-levels`, `act-examples-pass-fail-inapplicable`) for the MUST part and give the rest SHOULD.
    - I checked the other non-owner MUST rules and they hold: `accessibility-options-include-text-size` (WCAG AA), `analytics-event-names-fit-platform-limits` (Firebase's hard limits), `released-version-immutable` (SemVer MUST).
- R1.2: `rules.md`, `tmpl-feature-flags-table` (source fidelity): the MUST covers the table layout `| Flag Key | Default | Description |`. `openfeature-flag-key-and-default` supports only that a flag has a key and a default value, and it says that about the client evaluation API, not about a documentation table. The build-bar line already leaves the table out ("every flag … has its key and its default value"). Fix: keep the MUST on "give each flag its key and its default value". Put the table at SHOULD, or drop it.
- R1.3: `rules.md` (source fidelity: every rule follows from the claims it cites): three rules cite a claim their text does not use, or say more than the claim supports. Every instance:
    - `tmpl-appearance-properties` cites `fluent-contrast-in-all-states` but says nothing about contrast. Contrast is `appearance-contrast-in-all-states`'s subject.
    - `tmpl-states-table` cites `wcag-name-role-value`. That claim is about states being programmatically determinable and announced, not about a visual table of appearance changes.
    - `tmpl-design-decisions-approved`: its first SHOULD ("Each decision … SHOULD be recorded in `## Design Decisions`") has no supporting claim, because `nygard-adr-status` covers only a decision's status. Its second SHOULD says "approved by the user", but the claim says "project stakeholders".
    - Fix:
      - Drop `fluent-contrast-in-all-states` from `tmpl-appearance-properties`. `appearance-contrast-in-all-states` still cites it.
      - Drop `wcag-name-role-value` from `tmpl-states-table` (`if-accessibility` still cites it), or add the programmatic-state point the claim actually makes.
      - Reduce `tmpl-design-decisions-approved` to the status the claim supports, for example "Each decision in `## Design Decisions` SHOULD carry its status: pending (proposed) until its stakeholders agree, then yes (accepted)." Change its build-bar line to match.
- R1.4: `rules.md`, `accessibility-options-include-text-size` (internal consistency): the rule says an ingredient that shows text MUST give its text-resize behaviour "in `## Accessibility Options`". `if-section-order` marks that section "(MAY omit)", and nothing tells the author that such an ingredient must therefore carry it. Its build-bar line also leaves out where the statement goes. Fix: say so in the rule, for example "… MUST carry `## Accessibility Options` and say there how its text resizes …". Alternatively, put the statement in `## Accessibility`, which is always present. Make the build-bar line name the section either way.
- R1.5: `a-build-must-establish.md` (the build bar must match the rule it checks): four lines for owner-list rules leave out values that the kept rule text requires. Each omission quietly leans toward an open question that belongs to the owner. Every instance:
    - `tmpl-accessibility-min-tap-target` drops "44×44pt" (open question 4).
    - `tmpl-deep-linking-patterns` drops the three URL patterns, among them `{{app_scheme}}://component-name` (open question 6).
    - `tmpl-analytics-events` drops the two template rows and their dotted names (open question 5).
    - `if-compliance` drops the status values `passed`, `failed`, `partial` (open question 7).
    - Fix: restore each value as the rule states it, for example "`## Accessibility` holds the template's items: …, and a minimum tap target of 44×44pt" and "… Status values `passed`, `failed`, `partial`, each check linked to its definition".
- R1.6: `rules.md` (behavioral-requirements `must-not-bundle-behaviors-into-one-requirement`): rules that are not on the owner list bundle separately testable behaviours into one bullet. Every instance:
    - `short-required-core-labelled-optional-rest`: core and optional labels; the specified heading and level.
    - `overview-states-when-not-to-use`: when not to use; why to use.
    - `if-overview`: what it is; when to use it.
    - `if-behavioral-requirements`: the section is present; RFC 2119 keywords; bold kebab-case names.
    - `if-accessibility`: four separate items, plus the infrastructure "not applicable" case.
    - `if-test-vectors`: the four-column table; each vector mapped to a named requirement.
    - `tmpl-test-vector-id-format`: unique ID form; requirements named; table form.
    - `assumptions-and-limitations-stated`: assumptions, limitations and exceptions; out of scope and why.
    - `tmpl-privacy-fields`: the four fields; an ingredient that collects nothing says so.
    - `tmpl-logging-subsystem-category`: Apple's meaning for subsystem and category; the events table.
    - `tmpl-platform-notes-platforms`: an entry per targeted platform; the "nothing to add" line.
    - `tmpl-design-decisions-approved`: recorded; approved.
    - `tmpl-feature-flags-table`: key and default; table.
    - Fix: split each into one named rule per behaviour. The verdict name stays on one part, and new names are free. Each part cites the subset of the original claims it rests on, at that subset's weakest strength. Each new rule gets its own `a-build-must-establish.md` line, and every `supported` and `new` claim stays cited.
- R1.7: `rationale.md` (behavioral-requirements `must-explain-rationale-for-should-requirements`): the Rationale covers 11 of 53 rules. These SHOULD rules give no reason, either inline or in the Rationale: `tmpl-approval-fields`, `overview-states-when-not-to-use`, `appearance-contrast-in-all-states`, `tmpl-states-table`, `states-include-hover-and-selected`, `accessibility-keyboard-interaction`, `tmpl-test-vector-id-format`, `assumptions-and-limitations-stated`, `tmpl-deep-linking-patterns`, `tmpl-accessibility-options`, `tmpl-analytics-events`, `tmpl-privacy-fields`, `privacy-states-encryption-in-transit`, `tmpl-logging-subsystem-category`, `tmpl-design-decisions-approved`, `tmpl-compliance-link-form`, `change-history-iso-dates`. The ones that do give a reason are `tmpl-localization-table` ("for the translator"), `tmpl-platform-notes-platforms` ("since each platform's own guidelines differ") and those in `rationale.md`. Fix: add one Rationale bullet per rule, or an inline "so that …" clause, drawn from the cited claim. Examples:
    - `change-history-iso-dates`: an ISO standard date format, per Keep a Changelog.
    - `tmpl-compliance-link-form`: a UUID is unique across space and time, so the link survives renames.
    - `accessibility-keyboard-interaction`: APG documents keyboard interaction beside roles, states and properties.
- R1.8: `rules.md` `short-required-core-labelled-optional-rest` and `intro.md` (behavioral-requirements `should-not-use-unanchored-relative-terms`): "a short core of sections" gives no threshold and names no core, so a build cannot test "short". Fix: define the core as the sections `if-section-order` does not mark "(MAY omit)", or drop "short" in both places.

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/ingredient-formatting, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/review.md:
- `# Review: ingredient-formatting`
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
