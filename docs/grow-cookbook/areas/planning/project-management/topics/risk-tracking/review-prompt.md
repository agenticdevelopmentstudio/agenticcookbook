You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-24. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/risk-tracking/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/risk-tracking/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/risk-tracking/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/risk-tracking/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/risk-tracking/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/risk-tracking/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/risk-tracking/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook roles check cookbook/guidelines/planning/project-management/risk-tracking`.

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
- R1.1: `rules.md`, bundled rules (behavioral-requirements must-not-bundle-behaviors-into-one-requirement; guideline-formatting one-requirement-per-rule): each of these rules joins two or more behaviours that can each be tested on its own, so one part can pass while another fails:
    - `risk-identification-and-attention-flagging`: identify risks whatever their source; surface new risks and impediments as they appear; record each one as soon as it is identified, whoever raised it.
    - `distinguish-immediate-action-from-monitoring`: evaluate each risk as needing action now or being watched; record its proximity (already two SHOULDs in one bullet).
    - `link-concerns-to-related-elements`: a unique identifier; the product or process it concerns (two SHOULDs).
    - `concern-has-status-and-raiser`: the raiser is named; a status is carried; the status history is kept (two SHOULDs plus the history clause).
    - `risk-review-cadence`: reviews are planned, with responsibility defined, inside the normal management flow; the register is checked for new or revised risks at each review (two SHOULDs).
    - `owner-most-capable-and-not-overloaded`: the owner is the person most capable; no one holds too many risks (two SHOULDs).
    - `risk-response-triage`: the response comes from a defined set of options; it is chosen by weighing benefit against cost (the build line checks the two separately).
    - `escalate-risks-beyond-tolerance`: escalation criteria are agreed; a risk beyond tolerance is escalated rather than accepted (two SHOULDs).
    - `describe-risk-as-cause-event-effect`: the description gives cause, event and effect; no entry duplicates another (the build line checks the two separately).
    Fix: split each into one rule per behaviour. The prior rule name stays on one half, because verdict names are fixed, and the other half gets a fresh name. Each new rule carries its own citation (the claims that support that half), its own line in `a-build-must-establish.md`, and an entry in the SHOULD list of `a-complete-review-must-establish.md`.
- R1.2: `rules.md`, the list as a whole (guideline-formatting keep-rule-lists-short; template/sibling structure): the 17 rules are one flat list, but a list SHOULD have no more than seven items where possible. The siblings group their rules under `###` subsections (`issue-tracking` has "Recording issues" and "Triage"; `dependency-tracking` has three to six rules per subsection). Fix: group the rules, including the new ones from the split above, under `###` subsections of seven or fewer. Possible groups are recording a risk, ownership, review, response and escalation, and tooling.
- R1.3: `rules.md`, `risk-becomes-issue-when-it-happens`, "SHOULD leave the risk register": this rests on the part of the claims that the second check refuted. `pmbok8-issue-already-happened` is refuted because "the source never says an issue no longer belongs in the risk register". `orange-book-contingency-if-risks-crystallise` is refuted because Principle D9 "does not say that crystallising is the point where something stops being a risk". `prince2-issue-is-event-that-happened` and `atlassian-raid-issues-need-immediate-attention` define an issue and set it apart from a risk, but neither says the risk leaves the register. The wording also contradicts the guideline itself in three places:
    - `concern-has-status-and-raiser` keeps each risk's status (active or closed) and its history in the register.
    - `keeping-a-risk-register.md` step 7 says to "close the risk and raise an issue".
    - The build-bar line says "is closed and raised as an issue".
    Fix: "A risk whose event has happened SHOULD be closed in the risk register and raised as an issue, which needs management action now." Add `prince2-risk-status-field` (active or closed; named by the `concern-has-status-and-raiser` verdict) to its citation.
- R1.4: `rules.md`, `flag-project-at-risk`, "alongside a record for each risk rather than in place of one", and its `a-build-must-establish.md` line, "beside its per-risk records": none of the cited claims supports the clause. `linear-health-at-risk` was refuted on exactly the per-risk part ("Nothing in the quote or the page supports 'no per-risk record type'"), and its quote supports only the project-level health indicator. The clause also decides part of the owner's open question on tracker mapping, which lists "a project health flag such as Linear's 'At risk'" as one candidate mapping for a small team, because it rules that flag out as the mapping. Fix: end the rule at the indicator: "A team MAY mark a project its risks threaten with a health indicator such as on track, at risk or off track. (claim: linear-health-at-risk)". Make the build line read "where used, a threatened project carries a health indicator". The other rules already ask for a record for each risk, so nothing is lost.
- R1.5: `artifact.json` `related` and `intro.md`, the scope paragraph (criterion 6; cross-recipe-consistency must-reference-siblings-by-uuid): `related` is `[]`, but the text hands every risk that has happened to issue tracking, and sibling guidelines it overlaps already exist:
    - `issue-tracking` (`f77eeffe-2699-4028-9195-4bfc23c75e91`, in `cookbook/index.json`). Its own intro sends "risks that have not happened" to this topic.
    - `dependency-tracking` (`3f978ba7-c8c1-4b53-8fda-12e5a6966b75`). Its `at-risk-dependency-logged-as-risk` rule feeds this register, and its round-1 review already asked that guideline to add this one to its `related`.
    The intro also names issue tracking in free prose, not by link. Fix: add both UUIDs to `related`, and in the intro link issue tracking as `[adc.guideline.planning.project-management.issue-tracking](cookbook:f77eeffe-2699-4028-9195-4bfc23c75e91)`, the form `issue-tracking`'s intro uses for its existing siblings. `project-record-linking` has no guideline yet, so it stays a topic mention.

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/risk-tracking, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/risk-tracking/review.md:
- `# Review: risk-tracking`
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
