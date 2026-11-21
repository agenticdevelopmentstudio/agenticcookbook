You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-21. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/activity-triggers/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/activity-triggers/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/activity-triggers/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/activity-triggers/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/activity-triggers/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/activity-triggers/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/activity-triggers/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook roles check cookbook/guidelines/cookbook/authoring/activity-triggers`.

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
- R1.1: `rules.md`, **retire-assesses-impact-and-migrates**: the MUST outruns its claim, and part of the claim has no rule. bp-retained-term-marked's quote makes marking a retained term MUST ("it must be marked, e.g., 'for retrieval purposes only'"), makes recording the date of its status change MUST ("the date of its change in status must be recorded in the history note and displayed to users"), and makes the successor cross-reference only SHOULD ("a cross-reference to the new term should be provided"). The rule puts "pointing to its successor" under the MUST and leaves out the dated status change. **trigger-change-history** then has the discontinuation date only as MAY ("the history note MAY also record the date the value was discontinued"), so the guideline sets that date one level weaker than its source. The how-to (`changing-the-vocabulary.md`, Retire) already says to record the date. I checked every other rule for a MUST that rests on a clause its source gives as should or may and found no other case. Fix: split it into "a retired value that is kept MUST be marked as kept for retrieval only, and the date of that change MUST be recorded in its history note" and "it SHOULD point to its successor", both citing bp-retained-term-marked, and make the discontinuation date in trigger-change-history agree with that MUST for retained values.
- R1.2: `rules.md`, **add-trigger-to-guide-first** against **canonical-values-only**: the same obligation appears at two strengths. canonical-values-only says every `triggers` value MUST be a value of the canonical table, which means a new value MUST be in the table before any guideline uses it. add-trigger-to-guide-first says the new value SHOULD be "added to the canonical table before any guideline uses it", which reads as permission to deviate. The build bar (`add-trigger-to-guide-first: … added to the table before any guideline used it`) and the review bar (`every new value was added to the table … before it was used`) inherit the clash. Fix: limit add-trigger-to-guide-first to what its claims support at SHOULD (favour an existing value, nominate a candidate, have the editor review it) and leave "in the table before use" to canonical-values-only's MUST, or state that clause as a consequence of canonical-values-only rather than as a separate SHOULD.
- R1.3: `rules.md`, compound rules (behavioral-requirements, must-not-bundle-behaviors-into-one-requirement and must-be-independently-testable): several new or supported rules bundle separately testable behaviours, often at different strengths, into one named rule. A builder or reviewer cannot pass or fail a part, and the build bar collapses each into one line. Every instance: **trigger-one-meaning-one-label** (MUST one meaning, MUST one label, MUST NOT share a meaning); **trigger-scope-note-per-value** (SHOULD scope note and example; SHOULD overlapping values say which applies); **add-trigger-to-guide-first** (SHOULD favour existing; SHOULD nominate, review and add); **trigger-change-history** (SHOULD entry date and dated changes with person; MAY discontinuation and succession); **rename-keeps-old-value-as-alias** (date the rename, keep an alias, match it hidden, retag automatically); **retire-assesses-impact-and-migrates** (MUST consider impact; MUST mark retained; MAY auto-migrate); **vocabulary-periodic-review** (SHOULD policies; SHOULD test and treat outliers as candidates); **measure-trigger-selection-with-labelled-tasks** (SHOULD measure with a three-part collection; SHOULD hold out; MAY repeat runs); **report-recall-and-precision** (SHOULD report both; SHOULD tune recall first); **one-to-five-triggers** (SHOULD one to five per guideline, plus a vocabulary-review clause that repeats vocabulary-periodic-review). Owner-list rules are exempt and are not listed. Fix: split each into one rule per keyword-bearing behaviour, keeping the verdict's rule name on the main behaviour, giving each new rule its own citation and its own `## A build must establish` line, and dropping one-to-five-triggers' review clause in favour of vocabulary-periodic-review.
- R1.4: `rules.md` and the bars, unanchored relative terms (behavioral-requirements, should-not-use-unanchored-relative-terms): requirements turn on words that have no threshold, so two reviewers can reach different verdicts. Every instance outside the owner-list rules: **keep-always-loaded-core-small** "kept small and focused" (and `a-complete-review-must-establish.md` "The always-loaded tier stayed small", `what-a-reviewer-looks-for.md` "keeps growing"); **one-to-five-triggers** "a value that far more guidelines carry than the rest, or that almost none carry"; **vocabulary-periodic-review** "values that are overused and values assigned very rarely" (and `changing-the-vocabulary.md` Review: "far more guidelines than the rest … almost none carry"); **add-trigger-to-guide-first** "only with a strong case"; **measure-trigger-selection-with-labelled-tasks** "realistic tasks" and "extensive guideline text". Fix: anchor each to something checkable that the research gives or the cookbook already measures, without inventing counts the owner reserved. For example: the always-loaded tier holds only what every task needs (the build bar's own wording); an outlier value is one the review's tag count flags under a threshold the review policy records; a strong case is one the nomination states and the editor accepts. Or name the anchor as the owner's to set, as `measuring-selection.md` already does for the set's size.
- R1.5: `rules.md`, `adding-triggers-to-a-guideline.md`, `changing-the-vocabulary.md` (completeness): the guideline never says where the canonical trigger table is. canonical-values-only, triggers-from-canonical-taxonomy, add-trigger-to-guide-first, the how-to steps ("Read the canonical trigger table…", "added to the table first") and the review bar all depend on "the canonical table", but no part names its location. The table lives in `guide/introduction/trigger-guide.md`, the draft input the area plan names and the file `gf-triggers-field` points to. A builder skill compiled from this guideline cannot find the list it must check against. Fix: name the table's location once, in the how-to's first step or in canonical-values-only's text (for example "the canonical trigger table in `guide/introduction/trigger-guide.md`"). Do not add a citation for it.
- R1.6: `examples.md`, first example: the triggers shown break **order-specific-to-general**. `database-operations, performance-optimization, schema-design` lists `schema-design` last, although it is the narrowest of the three: the table scopes it to "Designing database schemas, migrations", a part of `database-operations` "Writing queries, migrations, transactions". `performance-optimization`, which covers queries and rendering, is the broadest. Fix: reorder to `schema-design`, `database-operations`, `performance-optimization`, or choose values whose specific-to-general order is plain.
- R1.7: `what-a-reviewer-looks-for.md`, `a-complete-review-must-establish.md`, `changing-the-vocabulary.md`: the review parts and the how-to state requirements that no rule states, so the reviewer flags things the builder was never told. Every instance: (a) `what-a-reviewer-looks-for.md` "Tooling that accepts … a frontmatter that does not parse". **validate-trigger-values-mechanically** requires only that tooling reject values outside the table, and cites the parse behaviour (pg-bad-frontmatter-loads-always, refuted by the second check) only as a reason. (b) `changing-the-vocabulary.md` Retire, "Never delete a value with guidelines still carrying it and no replacement", and `what-a-reviewer-looks-for.md` "a retirement that deletes a value its guidelines still carry with no replacement or migration". **retire-assesses-impact-and-migrates** has no prohibition on deletion and cites bp-delete-without-replacement-loses-access only as a "since" clause. (c) `a-complete-review-must-establish.md` "Any change to triggers or the vocabulary that affects selection was measured on the labelled task set" and `what-a-reviewer-looks-for.md` "A selection change made without a labelled task set…". **measure-trigger-selection-with-labelled-tasks** says selection SHOULD be measured, not that each change is. Fix: either give each a rule at the strength its claims support (a parse-failure check at SHOULD at most, since pg-bad-frontmatter-loads-always is refuted; a deletion prohibition from bp-delete-without-replacement-loses-access and bp-retire-consider-impact; re-measurement after a change), each with its build-bar line, or cut the review and how-to lines back to what the rules say.
- R1.8: `rationale.md`, second paragraph: "agent hosts silently ignore fields and values they do not understand" overstates the claims. pg-unknown-fields-ignored-silently covers unknown frontmatter fields only ("any other field is ignored without an error"), and no claim says a host ignores unknown values. The only claim about malformed frontmatter, pg-bad-frontmatter-loads-always, was refuted by the second check for its "silently". The rule text (validate-trigger-values-mechanically) words this correctly. Fix: "an agent host ignores a frontmatter field it does not know without an error", matching the rule.
- R1.9: `rationale.md`, last paragraph, and `artifact.json` `related` (cross-recipe-consistency, must-reference-siblings-by-uuid; cookbook-compliance, should-reference-guideline-inline): the rationale names `context-and-memory-management` and the sibling topic `requirement-keywords` as bare names, not as `[<rdid>](cookbook:<uuid>)` links. The area plan says this topic cites `context-and-memory-management` for the general loading rule. `related` holds `context-and-memory-management` (0f999db4-956a-4124-a142-367b1a570983) but not `requirement-keywords`, which the text also points readers to. Fix: link both in the text, as [adc.guideline.implementing.skills-and-agents.context-and-memory-management](cookbook:0f999db4-956a-4124-a142-367b1a570983) and [adc.guideline.cookbook.authoring.requirement-keywords](cookbook:456f23bd-4523-47e8-9541-073ac046f2ad), and add 456f23bd-4523-47e8-9541-073ac046f2ad to `related`, or drop the requirement-keywords sentence, which this guideline has no rule for.
- R1.10: `artifact.json` and `rules.md` (cookbook-compliance, neutrality): `cookr validate`'s neutrality census lists this folder as `unlisted` for `claude` and `codex`, and lint fails on it. The only matches are the claim ids cited in rules (ks-claude-path-scoped-rules, pg-claude-md-size-adherence, ks-codex-size-limit). The research fixes those ids, so moving the text into `hosts/<target>.add.md` is wrong. The guideline is about how agent hosts load guidance, so the census's exemption is the right fix. Fix: set `names_hosts` in `artifact.json` to the reason ("cites research claims whose ids name the hosts they were measured on"), then re-run `cookr validate`.

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/activity-triggers, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/activity-triggers/review.md:
- `# Review: activity-triggers`
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
