---
id: 1b7b83f9-3b8a-46f7-81b7-9a55291a23a2
title: "Activity Triggers"
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-21
modified: 2026-11-21
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Guideline triggers: a closed, governed vocabulary of activities, tiered on-demand loading, the trigger index, and measuring selection by recall and precision."
platforms: []
tags:
  - triggers
  - controlled-vocabulary
  - context-loading
  - guidelines
depends-on: []
related:
  - 0f999db4-956a-4124-a142-367b1a570983
  - 456f23bd-4523-47e8-9541-073ac046f2ad
references:
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://groups.niso.org/higherlogic/ws/public/download/6484/Guidelines%20for%20the%20Construction,%20Format,%20and%20Management%20of%20Monolingual%20Controlled%20Vocabularies.pdf
  - https://martinfowler.com/articles/continuousIntegration.html
  - https://code.claude.com/docs/en/memory
  - https://code.claude.com/docs/en/skills
  - https://cursor.com/docs/context/rules
  - https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
  - https://agents.md/
  - https://developers.openai.com/codex/guides/agents-md
  - https://platform.openai.com/docs/guides/tools-file-search
  - https://docs.pinecone.io/guides/search/filter-by-metadata
  - https://docs.claude.com/en/docs/agents-and-tools/tool-use/tool-search-tool
  - https://pre-commit.com/
  - https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md
  - https://stackoverflow.com/help/tagging
  - https://stackoverflow.com/help/privileges/create-tags
  - https://stackoverflow.com/help/privileges/suggest-tag-synonyms
  - https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
  - https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
  - https://www.w3.org/TR/skos-reference/
  - https://www.w3.org/TR/skos-primer/
  - https://www.niso.org/schemas/iso25964
  - https://git-scm.com/docs/githooks
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
  - https://arxiv.org/abs/2307.03172
  - https://arxiv.org/abs/2507.11538
  - https://research.trychroma.com/context-rot
  - https://arxiv.org/abs/2505.03275
  - https://www.anthropic.com/engineering/advanced-tool-use
  - https://www.anthropic.com/news/contextual-retrieval
  - https://wiki.eecs.yorku.ca/course_archive/2013-14/W/6339/_media/08eval.pdf
  - https://informationr.net/ir/16-4/paper502.html
approved-by: ""
approved-date: ""
triggers:
  - recipe-authoring
  - skill-authoring
---

# Activity Triggers

Tag each guideline with the activities it serves, using only values from the cookbook's closed trigger vocabulary, so an agent loads the guidelines its current activity needs on top of a small always-loaded core. Govern that vocabulary as a thesaurus is governed (one meaning per value, a scope note, a dated history, an alias on rename, an impact check on retirement), reject unlisted values with tooling, and measure trigger selection against labelled tasks by recall and precision.

## Rules

### Loading by activity

- **load-by-activity-not-all**: An agent SHOULD load guidelines by activity, not all of them: Instead of loading all 240 guidelines into context, agents query by activity to get the 10-20 that matter right now. Guidelines are the opposite: numerous, specific, and most are irrelevant to any given task. Loading all of them wastes context and dilutes signal. (claim: load-by-activity-not-all-prior)
- **filter-only-when-corpus-outgrows-context**: A corpus of guidelines small enough to fit in the prompt (Anthropic puts the line at about 200,000 tokens) MAY be loaded whole instead of filtered by trigger, since past a point more loaded documents buy little: 50 retrieved documents instead of 20 improved accuracy only marginally. (claims: ev-contextual-retrieval-small-kb-in-prompt, ev-more-docs-marginal)
- **guideline-declares-activities**: Each guideline SHOULD declare the activities it serves: Triggers solve this. Each guideline declares the activities where it's relevant. An agent about to write tests queries `writing-tests` and gets ~12 guidelines instead of 240. (claim: guideline-declares-activities-prior)
- **triggers-field-in-meta**: A guideline SHOULD declare its triggers in a `triggers` field of its own frontmatter, after `approved-date`, the way one agent host's rules declare their scope in a `paths` frontmatter field and Copilot instruction files in an `applyTo` frontmatter block. (claims: ks-claude-path-scoped-rules, ks-copilot-applyto-frontmatter)
- **query-union-of-triggers**: An agent MAY query several triggers at once and load the union of the guidelines they return, the same operation as a metadata filter's `in` over a list of values, and as Copilot using every instruction file that applies. (claims: ks-openai-metadata-filter, ks-pinecone-in-operator, ks-copilot-instructions-combined)
- **principles-always-loaded**: Principles SHOULD be the always-loaded tier: **Principles** — always loaded into context. Small (27 items), universal, load-bearing. These are the foundation that applies to every task. (claim: principles-always-loaded-prior)
- **keep-always-loaded-core-small**: The always-loaded tier SHOULD hold only what every task needs, with anything that applies only to some work moved to the on-demand tier, because whatever is always loaded adds to the context on every turn, a longer always-loaded file reduces adherence, and hosts cap or cut that tier: one host stops adding AGENTS.md files at 32 KiB by default, and another drops skill descriptions past its listing budget, removing the keywords used to match them. (claims: pg-claude-md-size-adherence, pg-cursor-rules-focused, ks-keep-few-tools-non-deferred, ks-codex-size-limit, ks-skill-listing-costs-every-turn, ks-skill-listing-budget-drops-descriptions)
- **trigger-filtered-on-demand**: Guidelines SHOULD be the on-demand tier: **Trigger-filtered guidelines** — loaded on demand based on current activity. When an agent is about to write tests, it queries `writing-tests` and gets ~12 specific testing guidelines. When it's about to call an API, it queries `api-integration` and gets the relevant networking and security guidelines. (claim: trigger-filtered-on-demand-prior)
- **fallback-when-tags-miss**: Trigger-filtered loading SHOULD have a fallback for a task whose triggers miss a guideline it needs, a selection by description over all guidelines beside the set loaded up front, as Cursor's agent-decided rules and agent skill descriptions select, because people tagging from a controlled vocabulary agree with each other only 27.5-39.5% of the time; selection by description under-triggers too, so neither replaces the other. (claims: bp-hybrid-upfront-plus-on-demand, ks-cursor-rule-types, ks-skill-description-decides-loading, ks-skill-undertrigger, ev-indexer-consistency-low)
- **log-loaded-guidelines**: A loader MAY log which guidelines it loaded for a task, when and why, as an agent host's hook can log which instruction files load, when they load and why. (claim: pg-instructions-loaded-hook)

### Checkpoints

- **escalating-checkpoint-pattern**: Checks SHOULD be staged by checkpoint: The most effective usage is graduated — lightweight guardrails during active work, thorough review at natural checkpoints: (claim: escalating-checkpoint-pattern-prior)
- **pre-commit-checklist**: Each commit SHOULD be checked against this set: **Pre-commit checklist** — a small mandatory set (~10 rules) triggered by `pre-commit`. Checked before every commit. Fast, focused, catches common issues. (claim: pre-commit-checklist-prior)
- **pre-pr-audit**: A broader set, triggered by `pre-pr`, SHOULD be checked once before a pull request is opened, more thorough than the commit check and covering testing completeness, accessibility and security headers: a slower second stage after the fast commit stage, run at a later checkpoint such as git's pre-push hook, which can block a push, or as a status check GitHub requires to pass before changes reach a protected branch. (claims: bp-second-stage-build, pg-githooks-pre-push, pg-github-required-status-checks)
- **check-cost-proportional-to-stakes**: A checkpoint MAY spend on checking in step with what is at stake: The cost of checking is proportional to the stakes of the action. (claim: check-cost-proportional-to-stakes-prior)

### The trigger index

- **trigger-index-location**: An agent SHOULD query this one index: The trigger index lives at `cookbook/index/triggers.yaml` (generated by `cookr update`). It lists each guideline by its source folder, relative to `cookbook/`: (claim: trigger-index-location-prior)
- **regenerate-index-after-change**: The trigger index MUST be regenerated after any trigger change: After adding or modifying guideline triggers, regenerate: (claim: regenerate-index-after-change-prior)
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
- **evaluation-before-trigger-text**: The selection evaluation SHOULD be built before the trigger values and scope notes it tests are written. (claim: pg-skills-evaluations-first)
- **evaluation-is-source-of-truth**: Whether trigger selection works SHOULD be judged by the selection evaluation, as its source of truth. (claim: pg-skills-evaluations-source-of-truth)
- **hold-out-part-of-task-set**: Part of the labelled task set SHOULD be held out from any tuning of trigger values or scope notes. (claim: ks-skill-trigger-train-test-split)
- **repeat-runs-for-a-rate**: Each task MAY be run several times to get a selection rate. (claims: ks-skill-trigger-train-test-split, ks-plugin-eval-trigger-rate)
- **report-recall-and-precision**: A selection evaluation SHOULD report recall (whether every guideline a task needs was loaded) and precision (whether only guidelines it needs were loaded), or the failure rate 1 minus recall@k in place of recall. (claims: ev-measure-by-recall-precision, ev-recall-defined, ev-precision-defined, ev-contextual-retrieval-failure-rate)
- **tune-recall-first**: Tuning trigger selection SHOULD raise recall first and then improve precision, because the two usually move in opposite directions. (claims: ev-recall-precision-inverse, ev-start-with-recall)

## Adding triggers to a guideline

1. Read the canonical trigger table in `guide/introduction/trigger-guide.md` and each value's scope note. Pick the values whose scope covers the activities the guideline serves, from one to five.
2. If no value fits, do not invent one in the guideline. Nominate a candidate value with a definition, a scope note, examples, the task words it should match and why no existing value covers it; it reaches a guideline only after the editor has reviewed it and it is in the table.
3. Write the values in the guideline's `triggers` field, after `approved-date`, most specific first. A guideline whose triggers are not chosen yet carries `[]`.
4. Regenerate the trigger index with `cookr update`. Never edit `cookbook/index/triggers.yaml` by hand.

## Changing the vocabulary

- **Add**: nominate the value, have the editor review it, record its date of entry and the person responsible in its history note, then add it to the table.
- **Rename**: record the rename's date in the history note, keep the old value as an alternative label referring to the new one (a hidden label if it should not show in the table), and retag the guidelines that carry it, automatically where tooling allows.
- **Retire**: list the guidelines tagged with the value and judge what retiring it does to finding them. Retag them under the successor (automatically for a one-for-one replacement), or keep the old value marked "for retrieval only", record the date of that change in its history note, and cross-reference its successor. Do not delete a value that guidelines still carry until they are retagged under a replacement.
- **Review**: on the review policy's schedule, count how many guidelines carry each value, treat each value the policy's recorded thresholds mark as overused or rarely assigned as a candidate for change or removal, and re-run the selection evaluation.

## Measuring selection

1. Build the test collection before writing the trigger values and scope notes it tests: the guidelines, a set of tasks, and for each task the guidelines it needs, judged by reading the task, not the trigger word. Include tasks that should not load a given guideline. IIR's rule of thumb is a minimum of 50 information needs; skill-creator uses 20 queries. The size the cookbook uses is the owner's to set.
2. Hold part of the set out from any tuning of values or scope notes.
3. Run each task's selection (several times where selection is not deterministic) and compare the guidelines loaded with the guidelines needed.
4. Report recall and precision per task and overall. Tune for recall first, then precision.

## Examples

A guideline's triggers, in its meta, most specific first (`schema-design` is a part of `database-operations`, and `performance-optimization` also covers rendering):

```yaml
triggers:
  - schema-design
  - database-operations
  - performance-optimization
```

An agent that is about to write tests for an API client queries two triggers at once and loads the union:

```text
writing-tests ∪ api-integration  →  every guideline tagged with either value
```

A rename kept resolvable (a sketch, in SKOS terms):

```text
prefLabel:   ui-implementation
altLabel:    ui-work            (old value; still resolves to the new one)
historyNote: 2026-11-21 renamed from ui-work
```

## What a reviewer looks for

- A `triggers` value that is not in the canonical table in `guide/introduction/trigger-guide.md`.
- A new value proposed with no stated reason why no existing value covers the activity, or admitted with no editor's review.
- A classified guideline with more than five triggers or none.
- Triggers not ordered from most specific to least specific.
- A `triggers` field on an artifact that is not a guideline.
- A hand edit to `cookbook/index/triggers.yaml`, or a trigger change committed without the index regenerated.
- A vocabulary value with no definition, no scope note or no example; a value with two meanings or two canonical labels; two values with one meaning; overlapping values whose scope notes do not say which applies.
- A value's description that does not use the words of the tasks it serves.
- A value with no history note giving its date of entry, or a change recorded with no date or no person responsible.
- A rename with no date in the history note, or one that drops the old value instead of keeping it as an alternative label.
- A change or retirement made with no look at the guidelines tagged with the value; a kept retired value not marked for retrieval only, or with no dated status change; a superseded value with no cross-reference to its successor; a value deleted while guidelines still carry it and no replacement was applied.
- No review policy for the vocabulary, or a review that did not count each value's guidelines against the policy's thresholds.
- Tooling that accepts an unlisted trigger value, or a guideline whose frontmatter does not parse.
- An always-loaded tier holding material that only some tasks need.
- Trigger-filtered loading with no fallback for a task whose triggers miss.
- A selection evaluation with no labelled task set, no tasks that should not load a guideline, no held-out part, or no recall and precision reported.

## A complete review must establish

- Every `triggers` value of every changed guideline is a value of the canonical table in `guide/introduction/trigger-guide.md`.
- Every new value was nominated with the reason no existing value covers it, and reviewed by the editor before it was admitted.
- Every changed, classified guideline carries one to five triggers, most specific first, or `[]` if not yet classified; no artifact other than a guideline carries `triggers`.
- The trigger index was regenerated by `cookr update` after the change and was not edited by hand.
- Every value added or changed in the vocabulary has one meaning, one canonical label, a non-redundant definition, a scope note, an example, task words in its description, and a history note with its date of entry; overlapping values say which applies.
- Every vocabulary change is recorded with its date and the person responsible.
- Every rename is dated and keeps the old value as an alternative label; every change or retirement considered the tagged guidelines; every kept retired value is marked for retrieval only with its dated status change; no value was deleted while guidelines still carried it without retagging them.
- A periodic review policy exists, and each review counted the guidelines per value and tested the vocabulary.
- Tooling rejects values outside the table and frontmatter that does not parse.
- The always-loaded tier holds only what every task needs, and on-demand loading keeps a fallback for missed tags.
- Selection is measured on a labelled task set with a held-out part, and recall and precision are reported.

## A build must establish

- `load-by-activity-not-all`: the agent loads the guidelines its activity's triggers select, not every guideline.
- `filter-only-when-corpus-outgrows-context`: loading the whole corpus instead of filtering is done only when it fits in the prompt.
- `guideline-declares-activities`: every guideline built declares the activities it serves.
- `triggers-field-in-meta`: the triggers sit in the guideline's `triggers` frontmatter field, after `approved-date`.
- `query-union-of-triggers`: a query for several triggers loads the union of the guidelines each returns.
- `principles-always-loaded`: principles are loaded into every task's context.
- `keep-always-loaded-core-small`: the always-loaded tier holds only what every task needs.
- `trigger-filtered-on-demand`: guidelines load only when an activity's trigger selects them.
- `fallback-when-tags-miss`: a description- or search-based selection covers tasks whose triggers miss a guideline.
- `log-loaded-guidelines`: where logging is built, it records which guidelines loaded, when and why.
- `escalating-checkpoint-pattern`: light checks run during work and broader ones at checkpoints.
- `pre-commit-checklist`: the `pre-commit` set is checked before every commit and stays fast.
- `pre-pr-audit`: the broader `pre-pr` set is checked once before the pull request is opened.
- `check-cost-proportional-to-stakes`: a checkpoint's checking grows with the stakes of the action it guards.
- `trigger-index-location`: queries read `cookbook/index/triggers.yaml`.
- `regenerate-index-after-change`: `cookr update` ran after every trigger change.
- `trigger-index-not-hand-edited`: the trigger index holds no hand edits.
- `canonical-values-only`: every `triggers` value is a value of the canonical table in `guide/introduction/trigger-guide.md`.
- `triggers-from-canonical-taxonomy`: the field's values come from the one canonical taxonomy and no other list.
- `one-to-five-triggers`: every classified guideline carries one to five triggers.
- `order-specific-to-general`: each guideline's triggers run from most specific to least specific.
- `triggers-guideline-only`: only guidelines carry a `triggers` field.
- `triggers-empty-until-classified`: a guideline not yet classified carries `[]`.
- `favour-existing-trigger-values`: every new value's nomination states why no existing value covers the activity.
- `add-trigger-to-guide-first`: a missing value was nominated as a candidate, not written unlisted into a guideline.
- `editor-reviews-candidate-values`: every admitted value was reviewed by the vocabulary's editor first.
- `canonical-trigger-vocabulary`: every value in the table has a definition, a "when it fires" scope note and example guidelines.
- `trigger-one-meaning-one-label`: no value has more than one meaning.
- `trigger-single-canonical-label`: no value has more than one canonical label.
- `trigger-values-not-redundant`: no two values share a meaning.
- `trigger-scope-note-per-value`: every value has a scope note saying how its use is limited, beside its definition.
- `overlapping-values-say-which-applies`: values whose scopes overlap each say which one applies.
- `trigger-values-carry-key-terms`: every value's description names when it applies in the tasks' own words.
- `trigger-change-history`: every value has a history note giving its date of entry.
- `trigger-change-dated-with-person`: every addition, modification and deletion records its date and the person responsible.
- `significant-changes-in-history-note`: every significant change to a value's meaning or form is in its history note.
- `administrative-changes-in-change-note`: where change notes are kept, they hold the fine-grained administrative changes.
- `history-note-records-succession`: where succession is recorded, the history note names the values that preceded or succeeded the value.
- `rename-dated-in-history-note`: every rename's date is in the value's history note.
- `rename-keeps-old-value-as-alias`: a renamed value's old name is kept as an alternative label and still resolves to the new one.
- `old-value-matched-not-shown`: where an old form is a hidden label, search and validation match it and the table does not show it.
- `one-for-one-retag-automatically`: where retagging is automated, a one-for-one change retags every guideline carrying the old value.
- `retire-assesses-impact-and-migrates`: every changed or retired value's tagged guidelines were looked at before the change.
- `retired-value-marked-retrieval-only`: every kept retired value is marked for retrieval only, with the date of its status change in its history note.
- `retired-value-points-to-successor`: every superseded value cross-references its successor.
- `no-delete-without-replacement`: no value was deleted while guidelines still carried it without retagging them under a replacement.
- `vocabulary-periodic-review`: a policy sets the periodic review, the adding of values and the replacing of obsolete ones.
- `review-tests-the-vocabulary`: each periodic review tested and evaluated the vocabulary.
- `review-flags-overused-and-rare-values`: each periodic review counted the guidelines per value and listed the values outside the policy's thresholds as candidates.
- `validate-trigger-values-mechanically`: tooling fails on a value outside the table.
- `reject-unparseable-frontmatter`: tooling fails on a guideline whose frontmatter does not parse.
- `measure-trigger-selection-with-labelled-tasks`: selection is measured on a labelled task set of guidelines, tasks that should and should not load them, and the guidelines each task needs.
- `evaluation-before-trigger-text`: the selection evaluation existed before the trigger values and scope notes it tests were written.
- `evaluation-is-source-of-truth`: claims that selection works rest on the evaluation's results.
- `hold-out-part-of-task-set`: part of the task set was held out from tuning.
- `repeat-runs-for-a-rate`: where selection is not deterministic, each task's rate comes from several runs.
- `report-recall-and-precision`: the measurement reports recall and precision.
- `tune-recall-first`: tuning raised recall before it improved precision.

## Rationale

Every agent host now loads context selectively. Agent hosts load path-scoped rules and skill bodies on demand. Cursor has four rule activation modes. Copilot has `applyTo`, and OpenAI file search and Pinecone filter by metadata. The published evaluations (Lost in the Middle, IFScale, Chroma's context-rot report, RAG-MCP) all find that more context and more simultaneous instructions make models less reliable. That supports filtering, though no study measures tag-filtered guideline loading for coding agents. A small corpus that fits in the prompt can still be loaded whole.

The vocabulary rules come from ANSI/NISO Z39.19, ISO 25964 and SKOS. They give a closed list with one meaning and one preferred label per value, a scope note, examples, a dated history, aliases for old forms, and retirement with an impact check. SKOS cannot close a vocabulary, and an agent host ignores a frontmatter field it does not know without an error, so tooling has to enforce the list.

Tags miss. People tagging from a controlled vocabulary agree only 27.5-39.5% of the time, and selection by description under-triggers, so loading needs a fallback and a measurement. The measurement uses IIR's test collection of documents, needs and relevance judgments, scored by recall and precision, which usually trade off.

No source supports any count in the prior text (240 guidelines, 10-20 per query, ~12 for `writing-tests`, 27 principles, ~10 pre-commit rules). No study backs "most effective" for graduated checkpoints, and no source states the proportional-cost rule. The index location, the regeneration step, the hand-edit ban, specific-to-general ordering, the guideline-only scope and the empty-list default are the cookbook's own design, which no outside source addresses. Those rules keep their prior text for the owner, as do the open questions research raised: the uncatalogued `refactor` and `research` values, the counts, whether pre-commit stays mandatory, the fallback and its recall trade, the size of the evaluation set, and the cap of five.

General context loading (retrieving just in time, not front-loading) belongs to [adc.guideline.implementing.skills-and-agents.context-and-memory-management](cookbook:0f999db4-956a-4124-a142-367b1a570983). RFC 2119 keyword case and lint severity belong to the sibling topic [adc.guideline.cookbook.authoring.requirement-keywords](cookbook:456f23bd-4523-47e8-9541-073ac046f2ad).

## References

- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- ANSI/NISO, [Z39.19 Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies](https://groups.niso.org/higherlogic/ws/public/download/6484/Guidelines%20for%20the%20Construction,%20Format,%20and%20Management%20of%20Monolingual%20Controlled%20Vocabularies.pdf)
- NISO, [ISO 25964: the international standard for thesauri](https://www.niso.org/schemas/iso25964)
- W3C, [SKOS Reference](https://www.w3.org/TR/skos-reference/) and [SKOS Primer](https://www.w3.org/TR/skos-primer/)
- Martin Fowler, [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)
- Anthropic, [skill-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md), [Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) and [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
- Cursor, [Rules](https://cursor.com/docs/context/rules)
- GitHub, [Adding repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions) and [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [AGENTS.md](https://agents.md/)
- OpenAI, [File search](https://platform.openai.com/docs/guides/tools-file-search); Pinecone, [Filter by metadata](https://docs.pinecone.io/guides/search/filter-by-metadata)
- [pre-commit](https://pre-commit.com/); Git, [githooks](https://git-scm.com/docs/githooks)
- Stack Overflow, [tagging](https://stackoverflow.com/help/tagging), [create new tags](https://stackoverflow.com/help/privileges/create-tags) and [tag synonyms](https://stackoverflow.com/help/privileges/suggest-tag-synonyms)
- Liu et al., [Lost in the Middle](https://arxiv.org/abs/2307.03172); [How Many Instructions Can LLMs Follow at Once?](https://arxiv.org/abs/2507.11538); Chroma, [Context Rot](https://research.trychroma.com/context-rot); [RAG-MCP](https://arxiv.org/abs/2505.03275)
- Manning, Raghavan and Schütze, [Introduction to Information Retrieval, chapter 8](https://wiki.eecs.yorku.ca/course_archive/2013-14/W/6339/_media/08eval.pdf)
- [Evaluation of controlled vocabularies by inter-indexer consistency](https://informationr.net/ir/16-4/paper502.html)
- The agent hosts' own documentation on memory, skills, skill authoring, tool search and AGENTS.md, which this guideline's `references` lists in full.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-21 | Mike Fullerton | Initial creation, written from research |
