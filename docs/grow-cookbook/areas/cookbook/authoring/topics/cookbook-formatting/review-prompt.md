You are re-reviewing a cookbook guideline you did not write. Today is
2026-11-21. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/cookbook-formatting/ (artifact.json and one .md per part).
Its research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/cookbook-formatting/research/research.json and research.md.
The second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/cookbook-formatting/second-check.md.
The owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/cookbook-formatting/owner-list.md.
The earlier reviews: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/cookbook-formatting/review-1.md
The author's disputes: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/cookbook-formatting/disputes.md (absent when there are none).
What changed this round: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/cookbook-formatting/diff-2.md (the diff from the previous draft).

Run cookr, this checkout's own, as `PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook <command>`: for example
`PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook roles check cookbook/guidelines/cookbook/authoring/cookbook-formatting`.

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
- R1.1: `rules.md`, `version-is-semver` (strength rule, criterion 3): the rule is SHOULD, but it cites `android-semver-good-basis`. That claim says Android's guidance points at Semantic Versioning "without mandating it" ("many developers consider Semantic Versioning a good basis"), and the second check notes "the guidance does not mandate SemVer". So the weakest cited claim is below SHOULD. I checked all 50 rules for a SHOULD or MUST that cites a claim whose own wording is permissive or non-mandating. This is the only instance. Definitional and factual claims, such as `jsonschema-required-keyword`, `jsonschema-const-keyword` and `topological-order-needs-dag`, do not weaken a rule. Fix: drop "as Android's guidance points to" and `android-semver-good-basis` from the citation. The rule still rests on `semver-normal-version-form`, `semver-no-leading-zeroes`, `swiftpm-version-semver`, `npm-version-node-semver` and `cargo-version-three-numeric-parts`, and the `version-is-full-semver` verdict keeps its rule. Leave the Android point to `rationale.md` if it is wanted.
- R1.2: `rationale.md` (source fidelity, criterion 2): three sentences say more than, or the opposite of, the research. (1) Paragraph 3: "Unknown keywords are treated as annotations too". This flat statement is the overstatement the second check refuted for `jsonschema-unknown-keywords-annotations`: Core 2020-12 says they "SHOULD be treated as annotations", and Ajv's strict mode rejects them. `validate-the-schema-strictly` already words it correctly. Fix: "JSON Schema 2020-12 says unknown keywords should be treated as annotations, so a misspelt keyword in the schema constrains nothing unless the schema is compiled strictly." (2) Paragraph 2: "as Cargo checks a package by building it rather than by parsing its manifest". `cargo-package-verify-build` says Cargo's packaging step checks the package "beyond parsing it", not instead of parsing it. Fix: "as Cargo's packaging step checks a package by building it, beyond parsing its manifest". (3) Last paragraph: "no outside source requires them or argues against them". The research has a source against one of them: the `cf-required-project-fields` verdict cites `npm-name-version-required-to-publish` (npm requires only name and version, and only for a package that will be published), and owner-list.md lists it as "against". Fix: "…are this cookbook's own design; no outside source requires them, and npm, for one, requires only `name` and `version`, and only of a package it publishes."
- R1.3: `a-build-must-establish.md` and `what-a-reviewer-looks-for.md`, `closed-objects-keep-an-extension-point` (the bars must match the rule's strength, cross-recipe-consistency within the guideline): both halves of the rule are MAY, including "a closed object meant to be extended through `allOf` MAY be closed with `unevaluatedProperties`". Both parts turn the second half into an unconditional requirement. Build bar: "closed objects extended through `allOf` use `unevaluatedProperties`". Review focus: "an object meant to be extended through `allOf` uses `unevaluatedProperties`". I checked every other MAY rule's build-bar line and review-focus bullet, and each is conditional ("when marked", "when present", "when generated", "when added"). Fix: build bar "an extension point, when added, is open for other tools, and a closed object extended through `allOf`, when closed with `unevaluatedProperties`, sees its subschemas' properties". Review focus: "an object meant to be extended through `allOf`, if closed, is closed with `unevaluatedProperties` rather than `additionalProperties`, or the change says why".
- R1.4: `artifact.json` `related` (frontmatter, criterion 6): `related` is `[]`, though the new text rests on a sibling guideline. `cf-source-domains` needs every `source.id` to be "the UUID of an ingredient or recipe" that resolves in `index.json`. `cf-code-root-coverage` and `cf-library-tree-mirrors-code` depend on "artifact's implementations" recorded in `index.json`. `ingredient-formatting` (`2c5ee8e0-9da5-4b44-9f87-51962abe76ab`) defines that identity and the `index.json` implementations (`if-reference-implementations`). Its siblings `guideline-formatting`, `ingredient-formatting` and `principle-formatting` all fill `related`. Fix: add `2c5ee8e0-9da5-4b44-9f87-51962abe76ab` to `related`.

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

Then run the /lint-artifact skill on /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/cookbook-formatting, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/cookbook-formatting/review.md:
- `# Review: cookbook-formatting`
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
