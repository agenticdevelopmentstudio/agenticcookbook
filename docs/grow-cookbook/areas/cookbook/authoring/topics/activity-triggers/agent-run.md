# Research fallback run: activity-triggers

The research team could not run (`team_probe.py researchteam`: "missing distributions: PyYAML, aiohttp, mcp, websockets"); one fresh Opus Agent ran the `research` prompt. Its reply, verbatim:

I wrote both research files, and the validator printed `Research passed.`

Files:
- /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/activity-triggers/research/research.json
- /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/activity-triggers/research/research.md

I did not commit them, because the brief said to write exactly two files and edit nothing else.

**Claims per question (115 in total, every one named in a verdict):**

| Question | Total | Research claims | `-prior` claims |
|---|---|---|---|
| best-practices | 35 | 27 | 8 |
| known-solutions | 34 | 29 | 5 |
| platform-guidelines | 24 | 24 | 0 |
| experts-view | 22 | 22 | 0 |

**Verdicts:**
- load-by-activity-not-all, unsupported: load-by-activity-not-all-prior, bp-smallest-high-signal-set, bp-context-rot-recall-falls, bp-no-laundry-list-of-rules, ks-path-rules-save-context, ks-tool-search-accuracy-degrades, ev-lost-in-middle-position, ev-lost-in-middle-below-closed-book, ev-more-docs-marginal, ev-ifscale-instruction-density, ev-chroma-context-rot, ev-rag-mcp-selection-accuracy, ev-rag-mcp-degrades-at-scale, ev-anthropic-tool-search-internal, ev-tool-search-token-reduction
- guideline-declares-activities, unsupported: guideline-declares-activities-prior, ks-claude-path-scoped-rules, ks-skill-description-decides-loading, ks-cursor-rule-types, ks-copilot-path-instructions, ks-openai-metadata-filter, ks-pinecone-metadata-filter, pg-skills-metadata-only-until-triggered
- canonical-trigger-vocabulary, supported: bp-controlled-vocabulary-defined, bp-vocab-control-three-methods, bp-scope-note-states-meaning, bp-controlled-vocab-improves-precision-recall, pg-skos-scope-note, pg-skos-example, pg-iso25964-maintenance, pg-iso25964-skos-compatible
- escalating-checkpoint-pattern, unsupported: escalating-checkpoint-pattern-prior, bp-commit-build-fast, bp-second-stage-build, ks-pre-commit-simple-issues, ks-pre-commit-stages
- principles-always-loaded, unsupported: principles-always-loaded-prior, bp-hybrid-upfront-plus-on-demand, ks-rules-without-paths-load-at-launch, ks-cursor-always-apply, ks-codex-concatenates-root-down, ks-keep-few-tools-non-deferred
- trigger-filtered-on-demand, unsupported: trigger-filtered-on-demand-prior, ks-skill-body-loads-on-use, pg-agent-skills-progressive-disclosure, ks-claude-path-scoped-rules, ks-copilot-path-instructions, ks-cursor-rule-types, ks-agents-md-nearest-file
- pre-commit-checklist, unsupported: pre-commit-checklist-prior, ks-pre-commit-simple-issues, pg-githooks-pre-commit-bypass, bp-commit-build-fast, bp-ten-minute-build
- pre-pr-audit, supported: bp-second-stage-build, pg-githooks-pre-push, pg-github-required-status-checks
- check-cost-proportional-to-stakes, unsupported: check-cost-proportional-to-stakes-prior, bp-commit-build-fast, bp-second-stage-build
- trigger-index-location, unsupported: trigger-index-location-prior
- query-union-of-triggers, supported: ks-openai-metadata-filter, ks-pinecone-in-operator, ks-copilot-instructions-combined
- regenerate-index-after-change, unsupported: regenerate-index-after-change-prior
- trigger-index-not-hand-edited, unsupported: trigger-index-not-hand-edited-prior
- triggers-field-in-meta, supported: ks-claude-path-scoped-rules, ks-copilot-applyto-frontmatter
- one-to-five-triggers, supported: ks-so-five-tag-cap, bp-prune-overused-and-rare-terms
- canonical-values-only, supported: bp-controlled-vocabulary-defined, bp-controlled-vocab-improves-precision-recall, ks-so-favor-existing-tags
- add-trigger-to-guide-first, supported: bp-nominate-candidate-term, bp-editor-reviews-new-terms, ks-so-favor-existing-tags
- order-specific-to-general, unsupported: order-specific-to-general-prior
- triggers-guideline-only, unsupported: triggers-guideline-only-prior
- triggers-empty-until-classified, unsupported: triggers-empty-until-classified-prior
- triggers-from-canonical-taxonomy, supported: bp-controlled-vocabulary-defined, pg-iso25964-maintenance
- trigger-one-meaning-one-label, new: bp-one-meaning-per-term, pg-skos-one-preflabel, bp-controlled-vocabulary-defined
- trigger-scope-note-per-value, new: bp-scope-note-states-meaning, pg-skos-scope-note, pg-skos-definition, pg-skos-example, ev-human-cant-pick-tool
- trigger-values-carry-key-terms, new: pg-skills-description-key-terms, pg-skills-metadata-only-until-triggered, bp-warrant
- trigger-change-history, new: bp-change-record-dated, bp-history-note-records-entry, bp-history-note-succession, pg-skos-history-note, pg-skos-change-note
- rename-keeps-old-value-as-alias, new: bp-rename-use-reference, pg-skos-altlabel-synonyms, pg-skos-hidden-label, ks-so-tag-synonyms-auto-retag
- retire-assesses-impact-and-migrates, new: bp-retire-consider-impact, bp-retained-term-marked, bp-one-for-one-auto-migrate, bp-delete-without-replacement-loses-access
- vocabulary-periodic-review, new: bp-vocabulary-needs-maintenance, bp-maintenance-policies, bp-prune-overused-and-rare-terms, bp-periodic-evaluation
- validate-trigger-values-mechanically, new: pg-skos-open-boundary, pg-unknown-fields-ignored-silently, pg-bad-frontmatter-loads-always
- measure-trigger-selection-with-labelled-tasks, new: ev-test-collection-three-parts, ev-fifty-information-needs, ev-relevance-to-need-not-query, pg-skills-evaluations-first, pg-skills-evaluations-source-of-truth, ks-skill-trigger-eval-set, ks-skill-trigger-train-test-split, ks-plugin-eval-trigger-rate, ev-little-research-vocab-evaluation
- report-recall-and-precision, new: ev-measure-by-recall-precision, ev-recall-defined, ev-precision-defined, ev-recall-precision-inverse, ev-contextual-retrieval-failure-rate, ev-start-with-recall
- fallback-when-tags-miss, new: bp-hybrid-upfront-plus-on-demand, ks-cursor-rule-types, ks-skill-description-decides-loading, ks-skill-undertrigger, ev-indexer-consistency-low
- keep-always-loaded-core-small, new: pg-claude-md-size-adherence, pg-cursor-rules-focused, ks-keep-few-tools-non-deferred, ks-codex-size-limit, ks-skill-listing-costs-every-turn, ks-skill-listing-budget-drops-descriptions
- log-loaded-guidelines, new: pg-instructions-loaded-hook
- filter-only-when-corpus-outgrows-context, new: ev-contextual-retrieval-small-kb-in-prompt, ev-more-docs-marginal

**Main findings:**
- **Numbers:** no source supports any number in the guide (240, 10-20, ~12, 27, ~10).
- **Pre-commit:** calling the pre-commit set "mandatory" is undercut by git's `--no-verify` bypass.
- **New rules:** the research adds rules for:
  - governing the trigger vocabulary
  - checking trigger values with tooling
  - a fallback when tags miss
  - measuring trigger selection by recall and precision against a labelled task set
- **Strengths:** research.md gives the strength the sources support for each unsupported rule and each new rule.
- **For the owner to decide:** six questions are recorded under `open_questions`:
  - what to do with `refactor` and `research`, which are in use but not in the trigger table
  - whether to keep the counts in the guide
  - whether pre-commit stays "mandatory"
  - whether to add a fallback
  - how big the evaluation set should be
  - whether to keep the cap at 5
