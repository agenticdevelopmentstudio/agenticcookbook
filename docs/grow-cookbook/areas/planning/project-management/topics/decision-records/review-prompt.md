You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-24. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/decision-records/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/decision-records/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/decision-records/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/decision-records/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/decision-records/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/decision-records/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/decision-records/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook roles check cookbook/guidelines/planning/project-management/decision-records`.

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
- R1.1: `rules.md`, `supersession-links-both-ways` against `acknowledge-contradicted-decisions`: two behaviours are required twice, at two strengths. (1) Marking the earlier record superseded is a MUST in `acknowledge-contradicted-decisions` ("the earlier record is marked superseded") and a SHOULD in `supersession-links-both-ways` ("the superseded record SHOULD be marked superseded with a link to its replacement"). (2) The new record naming the record it replaces is a MUST in `acknowledge-contradicted-decisions` ("a new record that names the earlier decision") and a SHOULD in `supersession-links-both-ways` ("the new record SHOULD name the record it replaces"). Under cookbook-compliance (must-not-contradict) and behavioral-requirements (must-use-keywords-with-defined-semantics), one behaviour cannot be both absolute and waivable. The two build-bar lines and the review-focus sentence repeat the overlap. Fix: cut `supersession-links-both-ways` down to the one thing it adds, the link from the superseded record's mark to its replacement. For example: "When one record supersedes another, the superseded record's status SHOULD link to the record that replaces it. (claims: supersede-and-link, supersession-header-fields, gds-way-supersede-must)". It stays SHOULD, because it cites two refuted claims. Narrow its `a-build-must-establish.md` line to match ("each superseded record's status links to its replacement").
- R1.2: `a-build-must-establish.md`, `backfill-undocumented-decisions`: the line "where a log was started for an existing system, known past decisions were recorded where their data was available" turns a MAY rule into an obligation the build must meet. The other MAY rule's line is written "where used" (`record-confidence-level`), and the review bar files backfill under "noted where it was used". Fix: make the line conditional on use, e.g. "where used, past decisions recorded retroactively are ones whose data was available".
- R1.3: `intro.md`, first paragraph: "A later decision that changes an earlier one never edits or silently contradicts it" and "the two link to each other" state as absolutes what the rules hold at lower strength. Not editing an accepted record is SHOULD NOT (`supersede-never-edit-accepted-records`). It cannot carry MUST, because it cites the refuted `adr-tools-supersede-command` and `clarifications-may-amend`. Two-way linking is SHOULD (`supersession-links-both-ways`). Only the "silently contradicts" part is MUST. Fix: keep "never silently contradicts" and soften the rest so it matches the rules, e.g. "...is a new record rather than an edit, it marks the old one superseded, and the two should link to each other".
- R1.4: `intro.md`, second paragraph: "such as datastore selection" mentions a cookbook artifact by a freeform description. cross-recipe-consistency (must-reference-siblings-by-uuid, must-format-cross-references-consistently) asks for an in-text `[rdid](cookbook:uuid)` link, which is the form sibling `task-breakdown` uses in its rationale. The artifact is already in `related`. Fix: write it as `[adc.guideline.planning.data.datastore-selection](cookbook:6a653107-929d-418e-865d-636373a27b02)`. The other mention there, "project record linking", has no guideline or uuid yet, so a freeform mention is the only form available and is not part of this finding.
- R1.5: Lint FM-03: `cookbook/index.json` has no entry for id `2b7a1593-48e0-4bbe-8e14-0df7a863628d` (expected rdid `adc.guideline.planning.project-management.decision-records`). template-conformance must-have-index-entry-and-matching-rdid fails for the same reason, and `cookr validate` reports index drift for `guidelines/INDEX.md`. Fix: run `cookr update`, using this checkout's cookr, to add the index entry and regenerate the index.

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/decision-records, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/decision-records/review.md:
- `# Review: decision-records`
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
