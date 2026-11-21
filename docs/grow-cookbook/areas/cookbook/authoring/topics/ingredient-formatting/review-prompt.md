You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-21. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/ingredient-formatting/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/ingredient-formatting/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/review-1.md, /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/review-2.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/ingredient-formatting/diff-3.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook roles check cookbook/guidelines/cookbook/authoring/ingredient-formatting`.

This is round 3 of at most 3: a scoped re-review, not a
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
- R2.1: `rules.md`, `accessibility-role`, `accessibility-label`, `accessibility-state-announcements` (source fidelity, internal consistency). These rules are new this round. Each is a MUST with no "Applies when", so it binds every ingredient. `if-accessibility` says "Applies when: always". `wcag-name-role-value` covers only "user interface components". `accessibility-not-applicable-stated` and the new "Saying a section has nothing to say" bullet tell an infrastructure ingredient to say accessibility is out of scope. Under the three MUSTs, that same ingredient must also give a role, a label and its state announcements. The two sets of rules contradict each other, and the MUSTs reach past the claim's scope. The build-bar lines for all three repeat the gap. Fix: scope each of the three rules, and its build-bar line, to an ingredient with a user interface, for example "**Applies when:** UI ingredients; an infrastructure ingredient follows `accessibility-not-applicable-stated`."
- R2.2: `rules.md`, `short-required-core-labelled-optional-rest` (internal consistency). This text changed this round. It defines the required sections as "carried by every ingredient" and as those `if-section-order` leaves unmarked. `## Appearance` and `## States` are unmarked there, but `if-appearance` and `if-states` say they "MAY be omitted for infrastructure ingredients". So the rule calls two sections required by every ingredient when another rule lets some ingredients omit them. Fix: drop "carried by every ingredient", or qualify it, for example "(`## Appearance` and `## States` by UI ingredients only, per `if-appearance` and `if-states`)". If the build-bar line names the exception, make it match.
- R2.3: `rationale.md` (factual error against cited claims; every Rationale bullet is new this round). Three bullets say more than the claims they draw on. Every instance:
      - `tmpl-states-table`, `states-include-hover-and-selected`: the bullet says "Flutter's, Material's and Fluent's state lists include hover and selected". `fluent-rest-selected-states` names only rest and selected, and has no hover. Fix: "Flutter's and Material's state lists include hover and selected, and Fluent's includes selected."
      - `tmpl-logging-subsystem-category`: the bullet says "so that log messages can be filtered by functional area". Neither `apple-logger-subsystem-category` nor `apple-logger-optional` mentions filtering. The second claim says only that the two strings "add context to all messages you log". Fix: "so that each message carries the context of its functional area".
      - `section-structure-machine-checked`: the bullet says "MD043's wildcards stand only for unspecified headings, so named optional sections take a custom rule". `md043-wildcards-only`'s second check refuted exactly that inference: the doc also lists `%` regex headings and `^` loops, and never says a named heading cannot be optional or that a custom rule is needed. Fix: "MD043's wildcards `*`, `+` and `?` stand for unspecified headings; a custom rule can name an optional section".

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
