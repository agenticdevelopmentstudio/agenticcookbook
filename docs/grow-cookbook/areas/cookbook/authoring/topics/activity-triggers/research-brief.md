# Research brief: activity-triggers

- **Topic:** activity-triggers, area `cookbook/authoring`.
- **Artifact:** `cookbook/guidelines/cookbook/authoring/activity-triggers` (new: no rules of its own yet; its folder holds only `research/` until stage 3).
- **Base commit:** `071e52f9572bf4b7c534cfcf95fb111282abc423` (from `base.txt`).
- **Research type:** Technology / software (intent Decide; domain retrieval and agent context selection; method specification, tool documentation and published evaluations).
- **Research bar:** Technology / software, no escalation (owner ruling, Owner question 6: "no escalation for any topic. Each keeps its proposed bar. Any metric claim in activity-triggers takes the Statistical bar, as the plan already says."). **Every metric claim** (a precision, recall, accuracy or token figure, or any evidence that filtering by activity improves or harms agent results) takes the *Statistical* bar of `guidelines/researching/process/research-methodology-and-sources`: name the study, its sample, its measure and its result, and score it on that bar.

What the topic rules: the cookbook's `triggers` field (the activity tags a guideline carries so an agent loads only the guidelines relevant to what it is doing now), the controlled vocabulary of trigger values, how a guideline chooses its triggers, how the vocabulary is governed (added to, renamed, retired, with the artifacts migrated), the trigger index an agent queries, the checkpoint pattern of loading (always, on activity, pre-commit, pre-PR), and how the cookbook checks that trigger-filtered loading picks the guidelines a task needs.

**Not this topic's:** RFC 2119 keyword case (RFC 8174's uppercase-only meaning) and the severity a rule's keyword gives a lint finding belong to the sibling topic `requirement-keywords` (`cookbook/guidelines/cookbook/authoring/requirement-keywords`, owner ruling Q10 + Q11). This topic cites it and never restates it: research neither keyword case nor a keyword-to-severity mapping here. Context loading in general (just-in-time retrieval, not front-loading context) is ruled by `cookbook/guidelines/implementing/skills-and-agents/context-and-memory-management` ("should-retrieve-context-just-in-time", "must-not-front-load-context"); this topic cites it for the general rule and researches only the cookbook's own activity selector.

## The four questions

Answer each as its own section, verbatim:

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

## Research questions (from the area plan)

1. Best practice: how should a set of rules be selected for the task in hand: tag-based filtering, a controlled vocabulary of activities, and checkpoint loading (always, on activity, pre-commit, pre-PR)?
2. Known solutions: how do retrieval and agent systems select context by task (Claude Code skills' descriptions and path rules, Cursor rules' globs and descriptions, retrieval-augmented generation with metadata filters), and how does each compare with the trigger guide's 28 canonical triggers and its 1–5 triggers per guideline?
3. Platform guidelines: what do Anthropic's, OpenAI's and other agent hosts' published guidance say about loading instructions conditionally, and what do controlled-vocabulary standards (ISO 25964, SKOS) say about a small fixed vocabulary?
4. The expert's view: what do retrieval and agent-context practitioners say about the precision and recall of tag-filtered loading, and about missing a rule because its tag did not match?
5. **Trigger vocabulary governance**: find how controlled vocabularies are extended, renamed and retired (ISO 25964, SKOS, taxonomy governance practice), and state the procedure for adding, renaming or retiring a trigger and migrating the artifacts that carry it.
6. **Trigger selection evaluation**: find how retrieval systems measure context selection (precision, recall, labelled task sets), and state how the cookbook checks that trigger-filtered loading picks the guidelines a task needs; each metric claim takes the *Statistical* bar.

For question 3, "platform" here means the agent hosts and the vocabulary standards: Anthropic (Claude Code skills, `CLAUDE.md` memory and path-scoped rules, Agent Skills), OpenAI (`AGENTS.md`, Codex, the Assistants/Responses file-search metadata filters), Cursor (project rules), GitHub Copilot (custom instructions, `applyTo` globs), and the W3C SKOS Reference and Primer and ISO 25964 for the vocabulary. Apple, Android and Windows have no bearing on this topic; say so in one line rather than researching them.

## Method

- Research to `guidelines/researching/process/research-methodology-and-sources`, using its source catalogue for the domain (retrieval and agent context selection; controlled vocabularies). Primary sources come before secondary ones: the agent hosts' own documentation (Anthropic, OpenAI, Cursor, GitHub), the W3C SKOS Recommendation and Primer, ISO 25964 (or its publicly available descriptions by ISO/NISO), ANSI/NISO Z39.19, and peer-reviewed or preprint evaluations of retrieval and tool/instruction selection (for metric claims). Use a secondary source only for what no primary source covers, and say so in the claim's trust basis.
- Verify every rule listed below. Each is quoted **verbatim**, with the file it is in and the base commit, as a claim to check, never as a source.
- Score each claim 0–100 per `guidelines/researching/evidence/verification-and-trust-scoring`, applying the principles `cite-the-claim-not-the-document`, `independence-before-corroboration`, `domain-stratified-trust`, `suppress-unsupported-confidence` and `provenance-at-generation-time`.
- `supported` means supported **at the rule's stated strength**: a MUST whose sources say "should" is `unsupported`, with the claim saying so. A rule marked *no RFC keyword* is judged on whether the research supports the practice it states; record the strength the sources support.
- Rules that state the cookbook's own internal design (where the index file lives, what `cookr update` generates, where the field sits in the meta) cannot be confirmed by an outside source as such; judge whether outside practice supports the design choice they make (a generated index never hand-edited, a closed vocabulary, a per-item tag cap), and record what it supports or finds against.
- A rule that carries a number (1–5 triggers, 28 triggers, ~12 or 10–20 guidelines per query, ~10 pre-commit rules) is supported only if a source supports that number or a range holding it; otherwise record it `unsupported` and say what the sources do support. A claim that filtering improves results ("dilutes signal", "most effective") is a metric claim: Statistical bar.
- Find what the topic is missing: practice the research finds that no rule covers, each as a `new` verdict naming a kebab-case rule (for instance a fallback when no trigger matches, a scope note or definition per trigger, a deprecation path, a measured evaluation set).

## The cookbook's current state (context, not a source)

At the base commit, for orientation only (never cite it as evidence): the `artifact.json` files of type `guideline` under `cookbook/` that carry a `triggers` list number 739, with list lengths 0 (22), 1 (162), 2 (491), 3 (60) and 4 (4); 30 distinct values are in use, the 28 canonical triggers plus `refactor` (17) and `research` (10), which the canonical table does not list. `cookbook/index/triggers.yaml` exists and begins "# Auto-generated by `cookr update` (strategy: triggers)" and "# Do not edit manually — re-run `cookr update` to regenerate." The trigger guide's own counts ("240 guidelines across 16 categories", "Principles (27 items)") are older than the cookbook's present counts.

## The rules to verify

All quoted verbatim at base commit `071e52f9572bf4b7c534cfcf95fb111282abc423`.

### From `guide/introduction/trigger-guide.md` (the draft)

The guide's summary, context only (not a rule): "Activity-based trigger system for filtering guidelines by what an AI agent is currently doing."

1. **load-by-activity-not-all** (no RFC keyword; section *Trigger Guide* intro and *Purpose*; metric claim, Statistical bar):
   > Instead of loading all 240 guidelines into context, agents query by activity to get the 10-20 that matter right now.

   > Guidelines are the opposite: numerous, specific, and most are irrelevant to any given task. Loading all of them wastes context and dilutes signal.

2. **guideline-declares-activities** (no RFC keyword; section *Purpose*):
   > Triggers solve this. Each guideline declares the activities where it's relevant. An agent about to write tests queries `writing-tests` and gets ~12 guidelines instead of 240.

3. **canonical-trigger-vocabulary** (no RFC keyword; section *Canonical Triggers*, the table whole):
   > | Trigger | When It Fires | Example Guidelines |
   > |---------|--------------|-------------------|
   > | `writing-tests` | Writing or modifying tests | test-pyramid, unit-test-patterns, properties-of-good-tests |
   > | `error-handling` | Adding try/except, catch, error paths | error-responses, retry-and-resilience, feedback-patterns |
   > | `new-module` | Creating a new file, module, or package | linting, scope-discipline, api-design |
   > | `api-integration` | Calling external APIs (REST, GraphQL, gRPC) | input-validation, cors, timeouts, rate-limiting |
   > | `ai-api-integration` | Calling AI/ML provider APIs specifically | ai-provider-observability, ai-cost-management |
   > | `data-modeling` | Defining types, schemas, database tables | concurrency, immutability, privacy |
   > | `database-operations` | Writing queries, migrations, transactions | sqlite-best-practices, indexing, query-optimization |
   > | `ui-implementation` | Building UI components or layouts | layout, color, typography, accessibility |
   > | `authentication` | Implementing auth flows, tokens, sessions | authentication, authorization, token-handling |
   > | `input-handling` | Processing user input, form data, file uploads | input-validation, form-design |
   > | `networking` | HTTP clients, WebSockets, retry logic, caching | caching, retry-and-resilience, timeouts, transport-security |
   > | `concurrency` | Threads, async/await, locks, queues | concurrency, immutability, background-tasks |
   > | `logging` | Adding log statements, analytics events | logging, analytics, sensitive-data |
   > | `security-review` | Reviewing code for security concerns | authentication, input-validation, secure-storage, privacy |
   > | `performance-optimization` | Optimizing hot paths, queries, rendering | caching, indexing, query-optimization, concurrency |
   > | `accessibility` | Screen readers, keyboard nav, contrast, Dynamic Type | accessibility, animation-motion, touch-click-targets |
   > | `internationalization` | Localization, RTL, locale formatting | localization, rtl-support |
   > | `feature-flags` | Adding or managing feature flags | feature-flags, ab-testing, debug-mode |
   > | `platform-integration` | Deep links, notifications, widgets, sharing | deep-linking, notifications, widgets-and-glanceable-surfaces |
   > | `code-review` | Reviewing code quality, structure, patterns | scope-discipline, properties-of-good-tests, post-generation-verification |
   > | `pre-commit` | Final check before committing code | linting, atomic-commits, bulk-operation-verification |
   > | `pre-pr` | Final check before opening a pull request | test-pyramid, flaky-test-prevention, accessibility, security-headers-checklist |
   > | `dependency-management` | Adding, updating, or auditing dependencies | dependency-security, no-external-dependencies-in-core-librari |
   > | `configuration` | App settings, environment config, build config | deep-linking, shortcuts-and-automation, backup-and-recovery |
   > | `offline-support` | Offline-first patterns, sync, conflict resolution | offline-and-connectivity, sync-engine-design, conflict-resolution |
   > | `skill-authoring` | Writing Claude Code skills, rules, or agents | authoring-skills-and-rules, skill-checklist, agent-checklist |
   > | `recipe-authoring` | Writing or modifying cookbook recipes | recipe-quality guidelines |
   > | `schema-design` | Designing database schemas, migrations | sqlite-best-practices, schema-evolution, sync-schema-design |

   Judge the design this table embodies (a small closed vocabulary of activities, each with a "when it fires" scope note and examples), not each row's examples.

4. **escalating-checkpoint-pattern** (no RFC keyword; section *Escalating checkpoint pattern*; "most effective" is a metric claim, Statistical bar):
   > The most effective usage is graduated — lightweight guardrails during active work, thorough review at natural checkpoints:

5. **principles-always-loaded** (no RFC keyword; same section, item 1):
   > **Principles** — always loaded into context. Small (27 items), universal, load-bearing. These are the foundation that applies to every task.

6. **trigger-filtered-on-demand** (no RFC keyword; same section, item 2):
   > **Trigger-filtered guidelines** — loaded on demand based on current activity. When an agent is about to write tests, it queries `writing-tests` and gets ~12 specific testing guidelines. When it's about to call an API, it queries `api-integration` and gets the relevant networking and security guidelines.

7. **pre-commit-checklist** (no RFC keyword; same section, item 3):
   > **Pre-commit checklist** — a small mandatory set (~10 rules) triggered by `pre-commit`. Checked before every commit. Fast, focused, catches common issues.

8. **pre-pr-audit** (no RFC keyword; same section, item 4):
   > **Pre-PR audit** — a broader set triggered by `pre-pr`. Checked once before opening a pull request. More thorough, covers testing completeness, accessibility, security headers.

9. **check-cost-proportional-to-stakes** (no RFC keyword; same section):
   > The cost of checking is proportional to the stakes of the action.

10. **trigger-index-location** (no RFC keyword; section *Querying triggers*):
    > The trigger index lives at `cookbook/index/triggers.yaml` (generated by `cookr update`). It lists each guideline by its source folder, relative to `cookbook/`:

11. **query-union-of-triggers** (no RFC keyword; section *Querying triggers*):
    > An agent can query multiple triggers at once. The union of results gives the full set of relevant guidelines:

12. **regenerate-index-after-change** (no RFC keyword; section *Regenerating the index*):
    > After adding or modifying guideline triggers, regenerate:

    followed by the command `cookr update`.

13. **trigger-index-not-hand-edited** (no RFC keyword; section *Regenerating the index*):
    > The index is a generated artifact — do not edit it manually.

14. **triggers-field-in-meta** (no RFC keyword; section *Adding Triggers to a Guideline*):
    > Add a `triggers` field to the guideline's YAML frontmatter, after `approved-date`:

15. **one-to-five-triggers** (no RFC keyword; section *Adding Triggers to a Guideline*, Rules):
    > Use 1-5 triggers per guideline. More than 5 means the guideline is too broad or the triggers are too granular.

16. **canonical-values-only** (no RFC keyword; same list):
    > Use only values from the canonical trigger table above.

17. **add-trigger-to-guide-first** (no RFC keyword; same list):
    > If a new trigger is needed, add it to this document first, then use it.

18. **order-specific-to-general** (no RFC keyword; same list):
    > Order triggers from most specific to least specific.

### From `guide/introduction/conventions.md`, the meta field table (row `triggers`)

19. **triggers-guideline-only** (no RFC keyword):
    > | `triggers` | Guideline only | Activity or context tags that make this guideline relevant to an AI agent.

20. **triggers-empty-until-classified** (no RFC keyword):
    > Empty list `[]` if not yet classified.

21. **triggers-from-canonical-taxonomy** (no RFC keyword):
    > Values from the canonical trigger taxonomy in `guide/introduction/trigger-guide.md`. |

## The devteam's text

None: the area has no speciality (`run_gaps.py` `why_empty` "area has no speciality"; `reference.json` is `[]`). No devteam sentence is quoted under this topic.

## Missing subjects this topic hosts

- **Trigger vocabulary governance** (area plan, Missing subjects 3): "the trigger guide fixes 28 canonical triggers but says nothing on how a trigger is added, renamed or retired, or how artifacts are migrated when the vocabulary changes." Research question 5 above.
- **Trigger selection evaluation** (area plan, Missing subjects 4): "nothing measures whether trigger-filtered loading picks the guidelines a task needs, or what it misses." Research question 6 above; every metric claim takes the *Statistical* bar.

## Overlaps to respect

- `cookbook/guidelines/implementing/skills-and-agents/context-and-memory-management` rules context loading in general; this topic cites it and rules only the cookbook's activity selector (area plan, Overlaps).
- `cookbook/guidelines/cookbook/skills-and-agents/skill-checklist`'s "should-use-natural-trigger-keywords" rules a skill's description, not an artifact's `triggers` field: no shared ground beyond the word.
- `requirement-keywords` owns keyword case and lint severity (Q10 + Q11).
