# Write brief: principle-formatting

Today is 2026-11-21.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/principle-formatting (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/principle-formatting/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/principle-formatting/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/principle-formatting/owner-list.md.
cookr, this checkout's own (never an installed one): PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook <command>

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

Write one roled guideline, as a single markdown doc with frontmatter, that:
- keeps every rule whose verdict is `supported`, reworded only where the
  research says it is wrong or unclear, at the strength of its weakest cited
  claim;
- adds a named rule for every `new` verdict, at the strength of its weakest
  cited claim;
- leaves every rule on the owner list below worded exactly as its prior
  text, citing its `<rule-name>-prior` claim: `(claim: <rule-name>-prior)`.
  Where the prior text has no MUST, SHOULD or MAY, put one lead-in in front of
  it carrying the keyword the old text implied, and keep the text after it
  word for word;
- settles none of the open questions on the owner list;
- follows /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/tbd/compliance/artifact-formatting/guideline-formatting.md,
  gf-roled-parts and gf-named-rules: an intro; a `## Rules` section of
  named rules `- **kebab-name**: … MUST|SHOULD|MAY …`; how-to and example
  sections; `## What a reviewer looks for`;
  `## A complete review must establish`; `## A build must establish`;
  `## Rationale`; `## References`; `## Change History`;
- gives `## A build must establish` exactly one line per named rule,
  `` - `rule-name`: … ``, and no line naming anything that is not a named
  rule of `## Rules` (`cookr roles check` refuses a rule with no line and a
  line naming no rule);
- cites research exactly as `cookr validate` enforces it: every named rule
  ends with one citation, `(claim: <id>)` or `(claims: <id>, <id>)`, with
  nothing after it, not even a full stop; only one citation per rule;
  every id is a claim `id` in research.json that some verdict names
  (gf-rule-cites-research);
- updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` to match the new text, and leaves `version`, `modified` and Change History to stage 5's `cookr bump`.

Edit only the draft. Never edit research, the owner list or another topic.
A finding you think is wrong is disputed, not obeyed: see the round sections
below, when there are any.

Verdicts:
- pf-frontmatter-complete: supported (claims: pep-preamble-required, skill-frontmatter-required, json-schema-required, astro-frontmatter-schema)
- pf-type-field: supported (claims: json-schema-const, pep-preamble-required, astro-frontmatter-schema)
- pf-title-heading: unsupported (claims: pf-title-heading-prior, md041-frontmatter-title-satisfies, md025-frontmatter-title-counts, markdownlint-custom-rules-frontmatter)
- pf-statement: unsupported (claims: pf-statement-prior, lead-with-main-point, ms-lead-with-most-important, google-opening-sentence, pep-abstract-short, google-paragraph-length, vale-metric-formulas)
- pf-actionable-guidance: supported (claims: right-altitude, claude-md-specific-concise, claude-md-headers-and-bullets, cursor-focused-actionable, ms-lists-short, nygard-bullets-not-fragments, diataxis-keep-bounded)
- pf-change-history: unsupported (claims: pf-change-history-prior, changelog-entry-per-version, changelog-dated, md043-required-headings)
- pf-brevity: unsupported (claims: pf-brevity-prior, claude-md-200-lines, skill-body-500-lines, agentskills-progressive-disclosure, cursor-rules-500-lines, codex-32kib-combined, copilot-two-pages, ifscale-density-degrades, chroma-context-rot, lost-in-the-middle, context-finite-resource, minimal-not-short, claude-md-line-gets-lost, ms-be-brief, adr-short-record, diataxis-keep-bounded, md013-measures-line-width)
- standard-roled-parts: supported (claims: evaluator-optimizer, skills-lighter-than-always-loaded, agentskills-progressive-disclosure)
- standard-named-rules: supported (claims: claude-md-headers-and-bullets, cursor-rules-500-lines, ms-lists-short)
- standard-one-source-per-topic: supported (claims: claude-md-conflicts, cursor-reference-not-copy, diataxis-keep-bounded)
- standard-research-cited: supported (claims: adr-motivation-lost, prompting-explain-why, diataxis-explain-why)
- roles-vocabulary: unsupported (claims: roles-vocabulary-prior)
- roles-intro-history-unroled: supported (claims: changelog-for-humans, claude-md-every-line-costs, claude-md-only-what-agent-lacks, lead-with-main-point)
- roles-principle-may-be-roled: supported (claims: evaluator-optimizer, skills-lighter-than-always-loaded, agentskills-progressive-disclosure)
- roles-every-part-roled: unsupported (claims: roles-every-part-roled-prior)
- roles-four-skills: supported (claims: evaluator-optimizer, skills-lighter-than-always-loaded)
- roles-principle-skill-names: unsupported (claims: roles-principle-skill-names-prior)
- roles-rationale-references-linked: supported (claims: agentskills-progressive-disclosure, skill-body-500-lines, skills-lighter-than-always-loaded)
- roles-principle-routing: unsupported (claims: roles-principle-routing-prior)
- pf-single-title: new (claims: google-single-h1, md025-single-title, md041-title-heading)
- pf-state-why: new (claims: prompting-explain-why, diataxis-explain-why, adr-motivation-lost)
- pf-only-what-the-agent-lacks: new (claims: skill-only-new-context, claude-md-only-what-agent-lacks, cursor-use-a-linter, smallest-high-signal-set, cursor-start-simple)
- pf-summary-what-and-when: new (claims: skill-description-what-and-when, agentskills-metadata-always-loaded)
- pf-history-newest-first: new (claims: changelog-latest-first, changelog-entry-per-version, changelog-dated)
- pf-format-checks-tool-enforced: new (claims: docs-as-code, codex-lint-in-ci, cursor-use-a-linter, claude-md-hooks-for-absolutes, md043-required-headings, json-schema-required, markdownlint-custom-rules-frontmatter, vale-metric-formulas, vale-occurrence, vale-script, agentsmd-any-headings)
- pf-always-loaded-budget: new (claims: claude-md-200-lines, codex-32kib-combined, claude-md-every-line-costs, ifscale-density-degrades, agentskills-metadata-always-loaded)
- pf-key-guidance-first: new (claims: lost-in-the-middle, ifscale-earlier-instructions, ms-first-screen, google-opening-sentence)

Second-check corrections, refuted (criteria 3 applies to these claims):
- adr-motivation-lost: refuted (quote-found yes, supports-claim partly); trust 62 -> 42; a rule citing it cannot carry MUST
- skill-only-new-context: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST
- docs-as-code: refuted (quote-found yes, supports-claim partly); trust 66 -> 46; a rule citing it cannot carry MUST
- md043-required-headings: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST
- vale-metric-formulas: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- ifscale-earlier-instructions: refuted (quote-found yes, supports-claim partly); trust 68 -> 48; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **pf-title-heading** — verdict `unsupported` (claims: pf-title-heading-prior, md041-frontmatter-title-satisfies, md025-frontmatter-title-counts, markdownlint-custom-rules-frontmatter). Prior text, kept word for word: "The first H1 heading MUST match the frontmatter `title` field exactly."
  - against: By default MD041 accepts a front-matter title in place of a first-line H1, so it does not by itself check that an H1 matches the front-matter title.
  - against: With default settings MD025 treats a front-matter title as the H1 and reports any later H1, so a compiled document carrying both a front-matter title and a `# Title` trips it unless front_matter_title is set to an empty string.
  - against: markdownlint custom rules receive the document's lines and its front-matter lines separately, so a custom rule can compare the H1 with the front-matter title or count body lines.
- **pf-statement** — verdict `unsupported` (claims: pf-statement-prior, lead-with-main-point, ms-lead-with-most-important, google-opening-sentence, pep-abstract-short, google-paragraph-length, vale-metric-formulas). Prior text, kept word for word: "A concise statement paragraph MUST appear immediately after the H1 heading. This is the principle's core idea — typically 1-3 sentences."
  - against: Start content with its most important piece of information (the inverted pyramid), so a reader who stops early still gets the main point.
  - against: Microsoft's style guide says to get to the point fast: lead with what matters most and front-load keywords.
  - against: Google's technical-writing course treats the opening sentence as the most important, since busy readers may skip what follows.
  - against: A structured document opens with a short abstract of the issue it addresses; PEP 1 says each PEP should have one of about 200 words.
  - against: Readers welcome paragraphs of three to five sentences and avoid ones of more than about seven.
  - against: Vale's metric check evaluates formulas over built-in counts (words, sentences, paragraphs, lists, headings by level, readability scores), document-wide or per scoped block, so it can bound a statement's sentence count or a body's word count.
- **pf-change-history** — verdict `unsupported` (claims: pf-change-history-prior, changelog-entry-per-version, changelog-dated, md043-required-headings). Prior text, kept word for word: "The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary."
  - against: A change history should have an entry for every version.
  - against: Each version in a change history shows its release date.
  - against: markdownlint MD043 enforces a required heading structure across a set of files, with wildcards for optional sections, so it can require a final `## Change History` heading.
- **pf-brevity** — verdict `unsupported` (claims: pf-brevity-prior, claude-md-200-lines, skill-body-500-lines, agentskills-progressive-disclosure, cursor-rules-500-lines, codex-32kib-combined, copilot-two-pages, ifscale-density-degrades, chroma-context-rot, lost-in-the-middle, context-finite-resource, minimal-not-short, claude-md-line-gets-lost, ms-be-brief, adr-short-record, diataxis-keep-bounded, md013-measures-line-width). Prior text, kept word for word: "Principles SHOULD be concise. The body (excluding frontmatter and Change History) SHOULD NOT exceed ~50 lines. Principles are philosophical anchors, not exhaustive guides — detailed guidance belongs in guidelines."
  - against: Anthropic's Claude Code guidance targets under 200 lines per always-loaded CLAUDE.md file, because longer files consume more context and reduce adherence.
  - against: Anthropic recommends keeping an on-demand SKILL.md body under 500 lines, splitting longer content into separate files.
  - against: The Agent Skills specification loads metadata (~100 tokens) for every skill at startup and the body (under 5000 tokens recommended) only on activation, and moves detailed reference material to separate files.
  - against: Cursor's rule guidance keeps each rule under 500 lines and splits large rules into composable ones.
  - against: OpenAI Codex stops adding instruction files once their combined size reaches 32 KiB by default, so an always-loaded set has a hard total budget.
  - against: GitHub's published prompt for generating Copilot repository instructions limits them to two pages.
  - against: Instruction-following accuracy falls as instruction density grows; even the best frontier models reach only 68% accuracy at 500 simultaneous instructions.
  - against: Across 18 models, performance grows less reliable as input length grows, even on simple tasks.
  - against: Language models use information at the start or end of a long context best and degrade significantly for information in the middle, even long-context models.
  - against: Anthropic's context-engineering guidance treats context as a finite resource with diminishing returns, because recall falls as context grows (context rot).
  - against: Minimal context does not mean short: an instruction still needs enough information up front for the agent to adhere, which is where a hard length cap can hurt.
  - against: When an agent keeps ignoring an instruction that is in its file, emphasis does not fix it: the file has grown long enough that the line gets lost, or the rule belongs in enforcement.
  - against: Microsoft's style guide says to be brief: give just enough to decide confidently and prune every excess word.
  - against: Michael Nygard's architecture decision record, a close analogue of a short principle document, is meant to be one or two pages long.
  - against: Diataxis keeps explanation closely bounded: instruction and technical description belong elsewhere, and letting them in harms the explanation and hides them from their proper place.
  - against: markdownlint's length rule MD013 measures the width of each line, not the length of a document, so a body-length cap needs a custom rule or another tool.
- **roles-vocabulary** — verdict `unsupported` (claims: roles-vocabulary-prior). Prior text, kept word for word: "A part may carry a `role` in `artifact.json`: `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **roles-every-part-roled** — verdict `unsupported` (claims: roles-every-part-roled-prior). Prior text, kept word for word: "A roled artifact gives every other part a role, names each rule in its `rules` parts (`- **kebab-name**: … MUST|SHOULD|MAY …`), and sets no `routes` and no `hosts/`."
- **roles-principle-skill-names** — verdict `unsupported` (claims: roles-principle-skill-names-prior). Prior text, kept word for word: "`principles/t`, which has no use case, keeps its type: `principle-t` and `reviewing-principle-t`." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **roles-principle-routing** — verdict `unsupported` (claims: roles-principle-routing-prior). Prior text, kept word for word: "Each skill has its own description and routes under its own use case, with the artifact's own use case below it (`coding/reviewing/planning/data`; a principle's `coding/reviewing/principles`)." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.

## Open questions

- Which length figure the principle rule should name: the research supports no ~50-line per-principle cap; it supports a budget for everything always loaded (Claude Code's under-200-lines-per-file target) and an on-demand body bound (SKILL.md under 500 lines / under 5000 tokens). Whether principles are always loaded together (then the cap is the shared budget divided across the cookbook's principles, about 45 today) or load on demand as compiled skills (then the skill bound applies) is the owner's to decide.
- Whether pf-frontmatter-complete's field list should match conventions.md's Field Definitions table, which marks approved-by and approved-date as required (written by /approve-artifact, not linted) while the draft list omits them.
- Whether pf-title-heading keeps its exact-match MUST as an internal consistency check (tool-decidable) although no outside source requires it, or is restated as the single-title practice the sources support.
- Whether pf-statement and pf-change-history stay MUST as definitions of the artifact type (internal design) or drop to the SHOULD their outside sources support.
- How a principle's actionable bullets relate to Diataxis, which keeps instruction out of explanation: whether a principle is an explanation page with a short action list, or a separate artifact kind for which Diataxis is not the model.
