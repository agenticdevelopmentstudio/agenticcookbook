You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-24. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/project-record-linking/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/project-record-linking/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/project-record-linking/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/project-record-linking/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/project-record-linking/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/project-record-linking/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/project-record-linking/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook roles check cookbook/guidelines/planning/project-management/project-record-linking`.

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
- R1.1: `rules.md` against sibling guidelines: some links this guideline makes a SHOULD or a MAY are required at a different strength by the sibling guideline for that kind of record, and nothing says which one governs. `intro.md` says each kind's own fields "stay with that record's own guideline". The rules still cover supersession, blockers and part-of links for every record, so the overlap is in the rules themselves. Under cookbook-compliance (must-not-contradict-applicable-guidelines, must-be-at-least-as-strict-as-guideline-musts, must-satisfy-all-applicable-guidelines-together) and behavioral-requirements (must-use-keywords-with-defined-semantics), a reader of both guidelines gets a waivable and an absolute version of the same behaviour. All the instances:
    1. `superseding-record-links-both-ways` (SHOULD: the superseding record links to the one it replaces, and the replaced one is marked superseded) against decision-records `acknowledge-contradicted-decisions` (MUST: "a new record that names the earlier decision, and the earlier record is marked superseded"). The same overlap shows in `close-or-supersede-never-delete`'s "marked superseded".
    2. `blocked-record-names-its-blocker` (SHOULD) against task-breakdown `blocked-task-references-blocker` (MUST: "blocked todos reference a specific blocker"), dependency-tracking `blocked-dependency-linked-to-affected-work` (MUST) and milestone-scheduling `blocked-milestone-has-issue-or-concern` (MUST).
    3. `child-record-carries-parent-link` (MAY) against task-breakdown `link-tasks-to-milestones` (SHOULD: each task linked to its milestone) and issue-tracking `link-fix-change-to-issue` (SHOULD: the fixing change linked to the issue). The research and `rationale.md` make this MAY about which end carries the link ("only GitHub documents which end carries it"). The rule text, "MAY carry the link to the larger record", reads as making the link itself optional.
    Fix: keep every strength, since the research supports nothing above SHOULD. Add one sentence to `intro.md`: where a kind of record's own guideline requires one of these links at a stronger level, that guideline governs for that kind, and this guideline is the baseline for the others. Name the four MUST rules above with in-text links (see the next finding). Reword `child-record-carries-parent-link` so the option is the end, not the link. For example: "Where a record is part of a larger one, such as a sub-issue under its parent issue, work under a milestone, or the change that resolves an issue, the link between them MAY be carried on the smaller record. (claims: ks-github-sub-issues-and-milestones, ks-github-closing-keywords)". Change its `a-build-must-establish.md` line to match ("where used, the link between a part record and the record it is part of is carried on the part record").
- R1.2: `intro.md` (second paragraph) and `linking-project-records.md` (step 5): sibling guidelines are named by freeform description. The intro has "decision supersession with decision records, issue resolution with issue tracking, blocked milestones with milestone scheduling, task blockers with task breakdown, and the risk and dependency fields with risk tracking and dependency tracking", and step 5 has "is a question for decision records". All six siblings exist and are in `related`. cross-recipe-consistency (must-reference-siblings-by-uuid, must-format-cross-references-consistently) asks for in-text `[rdid](cookbook:uuid)` links, the form decision-records uses for datastore-selection. Fix: write each one as its link: `[adc.guideline.planning.project-management.decision-records](cookbook:2b7a1593-48e0-4bbe-8e14-0df7a863628d)`, `…issue-tracking](cookbook:f77eeffe-2699-4028-9195-4bfc23c75e91)`, `…milestone-scheduling](cookbook:023d4c91-d797-4e82-880c-a4ad7906a54a)`, `…task-breakdown](cookbook:f264cc0b-45d3-4593-a437-7371610c5a8a)`, `…risk-tracking](cookbook:a55182ef-3144-407c-b64a-6377f37f5c63)` and `…dependency-tracking](cookbook:3f978ba7-c8c1-4b53-8fda-12e5a6966b75)`, each with the full `adc.guideline.planning.project-management.` rdid. Uses of "decision records" for the kind of record, such as in `rationale.md`, are not part of this finding.

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/project-record-linking, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/project-record-linking/review.md:
- `# Review: project-record-linking`
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
