# Write brief: activity-triggers

Today is 2026-11-21.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/activity-triggers (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/activity-triggers/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/activity-triggers/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/activity-triggers/owner-list.md.
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
- load-by-activity-not-all: unsupported (claims: load-by-activity-not-all-prior, bp-smallest-high-signal-set, bp-context-rot-recall-falls, bp-no-laundry-list-of-rules, ks-path-rules-save-context, ks-tool-search-accuracy-degrades, ev-lost-in-middle-position, ev-lost-in-middle-below-closed-book, ev-more-docs-marginal, ev-ifscale-instruction-density, ev-chroma-context-rot, ev-rag-mcp-selection-accuracy, ev-rag-mcp-degrades-at-scale, ev-anthropic-tool-search-internal, ev-tool-search-token-reduction)
- guideline-declares-activities: unsupported (claims: guideline-declares-activities-prior, ks-claude-path-scoped-rules, ks-skill-description-decides-loading, ks-cursor-rule-types, ks-copilot-path-instructions, ks-openai-metadata-filter, ks-pinecone-metadata-filter, pg-skills-metadata-only-until-triggered)
- canonical-trigger-vocabulary: supported (claims: bp-controlled-vocabulary-defined, bp-vocab-control-three-methods, bp-scope-note-states-meaning, bp-controlled-vocab-improves-precision-recall, pg-skos-scope-note, pg-skos-example, pg-iso25964-maintenance, pg-iso25964-skos-compatible)
- escalating-checkpoint-pattern: unsupported (claims: escalating-checkpoint-pattern-prior, bp-commit-build-fast, bp-second-stage-build, ks-pre-commit-simple-issues, ks-pre-commit-stages)
- principles-always-loaded: unsupported (claims: principles-always-loaded-prior, bp-hybrid-upfront-plus-on-demand, ks-rules-without-paths-load-at-launch, ks-cursor-always-apply, ks-codex-concatenates-root-down, ks-keep-few-tools-non-deferred)
- trigger-filtered-on-demand: unsupported (claims: trigger-filtered-on-demand-prior, ks-skill-body-loads-on-use, pg-agent-skills-progressive-disclosure, ks-claude-path-scoped-rules, ks-copilot-path-instructions, ks-cursor-rule-types, ks-agents-md-nearest-file)
- pre-commit-checklist: unsupported (claims: pre-commit-checklist-prior, ks-pre-commit-simple-issues, pg-githooks-pre-commit-bypass, bp-commit-build-fast, bp-ten-minute-build)
- pre-pr-audit: supported (claims: bp-second-stage-build, pg-githooks-pre-push, pg-github-required-status-checks)
- check-cost-proportional-to-stakes: unsupported (claims: check-cost-proportional-to-stakes-prior, bp-commit-build-fast, bp-second-stage-build)
- trigger-index-location: unsupported (claims: trigger-index-location-prior)
- query-union-of-triggers: supported (claims: ks-openai-metadata-filter, ks-pinecone-in-operator, ks-copilot-instructions-combined)
- regenerate-index-after-change: unsupported (claims: regenerate-index-after-change-prior)
- trigger-index-not-hand-edited: unsupported (claims: trigger-index-not-hand-edited-prior)
- triggers-field-in-meta: supported (claims: ks-claude-path-scoped-rules, ks-copilot-applyto-frontmatter)
- one-to-five-triggers: supported (claims: ks-so-five-tag-cap, bp-prune-overused-and-rare-terms)
- canonical-values-only: supported (claims: bp-controlled-vocabulary-defined, bp-controlled-vocab-improves-precision-recall, ks-so-favor-existing-tags)
- add-trigger-to-guide-first: supported (claims: bp-nominate-candidate-term, bp-editor-reviews-new-terms, ks-so-favor-existing-tags)
- order-specific-to-general: unsupported (claims: order-specific-to-general-prior)
- triggers-guideline-only: unsupported (claims: triggers-guideline-only-prior)
- triggers-empty-until-classified: unsupported (claims: triggers-empty-until-classified-prior)
- triggers-from-canonical-taxonomy: supported (claims: bp-controlled-vocabulary-defined, pg-iso25964-maintenance)
- trigger-one-meaning-one-label: new (claims: bp-one-meaning-per-term, pg-skos-one-preflabel, bp-controlled-vocabulary-defined)
- trigger-scope-note-per-value: new (claims: bp-scope-note-states-meaning, pg-skos-scope-note, pg-skos-definition, pg-skos-example, ev-human-cant-pick-tool)
- trigger-values-carry-key-terms: new (claims: pg-skills-description-key-terms, pg-skills-metadata-only-until-triggered, bp-warrant)
- trigger-change-history: new (claims: bp-change-record-dated, bp-history-note-records-entry, bp-history-note-succession, pg-skos-history-note, pg-skos-change-note)
- rename-keeps-old-value-as-alias: new (claims: bp-rename-use-reference, pg-skos-altlabel-synonyms, pg-skos-hidden-label, ks-so-tag-synonyms-auto-retag)
- retire-assesses-impact-and-migrates: new (claims: bp-retire-consider-impact, bp-retained-term-marked, bp-one-for-one-auto-migrate, bp-delete-without-replacement-loses-access)
- vocabulary-periodic-review: new (claims: bp-vocabulary-needs-maintenance, bp-maintenance-policies, bp-prune-overused-and-rare-terms, bp-periodic-evaluation)
- validate-trigger-values-mechanically: new (claims: pg-skos-open-boundary, pg-unknown-fields-ignored-silently, pg-bad-frontmatter-loads-always)
- measure-trigger-selection-with-labelled-tasks: new (claims: ev-test-collection-three-parts, ev-fifty-information-needs, ev-relevance-to-need-not-query, pg-skills-evaluations-first, pg-skills-evaluations-source-of-truth, ks-skill-trigger-eval-set, ks-skill-trigger-train-test-split, ks-plugin-eval-trigger-rate, ev-little-research-vocab-evaluation)
- report-recall-and-precision: new (claims: ev-measure-by-recall-precision, ev-recall-defined, ev-precision-defined, ev-recall-precision-inverse, ev-contextual-retrieval-failure-rate, ev-start-with-recall)
- fallback-when-tags-miss: new (claims: bp-hybrid-upfront-plus-on-demand, ks-cursor-rule-types, ks-skill-description-decides-loading, ks-skill-undertrigger, ev-indexer-consistency-low)
- keep-always-loaded-core-small: new (claims: pg-claude-md-size-adherence, pg-cursor-rules-focused, ks-keep-few-tools-non-deferred, ks-codex-size-limit, ks-skill-listing-costs-every-turn, ks-skill-listing-budget-drops-descriptions)
- log-loaded-guidelines: new (claims: pg-instructions-loaded-hook)
- filter-only-when-corpus-outgrows-context: new (claims: ev-contextual-retrieval-small-kb-in-prompt, ev-more-docs-marginal)

Second-check corrections, refuted (criteria 3 applies to these claims):
- pg-skos-definition: refuted (quote-found yes, supports-claim partly); trust 88 -> 68; a rule citing it cannot carry MUST
- pg-skos-altlabel-synonyms: refuted (quote-found yes, supports-claim partly); trust 88 -> 68; a rule citing it cannot carry MUST
- pg-skos-hidden-label: refuted (quote-found yes, supports-claim partly); trust 88 -> 68; a rule citing it cannot carry MUST
- pg-bad-frontmatter-loads-always: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST
- ks-skill-trigger-train-test-split: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST
- ks-plugin-eval-trigger-rate: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST
- ev-contextual-retrieval-failure-rate: refuted (quote-found yes, supports-claim partly); trust 60 -> 40; a rule citing it cannot carry MUST
- ev-start-with-recall: refuted (quote-found yes, supports-claim partly); trust 68 -> 48; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **load-by-activity-not-all** — verdict `unsupported` (claims: load-by-activity-not-all-prior, bp-smallest-high-signal-set, bp-context-rot-recall-falls, bp-no-laundry-list-of-rules, ks-path-rules-save-context, ks-tool-search-accuracy-degrades, ev-lost-in-middle-position, ev-lost-in-middle-below-closed-book, ev-more-docs-marginal, ev-ifscale-instruction-density, ev-chroma-context-rot, ev-rag-mcp-selection-accuracy, ev-rag-mcp-degrades-at-scale, ev-anthropic-tool-search-internal, ev-tool-search-token-reduction). Prior text, kept word for word: "Instead of loading all 240 guidelines into context, agents query by activity to get the 10-20 that matter right now.

Guidelines are the opposite: numerous, specific, and most are irrelevant to any given task. Loading all of them wastes context and dilutes signal." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Current context-engineering practice is to put the smallest set of high-signal tokens in front of the model, not everything that might apply.
  - against: Recall of information in the context falls as the number of tokens in the context grows, which is the reason to load fewer guidelines.
  - against: Stuffing every rule and edge case into the prompt is discouraged; rules should be selected, not accumulated.
  - against: Claude Code scopes rules so they load only when relevant, stating the aim as reducing noise and saving context.
  - against: Anthropic's tool search loads a focused set of tools on demand because selection accuracy degrades past 30-50 available tools.
  - against: Peer-reviewed evaluation shows models do not use long contexts robustly: performance drops when the relevant item sits in the middle of many documents (2,655 NaturalQuestions queries, 10-30 document contexts, accuracy).
  - against: Adding documents can make results worse than adding none: with the relevant document mid-context, GPT-3.5-Turbo scored below its closed-book 56.1%.
  - against: Retrieving 50 documents instead of 20 improved accuracy only about 1-1.5 points: past a point, more loaded material buys little.
  - against: Instruction-following accuracy falls as the number of simultaneous instructions rises: on 500 keyword-inclusion instructions, 20 models from seven providers, the best reached 68%.
  - against: Across 18 current models, performance grows less reliable as input length grows, even on simple tasks.
  - against: Retrieving a small relevant subset of tools before the model chooses tripled tool-selection accuracy and halved prompt tokens on an MCPBench web-search subset (20 trials).
  - against: Retrieval-based selection itself loses precision as the registry grows into the thousands, so filtering is not a free lunch.
  - against: Anthropic reports large accuracy gains from on-demand tool loading over large libraries (Opus 4: 49% to 74%), from internal testing with no disclosed sample.
  - against: Anthropic reports an 85% token reduction from deferring tool definitions, again from its own configuration without a disclosed method.
- **guideline-declares-activities** — verdict `unsupported` (claims: guideline-declares-activities-prior, ks-claude-path-scoped-rules, ks-skill-description-decides-loading, ks-cursor-rule-types, ks-copilot-path-instructions, ks-openai-metadata-filter, ks-pinecone-metadata-filter, pg-skills-metadata-only-until-triggered). Prior text, kept word for word: "Triggers solve this. Each guideline declares the activities where it's relevant. An agent about to write tests queries `writing-tests` and gets ~12 guidelines instead of 240." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Claude Code rules declare in YAML frontmatter (`paths`) where they apply and load only when Claude works with matching files: a per-item declaration of relevance, keyed on files rather than activities.
  - against: Claude Code selects skills by matching the task against each skill's free-text description, not against a closed tag vocabulary; the description must state when to use the skill.
  - against: Cursor offers four activation modes for a rule: always, agent-decided by description, by file pattern, and manual mention; selection by description is the fallback that tag-only filtering lacks.
  - against: GitHub Copilot applies path-specific instruction files only to requests about matching files.
  - against: OpenAI file search filters retrieved files by metadata attributes, including an `in` filter over a list of values: tag filtering with a multi-value query.
  - against: Vector databases attach key-value metadata to documents and restrict search to documents whose metadata matches a filter.
  - against: Until a skill is triggered, only its name and description occupy context; the description is matched against the request and must say what the skill does and when to use it.
- **escalating-checkpoint-pattern** — verdict `unsupported` (claims: escalating-checkpoint-pattern-prior, bp-commit-build-fast, bp-second-stage-build, ks-pre-commit-simple-issues, ks-pre-commit-stages). Prior text, kept word for word: "The most effective usage is graduated — lightweight guardrails during active work, thorough review at natural checkpoints:" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: The check run on every commit is kept fast at the price of catching fewer bugs; the balance between speed and bug finding is deliberate.
  - against: A slower, broader second-stage check runs after the fast commit check, covering end-to-end behaviour the commit stage skips.
  - against: Commit-time hooks are meant for simple issues, run on every commit, so that reviewers can spend their attention on architecture.
  - against: The pre-commit framework assigns checks to stages (commit, push), so heavier checks can run at a later checkpoint.
- **principles-always-loaded** — verdict `unsupported` (claims: principles-always-loaded-prior, bp-hybrid-upfront-plus-on-demand, ks-rules-without-paths-load-at-launch, ks-cursor-always-apply, ks-codex-concatenates-root-down, ks-keep-few-tools-non-deferred). Prior text, kept word for word: "**Principles** — always loaded into context. Small (27 items), universal, load-bearing. These are the foundation that applies to every task." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: A hybrid of a small set loaded up front plus on-demand retrieval at the agent's discretion is a recognised pattern, the shape of always-loaded principles plus trigger-filtered guidelines.
  - against: Claude Code rules with no scope load at launch, the equivalent of an always-loaded tier.
  - against: A Cursor rule marked alwaysApply is included in every session regardless of globs or description: an explicit always-loaded tier.
  - against: Codex loads AGENTS.md files before any work, concatenating them from the root down: a static, always-loaded layer rather than activity filtering.
  - against: Tool search keeps a small core (3-5 most-used tools) always loaded and defers the rest: the two-tier shape of always-loaded principles plus on-demand guidelines.
- **trigger-filtered-on-demand** — verdict `unsupported` (claims: trigger-filtered-on-demand-prior, ks-skill-body-loads-on-use, pg-agent-skills-progressive-disclosure, ks-claude-path-scoped-rules, ks-copilot-path-instructions, ks-cursor-rule-types, ks-agents-md-nearest-file). Prior text, kept word for word: "**Trigger-filtered guidelines** — loaded on demand based on current activity. When an agent is about to write tests, it queries `writing-tests` and gets ~12 specific testing guidelines. When it's about to call an API, it queries `api-integration` and gets the relevant networking and security guidelines." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: A Claude Code skill's body loads only when it is used, so long reference material costs almost nothing until needed: on-demand loading of a rule body.
  - against: Anthropic's Agent Skills guidance is progressive disclosure: load information in stages as needed rather than up front.
  - against: Claude Code rules declare in YAML frontmatter (`paths`) where they apply and load only when Claude works with matching files: a per-item declaration of relevance, keyed on files rather than activities.
  - against: GitHub Copilot applies path-specific instruction files only to requests about matching files.
  - against: Cursor offers four activation modes for a rule: always, agent-decided by description, by file pattern, and manual mention; selection by description is the fallback that tag-only filtering lacks.
  - against: AGENTS.md scopes instructions by directory: agents read the nearest file, so each subproject carries its own instructions.
- **pre-commit-checklist** — verdict `unsupported` (claims: pre-commit-checklist-prior, ks-pre-commit-simple-issues, pg-githooks-pre-commit-bypass, bp-commit-build-fast, bp-ten-minute-build). Prior text, kept word for word: "**Pre-commit checklist** — a small mandatory set (~10 rules) triggered by `pre-commit`. Checked before every commit. Fast, focused, catches common issues." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Commit-time hooks are meant for simple issues, run on every commit, so that reviewers can spend their attention on architecture.
  - against: Git's pre-commit hook can be bypassed with --no-verify, so a pre-commit check is not mandatory in fact.
  - against: The check run on every commit is kept fast at the price of catching fewer bugs; the balance between speed and bug finding is deliberate.
  - against: The commit-stage check is bounded by time (the XP ten-minute guideline), not by a count of rules.
- **check-cost-proportional-to-stakes** — verdict `unsupported` (claims: check-cost-proportional-to-stakes-prior, bp-commit-build-fast, bp-second-stage-build). Prior text, kept word for word: "The cost of checking is proportional to the stakes of the action." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: The check run on every commit is kept fast at the price of catching fewer bugs; the balance between speed and bug finding is deliberate.
  - against: A slower, broader second-stage check runs after the fast commit check, covering end-to-end behaviour the commit stage skips.
- **trigger-index-location** — verdict `unsupported` (claims: trigger-index-location-prior). Prior text, kept word for word: "The trigger index lives at `cookbook/index/triggers.yaml` (generated by `cookr update`). It lists each guideline by its source folder, relative to `cookbook/`:" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **regenerate-index-after-change** — verdict `unsupported` (claims: regenerate-index-after-change-prior). Prior text, kept word for word: "After adding or modifying guideline triggers, regenerate:" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **trigger-index-not-hand-edited** — verdict `unsupported` (claims: trigger-index-not-hand-edited-prior). Prior text, kept word for word: "The index is a generated artifact — do not edit it manually." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **order-specific-to-general** — verdict `unsupported` (claims: order-specific-to-general-prior). Prior text, kept word for word: "Order triggers from most specific to least specific." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **triggers-guideline-only** — verdict `unsupported` (claims: triggers-guideline-only-prior). Prior text, kept word for word: "| `triggers` | Guideline only | Activity or context tags that make this guideline relevant to an AI agent." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **triggers-empty-until-classified** — verdict `unsupported` (claims: triggers-empty-until-classified-prior). Prior text, kept word for word: "Empty list `[]` if not yet classified." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.

## Open questions

- Whether `refactor` (17 guidelines) and `research` (10 guidelines), in use at the base commit but absent from the canonical table, are nominated and added to the table or migrated to existing values; the governance verdicts give the procedure, not the outcome.
- Whether the guide keeps any counts (240 guidelines, 10-20 per query, ~12 for writing-tests, 27 principles, ~10 pre-commit rules): no source supports them and the cookbook's own state has outgrown them, so the owner decides between generated counts, ranges measured by an evaluation, or no numbers.
- Whether the pre-commit set stays 'mandatory' when git lets every pre-commit hook be bypassed with --no-verify, or whether the mandatory gate moves to a check the agent cannot skip (a required status check on the pull request).
- Whether trigger-filtered loading gets a fallback (a description- or keyword-based search over all guidelines, as Cursor's Apply Intelligently, Claude Code skill descriptions and the tool search tool do) for tasks whose tags miss a guideline, and how far the cookbook trades precision for recall there.
- What size of labelled task set the cookbook adopts to measure trigger selection: IIR's rule of thumb is 50 information needs, skill-creator uses 20 queries split 60/40; the owner sets the number and the recall target.
- Whether the 1-5 cap stays as is: Stack Overflow caps a question at 5 tags, while at the base commit no guideline carries more than 4 triggers; the owner decides whether the cap is 5, 4 or a soft warning.

## Round 1 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

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

Lint failed (`lint: fail 1`): fix each lint error in the draft. The review's `## Lint` section:

````
/lint-artifact on `cookbook/guidelines/cookbook/authoring/activity-triggers` (guideline, `guideline-formatting.md`), with cookr run as given:

| Check | Result |
|---|---|
| FM-01 to FM-11a | PASS. The frontmatter is complete, the id matches `cookbook/index.json`, the links resolve, and the H1 matches the title. |
| FM-12 | PASS. Change History has one row. |
| FM-13 | PASS. No placeholder text. |
| gf-summary-statement | PASS |
| gf-structured-guidance | PASS |
| gf-rfc-keywords | PASS |
| gf-roled-parts | PASS. All required roles are present and the build bar matches the rules. |
| gf-named-rules | PASS |
| gf-research-folder | PASS |
| gf-rule-cites-research | PASS |
| gf-triggers-field | PASS. `recipe-authoring`, `skill-authoring` |
| gf-compliance-section | PASS. The section is optional and absent. |
| Owner-decides | WARN. 13 rules cite `*-prior` claims under `unsupported` verdicts. These are the owner's to decide and are not an error. |
| Neutrality | FAIL. The folder is `unlisted` for `claude` and `codex`. See Findings. |

Pass: 12 | Warn: 1 | Fail: 1

lint: fail 1
````
