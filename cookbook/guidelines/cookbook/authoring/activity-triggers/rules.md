
### Loading by activity

- **load-by-activity-not-all**: An agent SHOULD load guidelines by activity, not all of them: Instead of loading every guideline into context, agents query by activity to get the 10-20 that matter right now. Guidelines are the opposite: numerous, specific, and most are irrelevant to any given task. Loading all of them wastes context and dilutes signal. (claim: load-by-activity-not-all-prior)
- **filter-only-when-corpus-outgrows-context**: A corpus of guidelines small enough to fit in the prompt (Anthropic puts the line at about 200,000 tokens) MAY be loaded whole instead of filtered by trigger, since past a point more loaded documents buy little: 50 retrieved documents instead of 20 improved accuracy only marginally. (claims: ev-contextual-retrieval-small-kb-in-prompt, ev-more-docs-marginal)
- **guideline-declares-activities**: Each guideline SHOULD declare the activities it serves: Triggers solve this. Each guideline declares the activities where it's relevant. An agent about to write tests queries `writing-tests` and gets ~12 guidelines instead of all of them. (claim: guideline-declares-activities-prior)
- **triggers-field-in-meta**: A guideline SHOULD declare its triggers in a `triggers` field of its own frontmatter, after `approved-date`, the way one agent host's rules declare their scope in a `paths` frontmatter field and Copilot instruction files in an `applyTo` frontmatter block. (claims: ks-claude-path-scoped-rules, ks-copilot-applyto-frontmatter)
- **query-union-of-triggers**: An agent MAY query several triggers at once and load the union of the guidelines they return, the same operation as a metadata filter's `in` over a list of values, and as Copilot using every instruction file that applies. (claims: ks-openai-metadata-filter, ks-pinecone-in-operator, ks-copilot-instructions-combined)
- **principles-always-loaded**: Principles SHOULD be the always-loaded tier: **Principles** — always loaded into context. Few, universal, load-bearing. These are the foundation that applies to every task. (claim: principles-always-loaded-prior)
- **keep-always-loaded-core-small**: The always-loaded tier SHOULD hold only what every task needs, with anything that applies only to some work moved to the on-demand tier, because whatever is always loaded adds to the context on every turn, a longer always-loaded file reduces adherence, and hosts cap or cut that tier: one host stops adding AGENTS.md files at 32 KiB by default, and another drops skill descriptions past its listing budget, removing the keywords used to match them. (claims: pg-claude-md-size-adherence, pg-cursor-rules-focused, ks-keep-few-tools-non-deferred, ks-codex-size-limit, ks-skill-listing-costs-every-turn, ks-skill-listing-budget-drops-descriptions)
- **trigger-filtered-on-demand**: Guidelines SHOULD be the on-demand tier: **Trigger-filtered guidelines** — loaded on demand based on current activity. When an agent is about to write tests, it queries `writing-tests` and gets ~12 specific testing guidelines. When it's about to call an API, it queries `api-integration` and gets the relevant networking and security guidelines. (claim: trigger-filtered-on-demand-prior)
- **fallback-when-tags-miss**: Trigger-filtered loading SHOULD have a fallback for a task whose triggers miss a guideline it needs, a selection by description over all guidelines beside the set loaded up front, as Cursor's agent-decided rules and agent skill descriptions select, because people tagging from a controlled vocabulary agree with each other only 27.5-39.5% of the time; selection by description under-triggers too, so neither replaces the other. (claims: bp-hybrid-upfront-plus-on-demand, ks-cursor-rule-types, ks-skill-description-decides-loading, ks-skill-undertrigger, ev-indexer-consistency-low)
- **log-loaded-guidelines**: A loader MAY log which guidelines it loaded for a task, when and why, as an agent host's hook can log which instruction files load, when they load and why. (claim: pg-instructions-loaded-hook)

### Checkpoints

- **escalating-checkpoint-pattern**: Checks SHOULD be staged by checkpoint: The most effective usage is graduated — lightweight guardrails during active work, thorough review at natural checkpoints, the pre-commit checklist and the pre-PR audit below. (claim: escalating-checkpoint-pattern-prior)
- **pre-commit-checklist**: Each commit SHOULD be checked against this set: **Pre-commit checklist** — a small mandatory set (~10 rules) triggered by `pre-commit`. Checked before every commit. Fast, focused, catches common issues. (claim: pre-commit-checklist-prior)
- **pre-pr-audit**: A broader set, triggered by `pre-pr`, SHOULD be checked once before a pull request is opened, more thorough than the commit check and covering testing completeness, accessibility and security headers: a slower second stage after the fast commit stage, run at a later checkpoint such as git's pre-push hook, which can block a push, or as a status check GitHub requires to pass before changes reach a protected branch. (claims: bp-second-stage-build, pg-githooks-pre-push, pg-github-required-status-checks)
- **check-cost-proportional-to-stakes**: A checkpoint MAY spend on checking in step with what is at stake: The cost of checking is proportional to the stakes of the action. (claim: check-cost-proportional-to-stakes-prior)

### The trigger index

- **trigger-index-location**: An agent SHOULD query this one index: The trigger index lives at `cookbook/index/triggers.yaml` (generated by `cookr update`). It lists each guideline by its source folder, relative to `cookbook/`, under each trigger value it declares. (claim: trigger-index-location-prior)
- **regenerate-index-after-change**: The trigger index MUST be regenerated after any trigger change: After adding or modifying guideline triggers, regenerate it with `cookr update`. (claim: regenerate-index-after-change-prior)
- **trigger-index-not-hand-edited**: The trigger index MUST NOT be edited by hand: The index is a generated artifact — do not edit it manually. (claim: trigger-index-not-hand-edited-prior)

### A guideline's triggers

- **canonical-values-only**: Every value in a guideline's `triggers` MUST be a value of the canonical trigger table in `guide/introduction/trigger-guide.md`, so a new value is in that table before any guideline uses it: the table is an explicit list in which every value has a definition, so a value outside it is no part of the controlled vocabulary, whose purpose is better precision and recall in finding guidelines. (claims: bp-controlled-vocabulary-defined, bp-controlled-vocab-improves-precision-recall)
- **triggers-from-canonical-taxonomy**: The `triggers` field MUST take its values from one canonical trigger taxonomy, an explicit list kept by the cookbook as its authority, and from no second list. (claims: bp-controlled-vocabulary-defined, pg-iso25964-maintenance)
- **one-to-five-triggers**: A classified guideline SHOULD carry from one to five triggers, the cap Stack Overflow puts on a question's tags. (claim: ks-so-five-tag-cap)
- **order-specific-to-general**: A guideline SHOULD list its triggers in this order: Order triggers from most specific to least specific. (claim: order-specific-to-general-prior)
- **triggers-guideline-only**: The `triggers` field MUST be carried by guidelines only, as this row of the conventions' field table says: | `triggers` | Guideline only | Activity or context tags that make this guideline relevant to an AI agent. (claim: triggers-guideline-only-prior)
- **triggers-empty-until-classified**: A guideline whose triggers are not yet chosen MAY carry an empty list: Empty list `[]` if not yet classified. (claim: triggers-empty-until-classified-prior)
- **favour-existing-trigger-values**: An author SHOULD use an existing trigger value whenever one covers the activity, and propose a new one only when the nomination states why no existing value covers it. (claims: ks-so-favor-existing-tags, bp-editor-reviews-new-terms)
- **add-trigger-to-guide-first**: When no existing trigger value fits, an author SHOULD nominate a new value as a candidate for the canonical table rather than write an unlisted value into a guideline. (claim: bp-nominate-candidate-term)
- **editor-reviews-candidate-values**: A candidate trigger value SHOULD be reviewed by the vocabulary's editor, preferably an editorial board, including whether an existing value already covers it, before it is admitted to the table. (claim: bp-editor-reviews-new-terms)

### Defining the vocabulary

- **canonical-trigger-vocabulary**: The cookbook SHOULD keep its trigger values as a controlled vocabulary built and maintained as ISO 25964-1 recommends for retrieval thesauri (a standard kept compatible with SKOS): an explicit list in which every value has an unambiguous, non-redundant definition, a scope note stating the meaning chosen for it (when it fires), and examples of its use (example guidelines), controlled by defining each value's scope, linking synonyms to one preferred value and telling homographs apart, because a controlled vocabulary improves both precision and recall in searching, as Z39.19 states without citing a study. (claims: bp-controlled-vocabulary-defined, bp-vocab-control-three-methods, bp-scope-note-states-meaning, bp-controlled-vocab-improves-precision-recall, pg-skos-scope-note, pg-skos-example, pg-iso25964-maintenance, pg-iso25964-skos-compatible)
- **trigger-one-meaning-one-label**: Each trigger value MUST have one and only one meaning. (claim: bp-one-meaning-per-term)
- **trigger-single-canonical-label**: Each trigger value MUST have no more than one canonical label. (claim: pg-skos-one-preflabel)
- **trigger-values-not-redundant**: Two trigger values MUST NOT share a meaning: every value's definition is non-redundant. (claim: bp-controlled-vocabulary-defined)
- **trigger-scope-note-per-value**: Each trigger value SHOULD carry, beside its definition of the complete meaning, a scope note saying how its use is limited. (claims: bp-scope-note-states-meaning, pg-skos-scope-note, pg-skos-definition)
- **overlapping-values-say-which-applies**: Trigger values whose scopes overlap SHOULD each say in their scope notes which one applies, because when a person cannot say which of two options fits a situation, an agent cannot be expected to do better. (claims: bp-scope-note-states-meaning, ev-human-cant-pick-tool)
- **trigger-values-carry-key-terms**: Each trigger value's name and description SHOULD say when it applies in the words of the tasks it serves, chosen on warrant (the language of the guidelines, of the agents and people who use them, and the cookbook's own needs), because until a guideline loads, only that text stands for it in matching. (claims: pg-skills-description-key-terms, pg-skills-metadata-only-until-triggered, bp-warrant)

### Recording changes

- **trigger-change-history**: Each trigger value SHOULD have a history note recording the date it entered the vocabulary. (claim: bp-history-note-records-entry)
- **trigger-change-dated-with-person**: Each addition, modification or deletion of a trigger value SHOULD be recorded with its date and the person responsible for it. (claim: bp-change-record-dated)
- **significant-changes-in-history-note**: A significant change to a trigger value's meaning or form SHOULD be recorded in its history note. (claim: pg-skos-history-note)
- **administrative-changes-in-change-note**: A fine-grained administrative change to a trigger value MAY be recorded in a change note, apart from its history note. (claim: pg-skos-change-note)
- **history-note-records-succession**: A trigger value's history note MAY name the values that preceded or succeeded it. (claim: bp-history-note-succession)

### Renaming and retiring values

- **rename-dated-in-history-note**: When a trigger value is renamed, the date of the rename SHOULD be recorded in its history note. (claim: bp-rename-use-reference)
- **rename-keeps-old-value-as-alias**: A renamed trigger value's old form SHOULD be kept as an alternative label referring to the new one, so the old value still resolves. (claims: bp-rename-use-reference, pg-skos-altlabel-synonyms)
- **old-value-matched-not-shown**: A renamed value's old form MAY be kept as a hidden label, which search and validation still match without the table displaying it. (claim: pg-skos-hidden-label)
- **one-for-one-retag-automatically**: When a trigger value is renamed or replaced one for one, the guidelines carrying the old value MAY be retagged automatically, as tag synonyms retag posts, instead of by hand. (claims: bp-one-for-one-auto-migrate, ks-so-tag-synonyms-auto-retag)
- **retire-assesses-impact-and-migrates**: Before a trigger value is changed or retired, the impact of the change on finding the guidelines already tagged with it MUST be considered. (claim: bp-retire-consider-impact)
- **retired-value-marked-retrieval-only**: A retired trigger value that is kept MUST be marked as kept for retrieval only, and the date of that change in its status MUST be recorded in its history note. (claim: bp-retained-term-marked)
- **retired-value-points-to-successor**: A retired trigger value superseded by a newer value SHOULD carry a cross-reference to its successor. (claim: bp-retained-term-marked)
- **no-delete-without-replacement**: A trigger value SHOULD NOT be deleted while guidelines still carry it unless they are first retagged under a replacement, since deleting a value without replacement indexing reduces access to those guidelines over time. (claims: bp-delete-without-replacement-loses-access, bp-retire-consider-impact)

### Reviewing and validating the vocabulary

- **vocabulary-periodic-review**: The trigger vocabulary SHOULD be maintained under set policies for periodic review, for adding values and for replacing obsolete ones, since a vocabulary is never finished. (claims: bp-vocabulary-needs-maintenance, bp-maintenance-policies)
- **review-tests-the-vocabulary**: Each periodic review of the trigger vocabulary SHOULD test and evaluate it. (claim: bp-periodic-evaluation)
- **review-flags-overused-and-rare-values**: Each periodic review SHOULD count the guidelines carrying each trigger value and treat as a candidate for change or removal every value that the review policy's recorded thresholds mark as overused or as assigned very rarely. (claims: bp-prune-overused-and-rare-terms, bp-maintenance-policies)
- **validate-trigger-values-mechanically**: Tooling SHOULD reject a guideline whose `triggers` holds a value outside the canonical table, because nothing else will: SKOS has no way to close a vocabulary's boundary, and an agent host ignores a frontmatter field it does not know without an error. (claims: pg-skos-open-boundary, pg-unknown-fields-ignored-silently)
- **reject-unparseable-frontmatter**: Tooling SHOULD reject a guideline whose frontmatter does not parse, because an agent host can load a rule whose frontmatter does not parse as if it had no scope. (claims: pg-bad-frontmatter-loads-always, pg-unknown-fields-ignored-silently)

### Measuring selection

- **measure-trigger-selection-with-labelled-tasks**: Trigger selection SHOULD be measured against a test collection of three parts: the guidelines, a set of tasks (a mix that should and should not load a given guideline), and for each task the guidelines it needs, judged against the task and not against the trigger word; little published work tests controlled vocabularies, so the cookbook builds its own set. (claims: ev-test-collection-three-parts, ev-relevance-to-need-not-query, ks-skill-trigger-eval-set, ev-little-research-vocab-evaluation)
- **task-set-size-reference-point**: The labelled task set's size SHOULD be weighed against the IR rule of thumb that 50 information needs has usually been found a sufficient minimum; the size the cookbook adopts is the owner's to set. (claim: ev-fifty-information-needs)
- **evaluation-before-trigger-text**: The selection evaluation SHOULD be built before the trigger values and scope notes it tests are written. (claim: pg-skills-evaluations-first)
- **evaluation-is-source-of-truth**: Whether trigger selection works SHOULD be judged by the selection evaluation, as its source of truth. (claim: pg-skills-evaluations-source-of-truth)
- **hold-out-part-of-task-set**: Part of the labelled task set SHOULD be held out from any tuning of trigger values or scope notes. (claim: ks-skill-trigger-train-test-split)
- **repeat-runs-for-a-rate**: Each task MAY be run several times to get a selection rate. (claims: ks-skill-trigger-train-test-split, ks-plugin-eval-trigger-rate)
- **report-recall-and-precision**: A selection evaluation SHOULD report recall (whether every guideline a task needs was loaded) and precision (whether only guidelines it needs were loaded), or the failure rate 1 minus recall@k in place of recall. (claims: ev-measure-by-recall-precision, ev-recall-defined, ev-precision-defined, ev-contextual-retrieval-failure-rate)
- **tune-recall-first**: Tuning trigger selection SHOULD raise recall first and then improve precision, because the two usually move in opposite directions. (claims: ev-recall-precision-inverse, ev-start-with-recall)

