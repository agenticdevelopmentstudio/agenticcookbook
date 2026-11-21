You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-21. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/requirement-keywords/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/requirement-keywords/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/requirement-keywords/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/requirement-keywords/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/requirement-keywords/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/requirement-keywords/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/requirement-keywords/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook roles check cookbook/guidelines/cookbook/authoring/requirement-keywords`.

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
- R1.1: `a-complete-review-must-establish.md`, `what-a-reviewer-looks-for.md`, `writing-a-requirement.md`: the review bar makes SHOULD rules items that a passing review must establish, and these parts state the uppercase case convention without the condition the rules attach to it. Instances:
    - (a) Review bar bullet 1, "in the form subject, keyword, operation", makes `one-keyword-per-requirement` (SHOULD) a pass condition.
    - (b) Bullet 3 does the same for `state-the-keyword-interpretation` (SHOULD).
    - (c) Bullet 4 does the same for `no-keywords-in-non-normative-text` (SHOULD NOT).
    - (d) Bullet 5 does the same for `one-keyword-set-never-mixed` and `no-mixed-case-negation-or-may-not` (SHOULD / SHOULD NOT).
    - (e) Bullet 6, "Lint findings take their severity from the keyword", makes `keyword-sets-finding-severity` a pass condition. That rule is a SHOULD, applies "by default", and says "The level stays configurable per check".
    - Since "A review passes when it establishes every item above", items (a) to (e) contradict the bar's own last bullet: "Every SHOULD rule is kept, or the change says why not".
    - (f) Review bar bullet 1 says "in uppercase", the review focus says "one uppercase keyword", and how-to step 2 says "Pick one keyword, in uppercase". `keywords-meaningful-only-in-uppercase` is conditional ("Where the cookbook follows BCP 14 as RFC 8174 states it … A document that declares a different convention … is read by its declaration"), and the build bar keeps that condition. These three parts drop it, which settles owner-list open question 1 (the case convention). They also contradict the kept MUST rule `gf-rfc-keywords-bold-or-uppercase` ("bold or uppercase"), which the same review bar lists as kept "with no exception".
    - Fix: reword bullets 1 and 3 to 6 so that each SHOULD item is something the review checks, kept or skipped with a stated reason, rather than a pass condition. Or drop them and rely on the two "Every MUST/SHOULD rule is kept" bullets. In all three parts, replace the unconditional "uppercase" with the rule's conditional form, or with "in the form the document's declared convention gives it".
- R1.2: `rules.md`: the guideline breaks its own `one-keyword-per-requirement` rule ("in the active form 'X MUST do Y' rather than the passive 'X MUST be Y'"), and `examples.md` labels exactly this form "Weak, passive". Every instance outside the owner-list wording:
    - `must-is-absolute-requirement`: "A rule's MUST MUST be read as …"
    - `should-is-recommendation`: "A rule's SHOULD MUST be read as …" and "the full implications MUST be understood and carefully weighed".
    - `may-is-optional-behavior`: "A rule's MAY MUST be read as …"
    - `keywords-meaningful-only-in-uppercase`: "only the UPPERCASE form of a keyword MUST be read as carrying its defined meaning".
    - `keywords-only-where-required`: "Keywords SHOULD be used with care and sparingly".
    - Fix: name the actor and use an active verb, for example "A reader MUST treat a rule's MUST as an absolute requirement …", "a deviating builder MUST first understand and weigh the full implications", and "An author SHOULD use the keywords with care and sparingly …".
- R1.3: `rules.md`: the rules break the guideline's own `lowercase-keyword-in-rule-text-flagged` rule and its fantasai-backed point that an ordinary-sense keyword word in rule text is an editorial error to reword. Its own linter would flag these lowercase keyword words in named-rule text:
    - `should-is-recommendation`: "a preferred but not required course" and "valid reasons to deviate may exist".
    - `may-is-optional-behavior`: "a course of action permitted, not required".
    - Fix: reword without the keyword words, for example "a preferred but not obligatory course", "valid reasons to deviate can exist" and "permitted, not obligatory". Claim ids and mentioned words inside quotes ("must and shall", 'MUST not') are not instances.
- R1.4: `rules.md`, `use-core-keyword-subset`: the rule says rules "SHOULD limit themselves to MUST, MUST NOT, SHOULD and MAY", which leaves out SHOULD NOT. This conflicts with the rest of the guideline:
    - The kept owner-list rules (`gf-rfc-keywords`, `rule-uses-rfc-2119-keywords`) enumerate five keywords, including SHOULD NOT.
    - The build-bar lines for `gf-rfc-keywords` and `rule-uses-rfc-2119-keywords` also list five.
    - The guideline's own rules use SHOULD NOT in `no-keywords-in-non-normative-text`, `warn-findings-do-not-block` and `no-mixed-case-negation-or-may-not` (twice).
    - The reading-a-keyword table lists SHOULD NOT.
    - Open question 4 itself describes Infra's encouraged set as "the five keywords MUST, MUST NOT, SHOULD, SHOULD NOT, MAY".
    - The build-bar line for `use-core-keyword-subset` repeats the four-keyword list.
    - Fix: list SHOULD NOT in the rule and in its build-bar line, or say explicitly that SHOULD NOT is the negation of SHOULD and falls within the subset.
- R1.5: `rules.md`, `warn-findings-do-not-block`: the closing clause, "a threshold that makes warnings block is an opt-in setting", says that a warning threshold exists or is allowed. That answers owner-list open question 3 ("Whether warnings ever block /approve-artifact … or never do"). Fix: drop the clause, or recast it as what the sources report, for example "the tools cited make a warning threshold optional", without saying whether `/approve-artifact` admits one.
- R1.6: `artifact.json` `references` and `references.md`: sources behind cited claims are missing. These claims are cited by the rules:
    - ISO/IEC Directives Part 2 Annex H (https://www.mhonarc.org/archive/html/ietf/2011-09/pdfBUKoWRBJxm.pdf) backs `iso-shall-requirement`, `iso-should-preferred`, `iso-may-permission`, `iso-no-must-for-shall` and `iso-no-may-not`. `rationale.md` names "ISO/IEC Directives Part 2" and "ISO/IEC" twice, and no reference backs either.
    - Atkins, spec-prod 0017, backs `tab-drop-formatting-requirement` and `tab-keywordless-must-equivalent`.
    - Sperberg-McQueen, spec-prod 0018, backs `sperberg-mcqueen-lowercase-misuse`, `sperberg-mcqueen-focus-attention` and `sperberg-mcqueen-iso-avoids-nonstandard-senses`.
    - fantasai, spec-prod 0016 and 0019, backs `fantasai-styling-requirement` and `fantasai-lowercase-misuse-is-editorial-error`.
    - Caceres, spec-prod 0024, backs `caceres-respec-defaults-bcp14` and `lint-unmarked-keyword-usage`.
    - The plainlanguage.gov shall-and-must page backs `plainlanguage-must-not-shall`.
    - https://vale.sh/docs/keys/minalertlevel backs `vale-minalertlevel-ci`.
    - The GitHub default-setup configuration page backs `github-ruleset-blocks-merge`.
    - Fix: add each URL to `references` and to `references.md`. The internal `git:` sources of the `-prior` claims need no entry.
- R1.7: `artifact.json` `related`: the field is `[]`, so it does not connect the guideline to the guidelines it overlaps with:
    - `guideline-formatting` (99eb40d3-98a6-4213-9fee-f8a62694dba4). Per the area plan, it cites this topic for keyword case and severity.
    - `recipe-quality/behavioral-requirements` (04fe1298-3880-4584-8a4a-c7a538eb5193), which states its own RFC 2119 keyword rules.
    - Fix: add both UUIDs.
- R1.8: Sibling `guideline-formatting` (route there, not this topic's to fix): its `rules.md` restates keyword rules this topic owns. The area plan says "The formatting topics cite it, never restate it". The restated rules:
    - `gf-rfc-keywords`, which also merges in the bold-or-uppercase text.
    - `normative-keywords-only-where-required`, which duplicates this topic's `keywords-only-where-required`.
    - Fix in guideline-formatting: cite requirement-keywords instead of restating these rules.

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/requirement-keywords, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/requirement-keywords/review.md:
- `# Review: requirement-keywords`
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
