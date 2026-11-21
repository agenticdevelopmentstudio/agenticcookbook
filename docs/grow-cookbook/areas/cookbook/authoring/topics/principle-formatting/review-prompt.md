You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-21. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/principle-formatting/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/principle-formatting/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/principle-formatting/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/principle-formatting/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/principle-formatting/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/principle-formatting/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/principle-formatting/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook roles check cookbook/guidelines/cookbook/authoring/principle-formatting`.

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
- R1.1: `artifact.json` (cookbook-compliance; `cookr validate` Neutrality): the artifact names hosts with no reason given, so `cookr validate` reports `guidelines/cookbook/authoring/principle-formatting | unlisted | claude, codex` and exits 1 on this artifact's account. Every instance: `rules.md` lines 9, 11, 13, 16, 18, 19 and 23 (claim ids `claude-md-*` and `codex-*`, plus "Claude Code" and "Codex" in `pf-always-loaded-budget`); `rationale.md` lines 8, 11 and 16 ("Claude Code", "Codex", "Claude may"); `references.md` lines 12, 13 and 17 (Claude and Codex link titles and URLs). The host figures are the evidence the rules stand on, and `roles-every-part-roled` forbids `hosts/` in a roled artifact, so moving the wording out is not the fix. Fix: add `"names_hosts"` to `artifact.json` with a reason of 16 characters or more, for example "Cites agent hosts' published instruction budgets and guidance as the evidence for its rules.", then confirm `cookr validate` no longer lists this folder under Neutrality.
- R1.2: `rationale.md` (source-fidelity): two rationale lines say more than their claim supports. (1) `pf-key-guidance-first` says models "at high instruction density, show a bias toward earlier instructions (IFScale)". The second check refuted exactly that qualifier for `ifscale-earlier-instructions`: the abstract reports the bias but does not tie it to high density. (2) `pf-state-why`/`standard-research-cited` says "Nygard notes that a decision's motivation is the hardest thing to recover later", but the `adr-motivation-lost` quote says "One of the hardest things to track". Fix: drop "at high instruction density" from (1), and write "one of the hardest things to track" in (2).
- R1.3: `what-a-reviewer-looks-for.md`, `a-complete-review-must-establish.md`, `how-to-keep-the-rules.md` (cross-recipe consistency within the guideline: the review and how-to parts must match the rule they serve): `pf-statement` says the statement is "typically 1-3 sentences", but three parts turn that into a hard limit. Every instance: review-focus "a statement that … runs past three sentences"; review-bar "to hold the core idea in one to three sentences"; how-to "Write the statement first, in one to three sentences". Fix: make each one say "typically one to three sentences", for example review-focus "a statement that is not the core idea or runs well past the typical one to three sentences". `a-build-must-establish.md` already says "typically" and needs no change.
- R1.4: `a-build-must-establish.md`, `a-complete-review-must-establish.md`, `how-to-keep-the-rules.md`, `intro.md` (rule fidelity; owner open question 1): `pf-always-loaded-budget` applies only to "Principles that load on every task", and leaves to the owner whether principles load always or as skills. Four parts drop that condition and treat every principle as always loaded. Every instance: build-bar "`pf-always-loaded-budget`: the principle was sized with everything else always loaded, against the hosts' limits"; review-bar "the principle's share of the always-loaded total was weighed against the hosts' limits"; how-to "Count the principle with the others that load on every task"; intro "size it against the always-loaded budget". Fix: put the condition back in each, for example build-bar "a principle that loads on every task was sized with everything else always loaded, against the hosts' limits", and how-to "When the principle loads on every task, count it with the others that do". `what-a-reviewer-looks-for.md` ("principles whose always-loaded total is not weighed") already keeps the condition.
- R1.5: `rules.md` (behavioral-requirements `must-not-bundle-behaviors-into-one-requirement`; conventions' "one rule to a bullet"): eight rules not on the owner list each bundle several separately testable behaviours into one bullet. Every instance: `pf-frontmatter-complete` (required fields present; no `domain` field); `pf-key-guidance-first` (statement before bullets; most important bullets first); `pf-actionable-guidance` (bullets present when the statement is not self-evident; each bullet specific yet heuristic; each a full sentence; two to seven items of one structure); `pf-only-what-the-agent-lacks` (only what the agent lacks; no copied conventions or lint rules; add a bullet only for a repeated mistake); `pf-history-newest-first` (a row per version; each dated; latest first); `pf-format-checks-tool-enforced` (tool-decidable checks run by a tool; text holds only what no tool checks); `standard-one-source-per-topic` (one folder per topic; detail linked, not copied); `standard-research-cited` (research kept in `research/`; each rule cites its claims). Fix: split each into one named rule per behaviour. A prior rule name stays on one of its parts; the new names are free. Each part cites the subset of the original claims it stands on, at that subset's weakest strength, and each new rule gets its own `a-build-must-establish.md` line. Owner-listed rules (`pf-title-heading`, `pf-statement`, `pf-change-history`, `pf-brevity`, `roles-*-prior`) are exempt and stay as they are.
- R1.6: `intro.md` and `artifact.json` `summary` (consistency with `pf-state-why`): the intro says "specific bullets that say why" and the summary says "actionable bullets that say why". The rule asks the principle to say why it holds, and the how-to says the reason goes "in it [the statement] or in the bullet it explains". Neither asks every bullet to give a reason. Fix: intro "its core idea first with the reason it holds, then specific bullets"; summary, for example, "How a cookbook principle is shaped: required frontmatter, one title, its main point and why first, actionable bullets, a dated history, and roled parts." (148 characters).

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/principle-formatting, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/principle-formatting/review.md:
- `# Review: principle-formatting`
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
