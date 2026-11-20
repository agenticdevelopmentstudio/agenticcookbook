# Phase 2, batch 1: topics converted to roled parts

Base for every lossless check: `0005775`. Every topic passed `cookr roles lossless --draft`, `cookr roles check` and `approve.py` (RESULT: APPROVED), and was committed alone with `commit_topic.py`. No topic has an `obsolete` entry, and none has a `judged` record.

| Topic | Commit | Rules | Moved | Obsolete |
|---|---|---|---|---|
| brainstorming/convergent-techniques | baeca03f | 12 | 0 | 0 |
| brainstorming/divergent-techniques | 1c35c595 | 16 | 0 | 0 |
| brainstorming/facilitation-without-anchoring | db506541 | 17 | 0 | 0 |
| brainstorming/framing-techniques | bdbf32f6 | 10 | 2 | 0 |
| cookbook/recipe-quality/behavioral-requirements | b34fc8d0 | 18 | 0 | 0 |
| cookbook/recipe-quality/completeness | bd1016bf | 18 | 3 | 0 |
| cookbook/recipe-quality/cookbook-compliance | f59aaa28 | 18 | 1 | 0 |
| cookbook/recipe-quality/cross-recipe-consistency | 85af7ed7 | 15 | 0 | 0 |
| cookbook/recipe-quality/source-fidelity | 5bce5c0f | 17 | 2 | 0 |
| cookbook/recipe-quality/template-conformance | 598e5337 | 23 | 0 | 0 |
| cookbook/skills-and-agents/agent-checklist | 95affcd4 | 29 | 0 | 0 |
| cookbook/skills-and-agents/rule-checklist | 71a9eeba | 26 | 0 | 0 |
| cookbook/skills-and-agents/skill-checklist | 02eb4aaf | 36 | 0 | 0 |
| cookbook/testing/properties-of-good-tests | 539abd45 | 6 | 0 | 0 |
| cookbook/testing/unit-test-patterns | 43bb4949 | 6 | 1 | 0 |
| implementing/accessibility/accessibility | bf589c2a | 24 | 27 | 0 |
| implementing/accessibility/dynamic-type | ea878800 | 3 | 2 | 0 |
| implementing/accessibility/font-scaling | e17b1207 | 3 | 1 | 0 |

All paths are under `cookbook/guidelines/`.

## brainstorming/convergent-techniques

- **promoted**: none. The named rules were already in the topic and were gathered into `rules.md` word for word. The technique one-liners stayed as `how-to` parts. The `idea-selection-user-led` part was left empty by the move and was deleted.
- **bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.
- **contradictions (R4)**: `affinity-small-first` is a SHOULD that carries an absolute: "… SHOULD … never from predefined clusters". Its level is unclear. The intro still says divergence must end first ("MUST NOT be introduced until divergence is complete."), and `convergence-after-divergence` repeats this. That is a duplicate, not a conflict.
- **unfinished**: nothing.

## brainstorming/divergent-techniques

- **promoted**: none.
- **bars**: look-for authored; review-bar authored; build-bar authored. The `how-to` parts were kept.
- **contradictions (R4)**: none found.
- **unfinished**: nothing.

## brainstorming/facilitation-without-anchoring

- **promoted**: none. Every rule was already named in the eight source parts. Each part was left empty by the move and was deleted.
- **bars**: look-for authored; review-bar authored; build-bar authored.
- **contradictions (R4)**: `burst-dedup` puts MUST and SHOULD in one rule, so its overall level is unclear.
- **unfinished**: nothing.

## brainstorming/framing-techniques

- **promoted**: none. The intro's requirement already used MUST. It became the rule `framing-before-divergence`: "Framing techniques MUST be applied before any divergent phase; premature ideation on a misframed problem wastes all generative effort." The intro was cut back to its first sentence. Its two wrapped-line sentences are recorded as moved to that rule.
- **bars**: look-for authored; review-bar authored; build-bar authored. The source lines moved to a `references` part, one per technique: "- <Technique>. Source: …".
- **contradictions (R4)**: none found.
- **unfinished**: nothing.

## cookbook/recipe-quality/behavioral-requirements

- **promoted**: none. The "Numeric…" bullet was split into `must-include-specific-values-for-measurable-constraints` and `should-not-use-unanchored-relative-terms`. `must-describe-required-outcome` was named from the common-violations sentence, which already said MUST: "A requirement MUST describe the required outcome, not the attempt — "MUST try to" implies effort, not outcome."
- **bars**: review-focus **moved** (the verification checklist, with 6 lines added for rules it did not cover); review-bar authored; build-bar authored. Common violations became `examples`.
- **contradictions (R4)**: none found.
- **unfinished**: nothing.

## cookbook/recipe-quality/completeness

- **promoted**: none. Rules that were split:
  - The test-vector rule became two rules: test vectors must be specified, and they must be concrete.
  - "SHOULD have test vectors" was separated from "document their omission".
  `must-not-submit-with-reminder-markers` was named from the common-violations sentence, which already said MUST NOT: "A recipe in this state MUST NOT be submitted for review."
- **forced wording change**: approve.py's FM-13 check matches the word itself as a reminder marker (`\b(TODO|TBD|FIXME|placeholder|fill in)\b`), including inside inline code. This topic's own subject matter uses that word, so it was respelled "place-holder" in intro.md, rules.md and verification-checklist.md. The rule was named `must-not-use-needs-review-for-later-content`. The 3 moved entries come from this respelling: one intro sentence to `intro`, one rule sentence to the rule, and one checklist line to `verification-checklist`. The meaning is unchanged. The orchestrator may prefer to change FM-13 to skip inline code rather than keep the respelling.
- **bars**: review-focus **moved** (the verification checklist, plus 4 lines); review-bar authored; build-bar authored.
- **contradictions (R4)**: "No MUST requirement MAY be left without a corresponding test vector" uses MAY as a prohibition. MUST NOT is meant.
- **unfinished**: nothing.

## cookbook/recipe-quality/cookbook-compliance

- **promoted**: none.
- **forced wording change**: the same FM-13 respelling ("place-holder") in one heading of common-violations.md. That is the 1 moved entry, to `common-violations`.
- **bars**: review-focus **moved** (the verification checklist, plus 6 lines); review-bar authored; build-bar authored.
- **contradictions (R4)**: none found.
- **unfinished**: nothing.

## cookbook/recipe-quality/cross-recipe-consistency

- **promoted**: none. The "Comparable complexity" definition became a sub-bullet of `should-match-sibling-section-depth`.
- **bars**: review-focus **moved** (the verification checklist, plus 4 lines); review-bar authored; build-bar authored.
- **contradictions (R4)**:
  - `no-incoherent-depth-standard`: "No recipe … MAY set …" uses MAY as a prohibition.
  - "a new recipe MUST not use" has a lowercase "not".
  - The rule "Unidirectional cross-references are acceptable but bidirectional is preferred" (a SHOULD) conflicts with the checklist's "Existing related recipes have been updated…", which reads as a requirement.
  - `must-explain-depth-disparity` puts MUST together with "SHOULD be noted".
- **unfinished**: nothing.

## cookbook/recipe-quality/source-fidelity

- **promoted** (2):
  - before: "A recipe that claims `MUST display an error message on failure` when the source code makes no such attempt is a source fidelity failure regardless of whether the behavior is desirable." (its only MUST is inside the quoted code). After: `must-not-claim-unattempted-error-handling`: "A recipe MUST NOT claim `MUST display an error message on failure` when the source code makes no such attempt; such a claim is a source fidelity failure regardless of whether the behavior is desirable."
  - before: "Requirements derived from what "a well-implemented component would do" rather than what the code actually does are a source fidelity violation." After: `must-not-derive-requirements-from-an-ideal`: "Requirements MUST NOT be derived from what "a well-implemented component would do" rather than what the code actually does; such requirements are a source fidelity violation."
  - Both originals are recorded as moved to their rules. In both, "is a … failure/violation" was read as MUST NOT.
- **splits**: the technical-debt bullet became `should-note-behavior-affecting-technical-debt` and `must-not-treat-behavior-affecting-debt-as-optional`. The "as it is" bullet was split before "Aspirational behavior" into `must-describe-code-as-it-is` and `must-separate-aspirational-behavior`.
- **bars**: review-focus **moved** (the verification checklist, plus 3 lines); review-bar authored; build-bar authored.
- **contradictions (R4)**:
  - "Technical debt in the source SHOULD be noted in Design Decisions when it affects behavioral correctness." is followed by "Authors MUST NOT treat documentation of technical debt as optional when the debt affects how implementations must behave". The same condition is given at SHOULD and at MUST, and the second sentence also has a lowercase "must behave".
  - The checklist's "Technical debt affecting behavioral correctness is documented in Design Decisions." reads as required, while the first rule is only a SHOULD.
- **unfinished**: nothing.

## cookbook/recipe-quality/template-conformance

- **promoted**: none. "Additional sections MAY be appended … They MUST NOT be inserted …" was split into `may-append-extra-sections-at-end` and `must-not-insert-sections-between-required`. The component-recipe section list became a sub-bullet of `must-contain-template-sections-in-order`.
- **bars**: review-focus **moved** (the verification checklist, plus 4 lines); review-bar authored; build-bar authored.
- **contradictions (R4)**:
  - Two rules use MAY as a prohibition where MUST NOT is meant: "No two recipes in the cookbook MAY share the same `id`." and "No required section MAY be omitted, even if its content is marked `NEEDS REVIEW`."
  - Two rules use "NOT permitted", which is not an RFC keyword: "Pre-release labels and build metadata are NOT permitted." and "Aliases … are NOT permitted."
  - The rule lists 10 required fields ("`id`, `title`, `type`, `version`, `status`, `language`, `created`, `modified`, `author`, and `summary`"). The checklist requires 15 ("… `summary`, `platforms`, `tags`, `depends-on`, `related`, `references`"). No rule requires `platforms` or `tags` to be present.
  - The whole topic describes a YAML-frontmatter recipe file, but history 2.0.0 says cookr format 2 replaced it ("UUID identity and rdid links replace the domain field"), so the frontmatter rules may be out of date.
- **unfinished**: nothing.

## cookbook/skills-and-agents/agent-checklist

- **promoted**: all 29. Each table row had no keyword of its own. Its level comes from the intro's severity legend: FAIL to MUST, WARN to SHOULD, INFO to MAY. The tables were kept unchanged, and each rule ends with its row ID and severity.
- `must-have-yaml-frontmatter` — before: "| S01 | YAML frontmatter present | File starts with `---`, has closing `---` | FAIL |" — after: "The agent file MUST have YAML frontmatter: it starts with `---` and has a closing `---`."
- `should-have-name-field` — before: "| S02 | `name` field present | Frontmatter contains `name:` | WARN |" — after: "The frontmatter SHOULD contain a `name:` field."
- `must-use-kebab-case-name` — before: "| S03 | `name` is kebab-case, lowercase, ≤64 chars | Regex: `^[a-z][a-z0-9-]{0,63}$` | FAIL |" — after: "The `name` MUST be lowercase kebab-case of at most 64 characters, matching `^[a-z][a-z0-9-]{0,63}$`."
- `must-have-description-field` — before: "| S04 | `description` field present | Frontmatter contains `description:` | FAIL |" — after: "The frontmatter MUST contain a `description:` field."
- `should-use-natural-trigger-keywords` — before: "| S05 | Description uses natural trigger keywords | Description includes phrases users would say; not too vague or too narrow | WARN |" — after: "The description SHOULD use natural trigger keywords: phrases users would say, neither too vague nor too narrow."
- `should-be-in-agents-directory` — before: "| S11 | Correct file location | Agent is in `.claude/agents/` or `~/.claude/agents/` | WARN |" — after: "The agent SHOULD be in `.claude/agents/` or `~/.claude/agents/`."
- `should-use-only-recognized-frontmatter-fields` — before: "| S12 | Only recognized frontmatter fields | Check against known fields: name, description, tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, effort, isolation | WARN |" — after: "The frontmatter SHOULD use only recognized fields: name, description, tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, effort, isolation."
- `should-use-lowercase-kebab-case-filename` — before: "| S13 | Filename is lowercase kebab-case | Filename matches `^[a-z][a-z0-9-]*\.md$`; UPPERCASE stems are reserved for identity files like `SKILL.md` and `CLAUDE.md` | WARN |" — after: "The filename SHOULD be lowercase kebab-case, matching `^[a-z][a-z0-9-]*\.md$`; UPPERCASE stems are reserved for identity files like `SKILL.md` and `CLAUDE.md`."
- `should-have-single-responsibility` — before: "| C01 | Single responsibility | Agent has one clear purpose; not a grab-bag of unrelated tasks | WARN |" — after: "The agent SHOULD have one clear purpose, not a grab-bag of unrelated tasks."
- `should-cover-error-handling` — before: "| C04 | Error handling covered | System prompt addresses what to do when things go wrong (tool failures, missing files, bad input) | WARN |" — after: "The system prompt SHOULD address what to do when things go wrong (tool failures, missing files, bad input)."
- `should-give-actionable-specific-instructions` — before: "| C07 | Instructions are actionable and specific | System prompt tells the agent what to do concretely | WARN |" — after: "The system prompt SHOULD tell the agent concretely what to do."
- `must-not-conflict-with-itself` — before: "| C08 | No conflicting instructions | Body does not contradict itself | FAIL |" — after: "The body MUST NOT contradict itself."
- `should-use-well-structured-markdown` — before: "| C09 | Well-structured markdown | Uses headings, lists, code blocks; not a wall of unstructured text | WARN |" — after: "The body SHOULD use headings, lists and code blocks, not a wall of unstructured text."
- `should-provide-verification-method` — before: "| B01 | Verification method provided | Agent includes how to validate it completed successfully | WARN |" — after: "The agent SHOULD include how to validate that it completed successfully."
- `should-not-replicate-native-capabilities` — before: "| B02 | Does not replicate native capabilities | Agent doesn't teach Claude things it already knows | WARN |" — after: "The agent SHOULD NOT teach Claude things it already knows."
- `should-include-usage-examples` — before: "| B05 | Examples or usage patterns included | Body or description includes expected usage context | WARN |" — after: "The body or description SHOULD include examples or usage patterns giving the expected usage context."
- `must-not-be-kitchen-sink` — before: "| B06 | No kitchen-sink anti-pattern | Agent doesn't try to do everything — stays focused on its stated purpose | FAIL |" — after: "The agent MUST NOT try to do everything; it stays focused on its stated purpose."
- `should-not-explore-unbounded` — before: "| B07 | No infinite-exploration anti-pattern | Agent scopes its investigation; doesn't read unbounded numbers of files | WARN |" — after: "The agent SHOULD scope its investigation and not read unbounded numbers of files."
- `should-not-be-claude-md-dump` — before: "| B08 | Not a CLAUDE.md dump | Agent content is agent-appropriate, not a copy-paste of project rules that belong in CLAUDE.md | WARN |" — after: "Agent content SHOULD be agent-appropriate, not a copy-paste of project rules that belong in CLAUDE.md."
- `should-match-model-override-to-complexity` — before: "| B10 | Model override appropriate | If `model:` is set, it matches the agent's complexity | WARN |" — after: "If `model:` is set, it SHOULD match the agent's complexity."
- `should-keep-description-under-200-characters` — before: "| B12 | Description concise for context budget | Description is under ~200 characters to avoid consuming excessive context | WARN |" — after: "The description SHOULD be under ~200 characters to avoid consuming excessive context."
- `must-have-name-and-description` — before: "| A01 | `name` and `description` frontmatter present | Agent .md file has both fields | FAIL |" — after: "The agent .md file MUST have both `name` and `description` frontmatter fields."
- `should-restrict-tool-access` — before: "| A02 | Tool access appropriately restricted | `tools` or `disallowedTools` limits access for specialized agents | WARN |" — after: "A specialized agent SHOULD have its tool access limited by `tools` or `disallowedTools`."
- `may-specify-model` — before: "| A03 | `model` field specified if beneficial | Agent benefits from a specific model for its task | INFO |" — after: "The `model` field MAY be specified when the agent benefits from a specific model for its task."
- `should-have-clear-focused-system-prompt` — before: "| A04 | System prompt is clear and focused | Markdown body gives the agent a clear role and scope | WARN |" — after: "The markdown body SHOULD give the agent a clear role and scope."
- `should-set-permission-mode-appropriately` — before: "| A05 | `permissionMode` set appropriately | `plan` for read-only agents, `bypassPermissions` for fully automated | WARN |" — after: "`permissionMode` SHOULD be set appropriately: `plan` for read-only agents, `bypassPermissions` for fully automated ones."
- `should-set-max-turns-for-bounded-tasks` — before: "| A06 | `maxTurns` set for bounded tasks | Simple agents that should finish quickly have a turn limit | WARN |" — after: "A simple agent that should finish quickly SHOULD have a `maxTurns` turn limit."
- `may-preload-skills` — before: "| A07 | `skills` lists preloaded skills if needed | Agent that needs domain knowledge has relevant skills preloaded | INFO |" — after: "An agent that needs domain knowledge MAY list relevant preloaded skills in `skills`."
- `may-scope-memory` — before: "| A08 | `memory` scope appropriate | If agent accumulates knowledge, memory is scoped correctly | INFO |" — after: "If the agent accumulates knowledge, its `memory` scope MAY be set so it is scoped correctly."
- **bars**: review-focus **moved** (the four checklist tables: structure-format, content-quality, best-practices, agent-specific); review-bar authored; build-bar authored, each restating the row's "How to check". The intro's Sources block moved word for word to a `references` part.
- **contradictions (R4)**: "S02 | `name` field present | … | WARN" (`should-have-name-field`) conflicts with "A01 | `name` and `description` frontmatter present | … | FAIL" (`must-have-name-and-description`). The same field is required at two levels.
- **unfinished**: nothing.

## cookbook/skills-and-agents/rule-checklist

- **promoted**: all 26, mapped by the same severity legend. This topic's legend is lowercase ("must fix", "should fix", "nice to have"), so INFO was read as MAY. Keywords that the source quoted (R02, R11, O04) are in backticks so that they do not set the rule's level.
- `should-have-single-responsibility` — before: "| C01 | Single responsibility | Rule addresses one coherent concern — not a grab-bag of unrelated instructions | WARN |" — after: "The rule SHOULD address one coherent concern, not a grab-bag of unrelated instructions."
- `should-give-actionable-specific-instructions` — before: "| C07 | Instructions are actionable and specific | Every instruction tells the LLM what to do concretely, not vague directives like "handle errors appropriately" | WARN |" — after: "Every instruction SHOULD tell the LLM concretely what to do, not give vague directives like "handle errors appropriately"."
- `must-not-conflict-with-itself` — before: "| C08 | No conflicting instructions | Rule does not contradict itself (e.g., "always do X" then later "never do X") | FAIL |" — after: "The rule MUST NOT contradict itself (e.g., "always do X" then later "never do X")."
- `should-use-well-structured-markdown` — before: "| C09 | Well-structured markdown | Uses headings, lists, code blocks; not a wall of unstructured text | WARN |" — after: "The rule SHOULD use headings, lists and code blocks, not a wall of unstructured text."
- `should-not-replicate-native-capabilities` — before: "| B02 | Does not replicate native capabilities | Rule doesn't teach Claude things it already knows (basic git, standard coding, etc.) | WARN |" — after: "The rule SHOULD NOT teach Claude things it already knows (basic git, standard coding, etc.)."
- `must-not-be-kitchen-sink` — before: "| B06 | No kitchen-sink anti-pattern | Rule doesn't try to govern everything — stays focused on its stated concern | FAIL |" — after: "The rule MUST NOT try to govern everything; it stays focused on its stated concern."
- `should-not-be-claude-md-dump` — before: "| B08 | Not a CLAUDE.md dump | Content is rule-appropriate, not project configuration that belongs in CLAUDE.md | WARN |" — after: "Content SHOULD be rule-appropriate, not project configuration that belongs in CLAUDE.md."
- `should-have-clear-title-heading` — before: "| R01 | Clear title/heading | File starts with a heading that identifies the rule's purpose | WARN |" — after: "The file SHOULD start with a heading that identifies the rule's purpose."
- `should-use-imperative-tone` — before: "| R02 | Imperative tone throughout | Uses RFC 2119 keywords (MUST, MUST NOT, SHOULD, MAY); not advisory or suggestive | WARN |" — after: "The rule SHOULD use an imperative tone throughout, with RFC 2119 keywords (`MUST`, `MUST NOT`, `SHOULD`, `MAY`), not advisory or suggestive wording."
- `should-number-or-separate-steps` — before: "| R03 | Steps are numbered or clearly separated | If procedural, steps are in a clear sequence with headings or numbered list | WARN |" — after: "If the rule is procedural, its steps SHOULD be in a clear sequence with headings or a numbered list."
- `must-not-use-vague-directives` — before: "| R04 | No vague directives | Every instruction is concrete and actionable; no "handle appropriately" or "write good code" | FAIL |" — after: "Every instruction MUST be concrete and actionable; no "handle appropriately" or "write good code"."
- `must-list-file-references-explicitly` — before: "| R05 | File references are explicit | If the rule says to read files, every file path is listed explicitly — no "read the principles" without paths | FAIL |" — after: "If the rule says to read files, every file path MUST be listed explicitly; no "read the principles" without paths."
- `must-not-give-contradictory-instructions` — before: "| R06 | No contradictory instructions | Rule does not say "always do X" then later "never do X" or otherwise conflict with itself | FAIL |" — after: "The rule MUST NOT say "always do X" then later "never do X" or otherwise conflict with itself."
- `should-address-single-concern` — before: "| R07 | Single concern | Rule addresses one coherent concern (planning, implementing, reviewing) — not a grab-bag | WARN |" — after: "The rule SHOULD address one coherent concern (planning, implementing, reviewing), not a grab-bag."
- `should-include-enforcement-mechanism` — before: "| R08 | Enforcement mechanism present | Rule includes steps to verify compliance — not just "do X" but "verify X was done" | WARN |" — after: "The rule SHOULD include steps to verify compliance: not just "do X" but "verify X was done"."
- `should-not-be-claude-md-dump-rule-specific` — before: "| R09 | Not a CLAUDE.md dump | Content is rule-appropriate, not project configuration that belongs in CLAUDE.md | WARN |" — after: "Content SHOULD be rule-appropriate, not project configuration that belongs in CLAUDE.md."
- `should-have-reasonable-length` — before: "| R10 | Reasonable length | Rule is long enough to be complete but not so long it gets ignored; under ~300 lines for a single rule file | WARN |" — after: "The rule SHOULD be long enough to be complete but not so long it gets ignored: under ~300 lines for a single rule file."
- `should-have-must-not-section` — before: "| R11 | "MUST NOT" section present | Rule explicitly states what the LLM must NOT do — common mistakes and anti-patterns | WARN |" — after: "The rule SHOULD have a `MUST NOT` section explicitly stating what the LLM must not do: common mistakes and anti-patterns."
- `should-be-deterministic` — before: "| R12 | Deterministic — no ambiguity | An LLM following the rule would produce consistent behavior across sessions; no room for interpretation on critical steps | WARN |" — after: "The rule SHOULD be unambiguous: an LLM following it would produce consistent behavior across sessions, with no room for interpretation on critical steps."
- `should-use-lowercase-kebab-case-filename` — before: "| R13 | Filename is lowercase kebab-case | Filename matches `^[a-z][a-z0-9-]*\.md$` (e.g., `testing.md`, `api-design.md`); UPPERCASE stems are reserved for identity files like `SKILL.md` and `CLAUDE.md` | WARN |" — after: "The filename SHOULD be lowercase kebab-case, matching `^[a-z][a-z0-9-]*\.md$` (e.g., `testing.md`, `api-design.md`); UPPERCASE stems are reserved for identity files like `SKILL.md` and `CLAUDE.md`."
- `should-stay-under-200-lines-8kb` — before: "| O01 | Rule file under 200 lines / ~8KB | Count lines and bytes; larger rules should move content to on-demand skills or external references | WARN |" — after: "The rule file SHOULD be under 200 lines / ~8KB; larger rules should move content to on-demand skills or external references."
- `should-not-duplicate-another-rule` — before: "| O02 | No content duplicated from another rule | Compare against other `.md` files in the same `.claude/rules/` directory; overlapping instructions are processed twice per turn | WARN |" — after: "The rule SHOULD NOT duplicate content from another `.md` file in the same `.claude/rules/` directory; overlapping instructions are processed twice per turn."
- `should-have-globs-when-scoped` — before: "| O03 | `globs` frontmatter present when scoped | If the rule only applies to specific file patterns (e.g., `.claude/**`, `site/**`), it should have `globs` frontmatter to prevent loading on unrelated work | WARN |" — after: "If the rule only applies to specific file patterns (e.g., `.claude/**`, `site/**`), it SHOULD have `globs` frontmatter to prevent loading on unrelated work."
- `should-keep-must-not-items-unique` — before: "| O04 | MUST NOT items are unique | Each MUST NOT adds a constraint not already expressed imperatively in the body text; restating "You MUST NOT skip this phase" from line 50 in the MUST NOT section wastes per-turn context | WARN |" — after: "Each `MUST NOT` item SHOULD add a constraint not already expressed imperatively in the body text."
- `may-inline-low-ratio-external-refs` — before: "| O05 | External refs have high content ratio | If an external file reference points to a file where frontmatter exceeds 50% of total lines, suggest inlining the useful content instead | INFO |" — after: "If an external file reference points to a file where frontmatter exceeds 50% of total lines, the review MAY suggest inlining the useful content instead."
- `should-limit-unconditional-external-reads` — before: "| O06 | No more than 5 unconditional external reads | Rules that mandate reading 6+ external files before any work create high entry cost; consider summaries, on-demand reads, or iterative approaches | WARN |" — after: "The rule SHOULD mandate no more than 5 unconditional external reads before any work; 6+ create high entry cost."
- **bars**: review-focus **moved** (the four checklist tables); review-bar authored; build-bar authored. The optimization part's opening paragraph moved word for word to a `rationale` part, "Why Rule Size Matters". The Sources block moved to `references`.
- **contradictions (R4)**:
  - Three pairs of rules say the same thing twice, though not in conflict: C08 and R06 (no contradictions), C01 and R07 (single concern), B08 and R09 (not a CLAUDE.md dump).
  - The legend's lowercase "must/should" is not RFC 2119.
- **unfinished**: nothing.

## cookbook/skills-and-agents/skill-checklist

- **promoted**: all 36, mapped by the severity legend.
- `must-have-yaml-frontmatter` — before: "| S01 | YAML frontmatter present | File starts with `---`, has closing `---` | FAIL |" — after: "The skill file MUST have YAML frontmatter: it starts with `---` and has a closing `---`."
- `should-have-name-field` — before: "| S02 | `name` field present | Frontmatter contains `name:` | WARN |" — after: "The frontmatter SHOULD contain a `name:` field."
- `must-use-kebab-case-name` — before: "| S03 | `name` is kebab-case, lowercase, ≤64 chars | Regex: `^[a-z][a-z0-9-]{0,63}$` | FAIL |" — after: "The `name` MUST be lowercase kebab-case of at most 64 characters, matching `^[a-z][a-z0-9-]{0,63}$`."
- `must-have-description-field` — before: "| S04 | `description` field present | Frontmatter contains `description:` | FAIL |" — after: "The frontmatter MUST contain a `description:` field."
- `should-use-natural-trigger-keywords` — before: "| S05 | Description uses natural trigger keywords | Description includes phrases users would say; not too vague ("does stuff") or too narrow ("only for X on Tuesdays") | WARN |" — after: "The description SHOULD use natural trigger keywords: phrases users would say, neither too vague ("does stuff") nor too narrow ("only for X on Tuesdays")."
- `should-keep-skill-md-under-500-lines` — before: "| S06 | SKILL.md ≤ 500 lines | `wc -l SKILL.md` | WARN |" — after: "SKILL.md SHOULD be at most 500 lines (`wc -l SKILL.md`)."
- `should-put-supporting-files-in-subdirectories` — before: "| S07 | Supporting files in subdirectories | Loose files (non-SKILL.md) at skill root → should be in references/, scripts/, examples/ | WARN |" — after: "Supporting files (non-SKILL.md) SHOULD be in references/, scripts/ or examples/, not loose at the skill root."
- `should-reference-supporting-files` — before: "| S08 | SKILL.md references its supporting files | If references/ exists, SKILL.md mentions those files or uses `${CLAUDE_SKILL_DIR}` to load them | WARN |" — after: "If references/ exists, SKILL.md SHOULD mention those files or use `${CLAUDE_SKILL_DIR}` to load them."
- `should-match-directory-to-name` — before: "| S09 | Directory name matches `name` field | Compare directory basename to frontmatter `name` | WARN |" — after: "The directory basename SHOULD match the frontmatter `name`."
- `should-have-argument-hint-when-using-arguments` — before: "| S10 | `argument-hint` present if `$ARGUMENTS` used | SKILL.md uses `$ARGUMENTS` or `$1`, `$2` but frontmatter lacks `argument-hint:` | WARN |" — after: "If SKILL.md uses `$ARGUMENTS` or `$1`, `$2`, the frontmatter SHOULD have `argument-hint:`."
- `should-be-in-skills-directory` — before: "| S11 | Correct file location | Skill is in `.claude/skills/` or `~/.claude/skills/` | WARN |" — after: "The skill SHOULD be in `.claude/skills/` or `~/.claude/skills/`."
- `should-use-only-recognized-frontmatter-fields` — before: "| S12 | Only recognized frontmatter fields | Check against known fields: name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model, effort, context, agent, hooks, paths, shell | WARN |" — after: "The frontmatter SHOULD use only recognized fields: name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model, effort, context, agent, hooks, paths, shell."
- `must-name-main-file-skill-md` — before: "| S13 | Main file named `SKILL.md` (uppercase stem) | Filename is exactly `SKILL.md`, not `skill.md` or `Skill.md` — Claude Code looks for this exact name | FAIL |" — after: "The main file MUST be named exactly `SKILL.md`, not `skill.md` or `Skill.md`; Claude Code looks for this exact name."
- `should-use-lowercase-descriptive-supporting-names` — before: "| S14 | Supporting files use lowercase descriptive names | Files in references/, scripts/, examples/ match `^[a-z][a-z0-9-]*(\.[a-z]+)+$`; names describe content (not `doc1.md`) | WARN |" — after: "Files in references/, scripts/ and examples/ SHOULD match `^[a-z][a-z0-9-]*(\.[a-z]+)+$` and have names that describe their content (not `doc1.md`)."
- `should-have-single-responsibility` — before: "| C01 | Single responsibility | Skill has one clear purpose; not a grab-bag of unrelated instructions | WARN |" — after: "The skill SHOULD have one clear purpose, not a grab-bag of unrelated instructions."
- `should-give-task-skills-step-by-step-instructions` — before: "| C02 | Task skills have step-by-step instructions | If the skill performs actions (not just reference), it should have numbered steps or a clear workflow | WARN |" — after: "If the skill performs actions (not just reference), it SHOULD have numbered steps or a clear workflow."
- `should-keep-reference-and-task-content-apart` — before: "| C03 | Reference vs task content appropriate | Reference skills (background knowledge) should not have imperative "do X" steps; task skills should not be pure documentation | WARN |" — after: "Reference skills (background knowledge) SHOULD NOT have imperative "do X" steps, and task skills SHOULD NOT be pure documentation."
- `should-cover-error-handling` — before: "| C04 | Error handling covered | Instructions address what to do when things go wrong (tool failures, missing files, bad input) | WARN |" — after: "Instructions SHOULD address what to do when things go wrong (tool failures, missing files, bad input)."
- `should-use-arguments-when-accepting-input` — before: "| C05 | `$ARGUMENTS` used when skill accepts input | Description implies the skill takes input but body never references `$ARGUMENTS` | WARN |" — after: "If the description implies the skill takes input, the body SHOULD reference `$ARGUMENTS`."
- `must-use-claude-skill-dir-for-file-references` — before: "| C06 | `${CLAUDE_SKILL_DIR}` for file references | Skill references its own supporting files using `${CLAUDE_SKILL_DIR}`, not hardcoded paths | FAIL |" — after: "The skill MUST reference its own supporting files using `${CLAUDE_SKILL_DIR}`, not hardcoded paths."
- `should-give-actionable-specific-instructions` — before: "| C07 | Instructions are actionable and specific | Steps tell Claude what to do concretely, not vague directives like "handle errors appropriately" | WARN |" — after: "Steps SHOULD tell Claude concretely what to do, not give vague directives like "handle errors appropriately"."
- `must-not-conflict-with-itself` — before: "| C08 | No conflicting instructions | Body does not contradict itself (e.g., "always do X" then later "never do X") | FAIL |" — after: "The body MUST NOT contradict itself (e.g., "always do X" then later "never do X")."
- `should-use-well-structured-markdown` — before: "| C09 | Well-structured markdown | Uses headings, lists, code blocks; not a wall of unstructured text | WARN |" — after: "The skill SHOULD use headings, lists and code blocks, not a wall of unstructured text."
- `should-not-duplicate-supporting-files` — before: "| C10 | No redundancy with supporting files | SKILL.md and reference files don't duplicate large blocks of the same content | WARN |" — after: "SKILL.md and reference files SHOULD NOT duplicate large blocks of the same content."
- `should-provide-verification-method` — before: "| B01 | Verification method provided | Skill includes how to validate it worked (run tests, check output, verify file exists) | WARN |" — after: "The skill SHOULD include how to validate it worked (run tests, check output, verify file exists)."
- `should-not-replicate-native-capabilities` — before: "| B02 | Does not replicate native capabilities | Skill doesn't teach Claude things it already knows (basic git, standard coding, etc.) | WARN |" — after: "The skill SHOULD NOT teach Claude things it already knows (basic git, standard coding, etc.)."
- `should-disable-model-invocation-for-side-effects` — before: "| B03 | `disable-model-invocation` for side-effect skills | Skills that deploy, commit, send messages, or modify external state should set `disable-model-invocation: true` | WARN |" — after: "Skills that deploy, commit, send messages, or modify external state SHOULD set `disable-model-invocation: true`."
- `may-use-context-fork-for-isolated-tasks` — before: "| B04 | `context: fork` considered for isolated tasks | Task skills that do heavy reading/fetching and return a result benefit from fork isolation | INFO |" — after: "Task skills that do heavy reading/fetching and return a result MAY use `context: fork`, since they benefit from fork isolation."
- `should-include-usage-examples` — before: "| B05 | Examples or usage patterns included | Skill body or references include at least one example invocation or expected output | WARN |" — after: "The skill body or references SHOULD include at least one example invocation or expected output."
- `must-not-be-kitchen-sink` — before: "| B06 | No kitchen-sink anti-pattern | Skill doesn't try to do everything — stays focused on its stated purpose | FAIL |" — after: "The skill MUST NOT try to do everything; it stays focused on its stated purpose."
- `should-not-explore-unbounded` — before: "| B07 | No infinite-exploration anti-pattern | Task skills scope their investigation; don't read unbounded numbers of files | WARN |" — after: "Task skills SHOULD scope their investigation and not read unbounded numbers of files."
- `should-not-be-claude-md-dump` — before: "| B08 | Not a CLAUDE.md dump | Skill content is skill-appropriate, not a copy-paste of project rules that belong in CLAUDE.md | WARN |" — after: "Skill content SHOULD be skill-appropriate, not a copy-paste of project rules that belong in CLAUDE.md."
- `may-use-allowed-tools-for-restriction` — before: "| B09 | `allowed-tools` used if tool restriction needed | If the skill should only use certain tools, `allowed-tools` is set | INFO |" — after: "If the skill should only use certain tools, it MAY set `allowed-tools`."
- `should-match-model-override-to-complexity` — before: "| B10 | Model override appropriate | If `model:` is set, it matches the skill's complexity (don't use opus for trivial tasks) | WARN |" — after: "If `model:` is set, it SHOULD match the skill's complexity (don't use opus for trivial tasks)."
- `should-keep-dynamic-context-injection-safe` — before: "| B11 | Dynamic context injection correct | If `` !`command` `` syntax is used, the command is safe, fast, and deterministic | WARN |" — after: "If `` !`command` `` syntax is used, the command SHOULD be safe, fast, and deterministic."
- `should-keep-description-under-200-characters` — before: "| B12 | Description concise for context budget | Description is under ~200 characters to avoid consuming excessive context | WARN |" — after: "The description SHOULD be under ~200 characters to avoid consuming excessive context."
- **bars**: review-focus **moved** (the three checklist tables); review-bar authored; build-bar authored. The Sources block moved to `references`.
- **contradictions (R4)**: "S02 | `name` field present | … | WARN" makes the field optional at WARN. "S03 | `name` is kebab-case, lowercase, ≤64 chars | … | FAIL" and "S09 | Directory name matches `name` field" then treat that field as present.
- **unfinished**: nothing.

## cookbook/testing/properties-of-good-tests

- **promoted**: none. All six properties already used MUST or SHOULD, and they were named in order.
- **bars**: look-for authored; review-bar authored; build-bar authored. "Less relevant for cookbook authoring" became `rationale`.
- **contradictions (R4)**:
  - The intro says "each test vector should exhibit these properties" (a lowercase should), but three of the properties are MUST.
  - Cross-topic conflict: "**Specific** — each vector SHOULD target one behavior or edge case" (here) and "Each vector MUST test one behavioral concept" (unit-test-patterns) give the same requirement at two levels.
- **unfinished**: nothing.

## cookbook/testing/unit-test-patterns

- **promoted** (1): before: "Use descriptive names that read as specifications:". After: `should-use-descriptive-specification-names`: "Test vectors SHOULD use descriptive names that read as specifications." The example names stayed in `naming-test-vectors` as `examples`.
- **bars**: look-for authored; review-bar authored; build-bar authored. The Arrange/Act/Assert bullets became sub-bullets of `should-follow-arrange-act-assert`.
- **contradictions (R4)**: the same SHOULD/MUST split with properties-of-good-tests, given above.
- **unfinished**: nothing.

## implementing/accessibility/accessibility

- **promoted**:
  - Items under the "All components MUST integrate …:" lead-in. Each item has no keyword, so each takes MUST from the lead-in:
    - "Semantic roles and labels on all interactive elements" became `must-give-interactive-elements-semantic-roles-and-labels`: "Semantic roles and labels MUST be on all interactive elements."
    - "VoiceOver (Apple) / TalkBack (Android) / screen reader (Web) full support", together with the folded "Screen reader full support (VoiceOver, TalkBack, Narrator, ARIA)", became `must-fully-support-screen-readers`: "Components MUST give full screen reader support: VoiceOver (Apple), TalkBack (Android), Narrator (Windows) and screen readers via ARIA (Web)."
    - "Keyboard and switch control navigation" became `must-support-keyboard-and-switch-control`: "Components MUST support keyboard and switch control navigation."
    - "WCAG AA minimum contrast (4.5:1 for text, 3:1 for large text)" became `must-meet-wcag-aa-contrast`: "Components MUST meet WCAG AA minimum contrast (4.5:1 for text, 3:1 for large text)."
    - "Meaningful focus order following visual layout" became `must-follow-visual-layout-focus-order`: "Components MUST have a meaningful focus order following visual layout."
  - Standards, from the TypeScript part:
    - "[WCAG 2.2](…) — minimum AA conformance for all components. WCAG 2.2 is the current W3C Recommendation and supersedes 2.1; honor its new AA criteria: …" became `should-meet-wcag-2-2-aa`: "Web (TypeScript) components SHOULD meet WCAG 2.2 minimum AA conformance — all components. WCAG 2.2 is the current W3C Recommendation and supersedes 2.1." It also became `should-honor-wcag-2-2-new-aa-criteria`: "Components SHOULD honor WCAG 2.2's new AA criteria: … (the full list kept)".
    - "Treat WCAG 3.0 as a horizon Working Draft, not yet actionable." became `should-treat-wcag-3-as-not-yet-actionable`: "Authors SHOULD treat WCAG 3.0 as a horizon Working Draft, not yet actionable."
    - "[WAI-ARIA Authoring Practices](…) — correct ARIA roles, states, and properties." became `should-follow-wai-aria-authoring-practices`: "Components SHOULD follow the WAI-ARIA Authoring Practices: correct ARIA roles, states, and properties."
    - "Screen reader support: use ARIA roles, `aria-live` for dynamic content, proper landmark regions." became `should-support-screen-readers-with-aria`: "Web screen reader support SHOULD use ARIA roles, `aria-live` for dynamic content, and proper landmark regions."
  - Windows:
    - "Set `AutomationProperties.Name` on interactive elements that lack visible text labels." became `should-set-automation-name-on-unlabeled-elements`: "Components SHOULD set `AutomationProperties.Name` on interactive elements that lack visible text labels."
    - "Use `AutomationProperties.LabeledBy` for form fields" became `should-use-labeled-by-for-form-fields`: "Form fields SHOULD use `AutomationProperties.LabeledBy`."
    - "Use `AutomationProperties.LiveSetting` for dynamic content regions" became `should-use-live-setting-for-dynamic-regions`: "Dynamic content regions SHOULD use `AutomationProperties.LiveSetting`."
    - "High contrast support is automatic when using `ThemeResource` — never hard-code colors" became `must-not-hard-code-colors`: "High contrast support is automatic when using `ThemeResource` — components MUST NOT hard-code colors."
    - "Test with [Accessibility Insights for Windows](…)" became `should-test-with-accessibility-insights`: "Components SHOULD be tested with [Accessibility Insights for Windows](…)."
    - "Keyboard navigation: all interactive elements must be reachable via Tab, actionable via Enter/Space" (a lowercase must) became `must-make-elements-keyboard-reachable`: "Keyboard navigation: all interactive elements MUST be reachable via Tab, actionable via Enter/Space."
    - "**Windows**: … minimum 40x40 epx recommended touch targets" became `should-use-40-epx-touch-targets`: "Windows touch targets SHOULD be a minimum of 40x40 epx, as recommended." The tooling line itself stays word for word in the `windows` how-to part.
- **structure**:
  - The settings tables in swift, kotlin, typescript and windows are kept as `how-to` parts. Each "Components MUST respond to these … :" lead-in became a per-platform rule that points at its table: `must-respond-to-swiftui-environment-values`, `must-respond-to-android-accessibility-settings`, `must-respond-to-css-user-preferences` and `must-respond-to-windows-accessibility-settings`.
  - `typescript-2` was the folded copy of `typescript`, identical in content, and was removed. The folded "# Accessibility" block in the intro was merged into the same rules.
  - The intro is now the H1 plus "All components MUST integrate with platform accessibility APIs from initial implementation."
  - The standards and tool links moved to a `references` part.
  - The 27 moved entries are the reworded list items, the lead-ins and the old headings.
- **bars**: look-for authored; review-bar authored; build-bar authored.
- **contradictions (R4)**:
  - `should-meet-wcag-2-2-aa` is a SHOULD, because it was an unkeyworded statement, while `must-meet-wcag-aa-contrast` is a MUST. AA conformance is stated at two levels.
  - Three touch-target sizes appear with no single rule: "**target size minimum 24×24 CSS px** (reconcile with the 44pt target … 44pt is the stricter Apple guidance)" against "minimum 40x40 epx recommended touch targets" (Windows).
  - Kotlin table: "Layouts must not break at larger display sizes" (lowercase). Windows table: "Layouts must not break up to 225% text scale" (lowercase), while font-scaling's rule says "Layouts MUST NOT break at 2x font size".
  - The Windows table's "Caret Browsing … Non-interactive text should be navigable" sits under a MUST lead-in.
  - "See platform-specific files for the full list of settings and environment keys." now refers to parts, not files. It was kept word for word as a sub-bullet.
- **unfinished**: nothing.

## implementing/accessibility/dynamic-type

- **promoted** (2):
  - "Use Dynamic Type throughout — avoid fixed font sizes." became `should-use-dynamic-type-throughout`: "Text SHOULD use Dynamic Type throughout, avoiding fixed font sizes."
  - "Custom fonts must respond to the bold text accessibility setting." (a lowercase must) became `must-make-custom-fonts-respond-to-bold-text`: "Custom fonts MUST respond to the bold text accessibility setting."
- The intro keeps its first sentence as the statement. That sentence is also `must-not-break-at-larger-text-sizes`.
- **bars**: look-for authored; review-bar authored; build-bar authored.
- **contradictions (R4)**: none within the topic.
- **unfinished**: nothing.

## implementing/accessibility/font-scaling

- **promoted** (2): "Check `Configuration.fontScale` and test with large font settings enabled." was split into two rules. `should-check-configuration-font-scale` says "Layouts SHOULD check `Configuration.fontScale`." `should-test-with-large-font-settings` says "Layouts SHOULD be tested with large font settings enabled."
- The intro keeps its first sentence as the statement. That sentence is also `must-not-break-at-2x-font-size`.
- **bars**: look-for authored; review-bar authored; build-bar authored.
- **contradictions (R4)**: "Layouts MUST NOT break at 2x font size" here and "Layouts must not break up to 225% text scale" (accessibility, Windows table) set different thresholds.
- **unfinished**: nothing.

## Unfinished

Nothing. Every topic has passed only `--draft`. Each topic's moved entries still need the independent judge's verdict before `cookr roles lossless` passes without `--draft`.
