You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-24. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/dependency-tracking/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/dependency-tracking/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/dependency-tracking/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/dependency-tracking/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/dependency-tracking/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/dependency-tracking/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/dependency-tracking/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook roles check cookbook/guidelines/planning/project-management/dependency-tracking`.

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
- R1.1: `examples.md`, the RAID-log table: the identity-team dependency is marked "Internal", but `map-internal-and-external-dependencies` defines internal as "under the team's control" and external as "beyond it", and the claim it cites (`internal-and-external-dependency-classes`) gives "delivery of a product from another project" as an external dependency. Another team delivering an endpoint is beyond the mobile team's control, so the example contradicts the rule it illustrates. Fix: mark the entry "External", or change the example to a dependency that is under the team's own control.
- R1.2: `rationale.md`, last paragraph: "PRINCE2 was reached only through secondary sources, so no rule rests on them" is untrue. `escalate-blocked-dependency-before-milestone` cites `prince2-manage-by-exception` (prince2.wiki, secondary) and names "the PRINCE2 project board once tolerance is exceeded", and `map-internal-and-external-dependencies` cites `internal-and-external-dependency-classes`, whose internal/external definitions are PRINCE2's as quoted by APM. Fix: keep "no rule rests on" for the PMBOK Guide, ISO 21502 and ISO 31000 only, and say PRINCE2 is reached through secondary sources (APM's quotation and prince2.wiki), which the escalation and internal/external rules use.
- R1.3: `rationale.md`, fourth paragraph: "each team dependency roughly halves the chance of on-time completion; it names no study, and gives only the direction of the effect, never a figure" states the figure the research forbids. research.md and the claim's `trust.basis` for `each-dependency-halves-on-time-chance` (trust 5, refuted by the second check) say it is usable "only as the direction of the effect, never as a figure", and "roughly halves" is a figure. The clause "gives only the direction of the effect" also puts the research's limit on the model, which does give a figure. Fix: state the direction only, e.g. "A practitioner teaching model, reported second-hand and naming no study, holds that each added team dependency lowers the chance of on-time completion; the research uses it for that direction only."
- R1.4: `rules.md`, bundled rules (behavioral-requirements must-not-bundle-behaviors-into-one-requirement; guideline-formatting one-requirement-per-rule): each of these rules joins two separately testable behaviours, so one can pass while the other fails: `dependency-owner-agreed-on-both-sides` (an agreed owner; the dependency confirmed and tracked in the other side's log), `dependency-has-need-by-date` (a need-by date is carried; the date is agreed with the source), `track-dependency-availability-and-status` (status tracked for the dependency's whole life; dependencies reviewed at regular points), `report-dependency-changes` (dependencies in the standard status reports; changes pushed to the people affected, already two SHOULDs in one bullet), `record-blocker-reason-and-duration` (a reason; a count of days blocked), `analyse-resolved-blockers` (resolved blocker records kept; clustered by cause), and `at-risk-dependency-logged-as-risk` (acknowledged as a risk with a management plan; reviewed for its effect on milestones). Fix: split each into one rule per behaviour, keeping the prior name on one half (names are fixed) and naming the other half freshly, each with its own citation and its own line in `a-build-must-establish.md` and its strength list in `a-complete-review-must-establish.md`.
- R1.5: `rules.md`, `record-blocker-reason-and-duration` and `analyse-resolved-blockers`, against sibling `task-breakdown` (cross-recipe-consistency; cookbook-compliance must-not-contradict-applicable-guidelines): both guidelines rule on the same blocked-work-item practice from the same Leopold and Magennis source at different strengths. Counting the days blocked is SHOULD here but recording the block's dates is MAY in `task-breakdown`'s `blocker-records-dates`; keeping resolved blockers is MAY here (bundled with clustering) but SHOULD in `task-breakdown`'s `keep-resolved-blockers`. A team keeping both guidelines gets two answers for one blocked task. Fix (this topic's part): scope these two rules to the blocked dependency record rather than "a blocked work item", or align their strengths with `task-breakdown` where the research allows it (research.md gives `record-blocker-reason-and-duration` "MAY to SHOULD"), and point to `task-breakdown` for blocked tasks. Any change to `task-breakdown` is that sibling's, for the orchestrator to route.
- R1.6: `artifact.json`, frontmatter `related` and `tags`: `related` is `[]`, although sibling guidelines this text overlaps already exist: `risk-tracking` (`a55182ef-3144-407c-b64a-6377f37f5c63`), whose risk register `at-risk-dependency-logged-as-risk` and the rationale's risk-register question turn on, and `task-breakdown` (`f264cc0b-45d3-4593-a437-7371610c5a8a`), which rules on blocked tasks, blocked-by links and blocker reasons that `flag-at-risk-or-blocked-dependencies`, `blocked-dependency-linked-to-affected-work` and `record-blocker-reason-and-duration` also cover. Criterion 6 asks for `related` to match the new guideline. `tags` also breaks the family vocabulary (cross-recipe-consistency must-use-family-tag-vocabulary): every sibling (`decision-records`, `issue-tracking`, `risk-tracking`, `task-breakdown`) tags itself with its own topic slug, and this one has `dependencies` but not `dependency-tracking`. Fix: add both uuids to `related` and add the tag `dependency-tracking`. Whether those siblings add this guideline to their own `related` is theirs.

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/dependency-tracking, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/dependency-tracking/review.md:
- `# Review: dependency-tracking`
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
