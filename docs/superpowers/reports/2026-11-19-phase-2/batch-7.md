# Phase 2 batch 7 report

Format-only conversion of the 16 batch-7 topics to roled parts. All 16 are converted and committed; unit-test-patterns was converted after a rename removed its skill-name collision (see its two sections).

## agent-structure-reference

`cookbook/guidelines/implementing/skills-and-agents/agent-structure-reference`: commit c9fb924; 2 rules, 1 moved, 0 obsolete.

**Promoted**:

- none

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Unfinished**: none.

## authoring-skills-and-rules

`cookbook/guidelines/implementing/skills-and-agents/authoring-skills-and-rules`: commit 255cdb89; 53 rules, 49 moved, 0 obsolete.

**Promoted**:

- `should-read-skills-table-before-creating-a-skill`: before "**Check the inventory first** -- Read the skills table in CLAUDE.md before creating a new skill."; after "The author SHOULD read the skills table in CLAUDE.md before creating a new skill (check the inventory first)."
- `should-not-duplicate-a-skill-purpose`: before "Do not duplicate an existing skill's purpose."; after "A new skill SHOULD NOT duplicate an existing skill's purpose."
- `should-confirm-new-skill-name-and-purpose`: before "If the skill is not already listed, confirm the name and purpose with the user before proceeding."; after "If the skill is not already listed, the author SHOULD confirm the name and purpose with the user before proceeding."
- `should-increment-skill-version-by-semver`: before "Increment the version on every change following semver: patch for fixes, minor for new behavior, major for breaking changes."; after "The version SHOULD be incremented on every change following semver: patch for fixes, minor for new behavior, major for breaking changes."
- `should-warn-when-loaded-skill-may-be-stale`: before "If the versions differ, warn the user that the loaded skill may be stale."; after "If the versions differ, the skill SHOULD warn the user that the loaded skill may be stale."
- `should-not-block-on-version-mismatch`: before "Continue running -- do not block execution."; after "On a version mismatch the skill SHOULD continue running and SHOULD NOT block execution."
- `should-not-describe-arguments-in-prose`: before "**Use `$ARGUMENTS`** -- Do not describe argument handling in prose."; after "A skill SHOULD NOT describe argument handling in prose."
- `should-use-arguments-variables`: before "Use `$ARGUMENTS`, `$0`, `$1` for input."; after "A skill SHOULD use `$ARGUMENTS`, `$0`, `$1` for input."
- `should-use-claude-skill-dir`: before "**Use `${CLAUDE_SKILL_DIR}`** -- Reference the skill's own supporting files with `${CLAUDE_SKILL_DIR}`."; after "A skill SHOULD reference its own supporting files with `${CLAUDE_SKILL_DIR}`."
- `should-use-repo-relative-cookbook-paths`: before "Use repo-relative paths or `../agenticdevelopercookbook/` paths for cookbook content."; after "A skill SHOULD use repo-relative paths or `../agenticdevelopercookbook/` paths for cookbook content."
- `should-keep-skill-description-under-200-characters`: before "**Description under 200 characters** -- The skill description is loaded into every session's context window." / "Keep it short and include natural trigger keywords so the model invokes the skill when appropriate."; after "The skill description SHOULD be kept short, under 200 characters."
- `should-include-trigger-keywords-in-description`: before "Keep it short and include natural trigger keywords so the model invokes the skill when appropriate."; after "The skill description SHOULD include natural trigger keywords so the model invokes the skill when appropriate."
- `should-use-one-atomic-permission-prompt`: before "**Atomic permission prompt** -- Before any file modifications, present a single yes/no prompt listing every file to be written and every command to be run, with reasons."; after "Before any file modifications, a skill SHOULD present a single yes/no prompt listing every file to be written and every command to be run, with reasons: one atomic permission prompt."
- `should-check-prerequisites-first`: before "**Error handling** -- Check prerequisites before starting work."; after "As error handling, a skill SHOULD check prerequisites before starting work."
- `should-stop-on-missing-prerequisites`: before "If required files are missing or the environment is misconfigured, stop immediately with a useful error message."; after "If required files are missing or the environment is misconfigured, the skill SHOULD stop immediately with a useful error message."
- `should-handle-invalid-arguments-explicitly`: before "Handle invalid arguments explicitly rather than failing silently."; after "A skill SHOULD handle invalid arguments explicitly rather than failing silently."
- `must-not-disable-model-invocation-on-called-skills`: before "Do NOT set it on skills that other skills need to call via the Skill tool."; after "`disable-model-invocation` MUST NOT be set on skills that other skills need to call via the Skill tool."
- `should-not-fork-chainable-skills`: before "**No `context: fork` on chainable skills** -- Forked skills cannot invoke other skills or write files visible to the caller."; after "Chainable skills SHOULD have no `context: fork`."
- `should-fork-only-isolated-read-heavy-tasks`: before "Only use `context: fork` for isolated, read-heavy tasks that return a report."; after "A skill SHOULD only use `context: fork` for isolated, read-heavy tasks that return a report."
- `should-keep-one-authoritative-source`: before "**Don't duplicate between body and references** -- Maintain one authoritative source."; after "A skill SHOULD NOT duplicate content between its body and its references but SHOULD maintain one authoritative source."
- `must-not-overlap-body-and-references`: before "Never have both with overlapping content that can drift out of sync."; after "A skill MUST NOT have both a body and references with overlapping content that can drift out of sync."
- `must-lint-skill-after-every-change`: before "**Always lint after creating or modifying** -- Run `/lint-skill <path>` after every change."; after "The author MUST always run `/lint-skill <path>` after creating or modifying a skill, after every change."
- `should-fix-all-skill-lint-fails`: before "Fix all FAILs before considering the skill complete."; after "The author SHOULD fix all FAILs before considering the skill complete."
- `should-present-skill-lint-warns`: before "Present WARNs to the user for review."; after "The author SHOULD present WARNs to the user for review."
- `should-add-new-skill-to-claude-md-and-readme`: before "**Update CLAUDE.md and README.md** -- After creating a skill, add it to the skills table in both files."; after "The author SHOULD update CLAUDE.md and README.md after creating a skill, adding it to the skills table in both files."
- `should-list-every-referenced-file-path`: before "**Explicit file paths** -- If the rule instructs the LLM to "read the principles" or "check the guidelines," list every file path it needs to read."; after "If the rule instructs the LLM to "read the principles" or "check the guidelines," it SHOULD list every explicit file path it needs to read."
- `should-keep-one-concern-per-rule`: before "**Single concern per rule** -- Each rule addresses one topic: planning, implementing, permissions, versioning, committing, etc."; after "Each rule SHOULD address a single concern, one topic: planning, implementing, permissions, versioning, committing, etc."
- `should-not-combine-concerns-in-one-rule-file`: before "Do not combine unrelated concerns into a single rule file."; after "Unrelated concerns SHOULD NOT be combined into a single rule file."
- `should-include-verification-steps`: before "**Enforcement mechanism** -- Do not just state "do X." Include verification steps that confirm X was actually done."; after "A rule SHOULD NOT just state "do X" but SHOULD include verification steps that confirm X was actually done, as an enforcement mechanism."
- `should-avoid-subjective-language`: before "**Deterministic instructions** -- Avoid subjective language like "appropriate," "as needed," or "if it makes sense." Be specific enough that two independent sessions following the rule produce consistent, comparable results."; after "A rule SHOULD give deterministic instructions and avoid subjective language like "appropriate," "as needed," or "if it makes sense.""
- `should-be-specific-enough-for-consistent-results`: before "**Deterministic instructions** -- Avoid subjective language like "appropriate," "as needed," or "if it makes sense." Be specific enough that two independent sessions following the rule produce consistent, comparable results."; after "A rule SHOULD be specific enough that two independent sessions following the rule produce consistent, comparable results."
- `should-reapply-everything-on-same-selection`: before "**Same-selection = repair** -- When a user re-selects the current configuration (e.g., re-runs a setup skill with the same parameters), re-apply everything from scratch."; after "When a user re-selects the current configuration (e.g., re-runs a setup skill with the same parameters), the rule SHOULD re-apply everything from scratch (same-selection = repair)."
- `should-not-skip-steps-on-same-selection`: before "Do not skip steps with "already done" -- treat it as a repair operation."; after "On a same selection, steps SHOULD NOT be skipped with "already done"; it SHOULD be treated as a repair operation."
- `should-name-requirements-not-number-them`: before "**Named requirements, not numbered** -- Use descriptive kebab-case names for requirements, not sequential identifiers like REQ-001."; after "Requirements SHOULD NOT be numbered and SHOULD use descriptive kebab-case names for requirements, not sequential identifiers like REQ-001."
- `must-lint-rule-after-every-change`: before "**Always lint after creating or modifying** -- Run `/lint-rule <path>` after every change."; after "The author MUST always run `/lint-rule <path>` after creating or modifying a rule, after every change."
- `should-fix-all-rule-lint-fails`: before "Fix all FAILs before considering the rule complete."; after "The author SHOULD fix all FAILs before considering the rule complete."
- `should-present-rule-lint-warns`: before "Present WARNs to the user for review."; after "The author SHOULD present WARNs to the user for review."
- `should-scope-agent-tool-access`: before "**Scope tool access** -- Use the `tools` or `disallowedTools` frontmatter fields to restrict what the agent can do."; after "An agent SHOULD use the `tools` or `disallowedTools` frontmatter fields to restrict what the agent can do."
- `should-set-max-turns`: before "**Set `maxTurns`** -- Prevent unbounded execution by setting a turn limit appropriate to the task complexity."; after "An agent SHOULD set `maxTurns`, a turn limit appropriate to the task complexity, to prevent unbounded execution."
- `should-write-a-clear-system-prompt`: before "**Clear system prompt** -- The markdown body IS the agent's instruction set." / "Make the instructions focused, unambiguous, and structured."; after "An agent's instructions SHOULD be a clear system prompt: focused, unambiguous, and structured."
- `must-lint-agent-after-every-change`: before "**Always lint** -- Run `/lint-agent <path>` after creating or modifying an agent."; after "The author MUST always run `/lint-agent <path>` after creating or modifying an agent."
- `should-fix-all-agent-lint-fails`: before "Fix all FAILs."; after "The author SHOULD fix all FAILs from `/lint-agent`."
- `should-design-skills-single-purpose-and-versioned`: after "Skills SHOULD be designed as single-purpose, versioned extensions." (its source sentence stays in place in its original part)
- `should-keep-rules-minimal-deterministic-side-effect-free`: after "Rules SHOULD be kept minimal, deterministic, and side-effect-free." (its source sentence stays in place in its original part)
- `should-check-inventory-before-creating`: after "The inventory SHOULD be checked before creating anything new." (its source sentence stays in place in its original part)

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Notes**: Flag: "Do NOT set it on skills that other skills need to call" was promoted to MUST NOT; its wording could also be read as SHOULD NOT.

**Unfinished**: none.

## codex-configuration

`cookbook/guidelines/implementing/skills-and-agents/codex-configuration`: commit 484e1aad; 19 rules, 5 moved, 0 obsolete.

**Promoted**:

- `should-disable-skills-via-skills-config`: before "Disable a skill without deleting it with a `[[skills.config]]` entry in `~/.codex/config.toml`, and restart Codex."; after "A skill SHOULD be disabled without deleting it with a `[[skills.config]]` entry in `~/.codex/config.toml`, and Codex restarted."
- `should-put-config-where-codex-looks`: after "Each kind of configuration (settings in `config.toml`, instructions in `AGENTS.md`, reusable procedures in skills) SHOULD be put in the place Codex looks for it." (its source sentence stays in place in its original part)
- `should-keep-shared-config-in-repo`: after "What the team shares SHOULD be kept inside the repository." (its source sentence stays in place in its original part)
- `should-not-repeat-parent-in-nested-agents-md`: after "Nested `AGENTS.md` files SHOULD add to the parent rather than repeat it." (its source sentence stays in place in its original part)
- `should-give-agents-override-a-reason`: after "An `AGENTS.override.md` SHOULD have a reason." (its source sentence stays in place in its original part)
- `should-put-repository-skills-under-agents-skills`: after "Repository skills SHOULD live under `.agents/skills`." (its source sentence stays in place in its original part)

**Bars**: look-for moved; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Notes**: The existing review text became `look-for.md`.

**Unfinished**: none.

## context-and-memory-management

`cookbook/guidelines/implementing/skills-and-agents/context-and-memory-management`: commit e6c9b051; 19 rules, 4 moved, 0 obsolete.

**Promoted**:

- `should-keep-only-behavior-changing-memory`: before "An overstuffed memory file dilutes attention and causes the agent to ignore the rules that matter — keep only what changes behavior, and prune regularly."; after "A memory file SHOULD keep only what changes behavior."
- `should-prune-memory-regularly`: before "An overstuffed memory file dilutes attention and causes the agent to ignore the rules that matter — keep only what changes behavior, and prune regularly."; after "Memory files SHOULD be pruned regularly."
- `should-treat-a-bigger-window-as-headroom`: before "Treat a bigger window as more headroom, not a license to stop curating — this is a durable property, not a vendor-specific number."; after "The agent SHOULD treat a bigger window as more headroom, not a license to stop curating — this is a durable property, not a vendor-specific number."

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Notes**: Flag: should-retrieve-context-just-in-time was promoted to SHOULD; its wording could also carry MUST.

**Unfinished**: none.

## copilot-configuration

`cookbook/guidelines/implementing/skills-and-agents/copilot-configuration`: commit 5a4baff6, then efd9d59b; 14 rules, 1 moved, 0 obsolete.

**Promoted**:

- `should-put-everywhere-guidance-in-one-file`: after "Guidance that applies everywhere SHOULD be put in one file." (its source sentence stays in place in its original part)
- `should-match-intended-files-with-apply-to`: after "Each path-specific file SHOULD have an `applyTo` glob that matches the files it intends." (its source sentence stays in place in its original part)
- `should-set-exclude-agent-only-on-purpose`: after "`excludeAgent` SHOULD be set only on purpose." (its source sentence stays in place in its original part)
- `should-not-carry-conflicting-agent-files`: after "A repository SHOULD NOT carry both an `AGENTS.md` and a `CLAUDE.md` or `GEMINI.md` with different content." (its source sentence stays in place in its original part)
- `should-put-repeatable-tasks-in-prompt-files`: after "Repeatable tasks SHOULD be put in prompt files." (its source sentence stays in place in its original part)

**Bars**: look-for moved; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Notes**: The review checklist became `look-for.md`, with lines added for the rules it did not cover. The never-clobber link moved into `references.md`. efd9d59b restored the source's own word "placeholder" (`${input:name:placeholder}`) after FM-13 was narrowed; it was approved with no further bump.

**Unfinished**: none.

## kimi-configuration

`cookbook/guidelines/implementing/skills-and-agents/kimi-configuration`: commit c8417b36; 10 rules, 4 moved, 0 obsolete.

**Promoted**:

- `should-place-agents-md-where-it-applies`: after "`AGENTS.md` SHOULD be placed at the root or in the subdirectory it covers." (its source sentence stays in place in its original part)
- `should-put-repository-skills-under-the-root`: after "Repository skills SHOULD be in `.kimi-code/skills/` or `.agents/skills/` under the repository root." (its source sentence stays in place in its original part)
- `should-not-shadow-a-skill-by-accident`: after "A new skill name SHOULD NOT shadow a skill at a lower priority level by accident." (its source sentence stays in place in its original part)

**Bars**: look-for moved; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Notes**: The review text became `look-for.md`. Note: the review line on secrets also names "base URLs", which goes beyond the API-key rule; it is kept as written and not made a rule.

**Unfinished**: none.

## never-clobber-user-files

`cookbook/guidelines/implementing/skills-and-agents/never-clobber-user-files`: commit 7df06fdf; 14 rules, 11 moved, 0 obsolete.

**Promoted**:

- `should-namespace-everything-shipped`: before "Namespace everything you ship."; after "Everything you ship SHOULD be namespaced. Use a name that carries your project or team prefix (`acme-review`, not `review`), or a directory that is yours (`acme/review/SKILL.md`), so a collision with a user's own name is unlikely."
- `should-check-before-writing`: before "Check before you write."; after "An installer SHOULD check before it writes. If the target exists, compare it to what you would write. If it is identical, do nothing. If it is a file you installed earlier (see the marker below), update it. If it is anything else, leave it, report the conflict by name, and stop for that file."
- `should-mark-what-is-installed`: before "Mark what you install."; after "An installer SHOULD mark what it installs. Put a recognizable marker in each file (a frontmatter field or a comment naming the package and version) or keep a manifest of installed paths, so an update and an uninstall touch only your files."
- `must-not-rename-or-remove-the-users-file`: before "Never fix a collision by renaming the user's file or by removing it."; after "A collision MUST NOT be fixed by renaming the user's file or by removing it. Rename or skip your own."
- `should-uninstall-only-own-unchanged-files`: before "Uninstall removes only files recorded as yours, and only if they still match what you wrote."; after "Uninstall SHOULD remove only files recorded as yours, and only if they still match what you wrote. A file the user has edited is left in place and reported."
- `should-check-in-the-installer`: before "Do the check in the installer, not in the shipped file."; after "The check SHOULD be done in the installer, not in the shipped file."
- `must-not-rely-on-a-unique-name`: before "A skill must not rely on being the only one with its name."; after "A skill MUST NOT rely on being the only one with its name."
- `should-make-installs-idempotent`: before "Make installs idempotent: running one twice leaves the same files and reports no conflict with itself."; after "Installs SHOULD be idempotent: running one twice leaves the same files and reports no conflict with itself."
- `should-choose-names-unlikely-to-repeat-across-levels`: before "Choose names that are unlikely to repeat across levels, and document the shadowing in the install report."; after "Shipped files SHOULD have names that are unlikely to repeat across levels."
- `should-document-shadowing-in-the-install-report`: before "Choose names that are unlikely to repeat across levels, and document the shadowing in the install report."; after "The install report SHOULD document the shadowing."
- `should-print-one-line-per-skipped-file`: before "Print one line per skipped file: the path, why it was skipped, and what the user can do (rename theirs, or install with your own prefix)."; after "An installer SHOULD print one line per skipped file: the path, why it was skipped, and what the user can do (rename theirs, or install with your own prefix)."
- `should-exit-non-zero-on-a-skipped-conflict`: before "Exit with a non-zero status when any file was skipped for a conflict, so automation notices."; after "An installer SHOULD exit with a non-zero status when any file was skipped for a conflict, so automation notices."
- `should-not-duplicate-a-built-in-name`: after "A shipped name SHOULD NOT duplicate a common built-in name." (its source sentence stays in place in its original part)

**Bars**: look-for moved; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Notes**: The review text became `look-for.md`.

**Unfinished**: none.

## performance

`cookbook/guidelines/implementing/skills-and-agents/performance`: commit 1750d1e0; 22 rules, 17 moved, 0 obsolete.

**Promoted**:

- `should-use-shell-scripts-for-deterministic-work`: before "If the operation is repeatable and has a known outcome, use a shell script."; after "If the operation is repeatable and has a known outcome, you SHOULD use a shell script."
- `should-extract-deterministic-skill-steps-into-scripts`: before "**In skills**: Extract deterministic steps into shell scripts in the skill's directory."; after "In skills, deterministic steps SHOULD be extracted into shell scripts in the skill's directory."
- `should-use-hooks-for-validation-and-formatting`: before "Use PreToolUse hooks for validation, PostToolUse hooks for formatting and linting."; after "You SHOULD use PreToolUse hooks for validation, PostToolUse hooks for formatting and linting."
- `should-have-agents-call-scripts-for-deterministic-subtasks`: before "**In agents**: When an agent's task includes deterministic subtasks, have it call shell scripts rather than reasoning through known operations."; after "When an agent's task includes deterministic subtasks, it SHOULD call shell scripts rather than reasoning through known operations."
- `should-consider-downgrading-simple-subtasks`: before "When a subtask is simple enough for a smaller model, consider downgrading."; after "When a subtask is simple enough for a smaller model, you SHOULD consider downgrading."
- `should-measure-not-assume`: before "But measure — don't assume."; after "But measure — don't assume: a downgrade SHOULD be measured, and its benefit SHOULD NOT be assumed."
- `should-verify-three-things-before-downgrading`: before "Before selecting a smaller model for a subtask, verify three things:"; after "Before selecting a smaller model for a subtask, you SHOULD verify three things: token efficiency, latency and correctness."
- `should-load-only-what-the-current-step-needs`: before "Load only what's needed for the current step."; after "You SHOULD load only what's needed for the current step."
- `must-not-load-deep-reference-unconditionally`: before "Never loaded unconditionally."; after "Deep reference (research, full cookbook) is never loaded unconditionally: it MUST NOT be."
- `should-pick-the-cheapest-model-that-handles-the-task`: after "You SHOULD pick the cheapest model that handles the task." (its source sentence stays in place in its original part)
- `should-ask-the-user-when-unclear`: after "When it is unclear whether to downgrade, you SHOULD ask the user and present the tradeoff." (its source sentence stays in place in its original part)
- `should-not-silently-downgrade`: after "You SHOULD NOT silently downgrade." (its source sentence stays in place in its original part)

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Notes**: Flag: "Do not silently downgrade" was promoted to SHOULD NOT; it could also be read as MUST NOT.

**Unfinished**: none.

## rule-structure-reference

`cookbook/guidelines/implementing/skills-and-agents/rule-structure-reference`: commit 2af86cba; 25 rules, 27 moved, 0 obsolete.

**Promoted**:

- `should-name-rule-files-lowercase-kebab-case`: before "The file name should be descriptive and lowercase kebab-case (e.g., `testing.md`, `api-design.md`)."; after "The file name SHOULD be descriptive and lowercase kebab-case (e.g., `testing.md`, `api-design.md`)."
- `may-include-a-title-or-version-in-frontmatter`: before "Optional frontmatter may include a title or version, but there is no enforced schema."; after "Optional frontmatter MAY include a title or version, but there is no enforced schema."
- `should-have-a-clear-title`: before "Clear title/heading identifying the rule's purpose"; after "A rule SHOULD have a clear title/heading identifying the rule's purpose."
- `should-number-procedural-steps`: before "Numbered or clearly separated steps if procedural"; after "A rule SHOULD have numbered or clearly separated steps if procedural."
- `should-give-distinct-concerns-their-own-sections`: before "Sections with headings for distinct concerns"; after "A rule SHOULD have sections with headings for distinct concerns."
- `should-be-deterministic`: before "**Deterministic**: The LLM should be able to follow the rule without ambiguity"; after "A rule SHOULD be deterministic: the LLM SHOULD be able to follow the rule without ambiguity."
- `should-list-every-referenced-file`: before "**Explicit file references**: If the rule says "read the principles," it lists every file path"; after "A rule SHOULD have explicit file references: if the rule says "read the principles," it lists every file path."
- `should-be-self-contained-or-clearly-scoped`: before "**Self-contained or clearly scoped**: Either contains all needed information or explicitly references where to find it"; after "A rule SHOULD be self-contained or clearly scoped: either contains all needed information or explicitly references where to find it."
- `should-not-use-vague-directives`: before "**No vague directives**: "Handle errors appropriately" is bad. "Validate user input at the API boundary, return HTTP 400 with a message for invalid input" is good."; after "A rule SHOULD NOT use vague directives: "Handle errors appropriately" is bad. "Validate user input at the API boundary, return HTTP 400 with a message for invalid input" is good."
- `should-avoid-vague-rules`: before "**Vague rules**: "Write good code" — not actionable"; after "Vague rules SHOULD be avoided: "Write good code" — not actionable."
- `should-avoid-contradictory-rules`: before "**Contradictory rules**: "Always do X" then later "Never do X""; after "Contradictory rules SHOULD be avoided: "Always do X" then later "Never do X"."
- `should-avoid-unbounded-scope`: before "**Unbounded scope**: Rule tries to govern everything instead of a specific concern"; after "Unbounded scope SHOULD be avoided: a rule tries to govern everything instead of a specific concern."
- `should-avoid-missing-file-paths`: before "**Missing file paths**: Rule says "read the guidelines" without listing which files"; after "Missing file paths SHOULD be avoided: a rule says "read the guidelines" without listing which files."
- `should-avoid-duplicating-claude-md`: before "**Duplicating CLAUDE.md**: Rule content that belongs in project instructions, not a standalone rule"; after "Duplicating CLAUDE.md SHOULD be avoided: rule content that belongs in project instructions, not a standalone rule."
- `should-avoid-rules-with-no-enforcement-mechanism`: before "**No enforcement mechanism**: Rule states preferences but provides no steps to verify compliance"; after "A rule with no enforcement mechanism SHOULD be avoided: it states preferences but provides no steps to verify compliance."
- `should-keep-per-turn-content-minimal`: before "Keep this minimal."; after "You SHOULD keep per-turn content, the content in the rule file itself, minimal."
- `should-put-large-reference-material-on-demand`: before "Use this for large reference material."; after "You SHOULD use per-session external files read on demand for large reference material."
- `should-keep-rule-files-under-200-lines`: before "**Target under 200 lines / ~8KB** per rule file." / "If larger, move content to skills or external references."; after "The target per rule file SHOULD be under 200 lines / ~8KB. If larger, its content SHOULD move to skills or external references."
- `should-inline-small-and-reference-large`: before "**Inline small, reference large.** A 5-line summary table belongs in the rule."; after "Small content SHOULD be inlined and large content referenced. A 5-line summary table belongs in the rule. A 200-line guideline belongs in an external file read on demand."
- `should-not-duplicate-across-rules`: before "**Don't duplicate across rules.** Two rules covering the same concept means Claude processes it twice per turn."; after "Rules SHOULD NOT duplicate content across rules."
- `should-use-globs-for-file-specific-rules`: before "**Use `globs` frontmatter** for rules that only apply to specific file patterns (e.g., `globs: .claude/**`)."; after "Rules that only apply to specific file patterns SHOULD use `globs` frontmatter (e.g., `globs: .claude/**`)."
- `should-avoid-mandatory-multi-file-reads`: before "**Avoid mandatory multi-file reads.** Rules that require reading 6+ files before any work begins create high entry cost." / "Prefer summaries, on-demand reads, or iterative approaches."; after "Mandatory multi-file reads SHOULD be avoided. You SHOULD prefer summaries, on-demand reads, or iterative approaches."
- `should-inline-mostly-metadata-files`: before "**Watch frontmatter ratios in referenced files.** If an external file is >50% YAML metadata, inline the content instead."; after "Frontmatter ratios in referenced files SHOULD be watched. If an external file is >50% YAML metadata, its content SHOULD be inlined instead."

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Notes**: Lowercase "should"/"may" criteria and the anti-patterns list were promoted to SHOULD/MAY (anti-patterns as "SHOULD be avoided").

**Unfinished**: none.

## skill-structure-reference

`cookbook/guidelines/implementing/skills-and-agents/skill-structure-reference`: commit 39486628; 7 rules, 6 moved, 0 obsolete.

**Promoted**:

- `should-load-reference-content-automatically-only-when-meant-to`: before "Use `user-invocable: false` if it should only load automatically."; after "Reference content SHOULD use `user-invocable: false` if it should only load automatically."
- `should-disable-model-invocation-for-side-effect-tasks`: before "Use `disable-model-invocation: true` for side-effect operations."; after "Task content SHOULD use `disable-model-invocation: true` for side-effect operations."
- `should-keep-skill-md-under-500-lines`: before "Keep SKILL.md under 500 lines; put detailed content in references/"; after "You SHOULD keep SKILL.md under 500 lines; you SHOULD put detailed content in references/"
- `should-reference-supporting-files-with-skill-dir`: before "Use `${CLAUDE_SKILL_DIR}` to reference supporting files"; after "You SHOULD use `${CLAUDE_SKILL_DIR}` to reference supporting files"
- `should-use-natural-keywords-in-the-description`: before "Description should use keywords users would naturally say"; after "Description SHOULD use keywords users would naturally say"
- `should-name-supporting-files-lowercase`: before "Supporting files in references/, scripts/, examples/ should use lowercase descriptive names"; after "Supporting files in references/, scripts/, examples/ SHOULD use lowercase descriptive names"

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Unfinished**: none.

## property-based-testing

`cookbook/guidelines/implementing/testing/property-based-testing`: commit 9734bac5; 3 rules, 3 moved, 0 obsolete.

**Promoted**:

- `should-use-property-tests-where-a-property-holds-for-all-inputs`: before "When to use: parsers, serializers, data transformers, encoders/decoders, validators — anything" / "where "for all valid inputs X, property Y holds.""; after "Property-based testing SHOULD be used for parsers, serializers, data transformers, encoders/decoders, validators — anything where "for all valid inputs X, property Y holds.""
- `should-describe-properties-instead-of-examples`: after "Instead of testing specific examples, you SHOULD describe properties of the output and let the framework generate hundreds of random inputs to try to falsify them." (its source sentence stays in place in its original part)

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Unfinished**: none.

## swift-testing

`cookbook/guidelines/implementing/testing/swift-testing`: commit e7edc861; 22 rules, 20 moved, 0 obsolete.

**Promoted**:

- `should-keep-ui-and-performance-tests-in-xctest`: before "Keep those in XCTest."; after "You SHOULD keep UI tests (`XCUIApplication`) and XCTest-based performance measurement (`measure {}`) in XCTest."
- `should-use-expect-for-ordinary-assertions`: before "**`#expect(expr)`** records a failure but continues; use it for ordinary assertions."; after "You SHOULD use `#expect(expr)`, which records a failure but continues, for ordinary assertions."
- `should-use-require-for-preconditions`: before "**`#require(expr)`** throws and halts the test when the expectation fails; use it for preconditions whose failure makes the rest of the test meaningless."; after "You SHOULD use `#require(expr)`, which throws and halts the test when the expectation fails, for preconditions whose failure makes the rest of the test meaningless."
- `should-assert-errors-with-expect-throws`: before "Use **`#expect(throws:)`** / `#require(throws:)` to assert error behavior instead of `do/catch`."; after "You SHOULD use `#expect(throws:)` / `#require(throws:)` to assert error behavior instead of `do/catch`."
- `should-group-related-tests-with-suite`: before "Group related tests with **`@Suite`** on a type (often a `struct`)."; after "You SHOULD group related tests with `@Suite` on a type (often a `struct`)."
- `should-pass-arguments-for-many-inputs`: before "Pass `arguments:` to run one test body over many inputs: `@Test(arguments: [1, 2, 3])`."; after "You SHOULD pass `arguments:` to run one test body over many inputs: `@Test(arguments: [1, 2, 3])`."
- `should-zip-paired-inputs`: before "Use `zip(...)` for paired inputs to avoid an unintended Cartesian product across two collections."; after "You SHOULD use `zip(...)` for paired inputs to avoid an unintended Cartesian product across two collections."
- `should-attach-traits-for-behavior-and-metadata`: before "Attach **traits** for behavior and metadata: `.disabled("reason")`, `.bug("url")`, `.timeLimit(.minutes(1))`, `.enabled(if:)`, and serialization via `.serialized`."; after "You SHOULD attach traits for behavior and metadata: `.disabled("reason")`, `.bug("url")`, `.timeLimit(.minutes(1))`, `.enabled(if:)`, and serialization via `.serialized`."
- `should-define-and-apply-tags`: before "Define **tags** with `@Tag` and apply them to filter/organize runs (e.g."; after "You SHOULD define tags with `@Tag` and apply them to filter/organize runs (e.g. `.tags(.network)`)."
- `should-target-the-latest-swift-toolchain`: before "Target the latest Swift 6.2.x toolchain and write tests that are clean under strict concurrency; annotate `@MainActor` on `@Test` functions that touch main-actor state rather than dispatching manually."; after "You SHOULD target the latest Swift 6.2.x toolchain."
- `should-write-tests-clean-under-strict-concurrency`: before "Target the latest Swift 6.2.x toolchain and write tests that are clean under strict concurrency; annotate `@MainActor` on `@Test` functions that touch main-actor state rather than dispatching manually."; after "You SHOULD write tests that are clean under strict concurrency."
- `should-annotate-main-actor-tests`: before "Target the latest Swift 6.2.x toolchain and write tests that are clean under strict concurrency; annotate `@MainActor` on `@Test` functions that touch main-actor state rather than dispatching manually."; after "You SHOULD annotate `@MainActor` on `@Test` functions that touch main-actor state rather than dispatching manually."
- `should-follow-one-entity-per-file`: before "Follow one-entity-per-file: one suite `struct` per file, with nested helpers in an `extension`."; after "You SHOULD follow one-entity-per-file: one suite `struct` per file, with nested helpers in an `extension`."

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Notes**: Flag: "Keep those in XCTest." was promoted to SHOULD; the source's "still required" could suggest MUST.

**Unfinished**: none.

## test-data

`cookbook/guidelines/implementing/testing/test-data`: commit 8dc8bc30; 6 rules, 7 moved, 0 obsolete.

**Promoted**:

- `should-construct-what-each-test-needs`: before "**Construct what you need, per test.** Avoid large shared fixture files."; after "You SHOULD construct what you need, per test."
- `should-avoid-large-shared-fixture-files`: before "**Construct what you need, per test.** Avoid large shared fixture files."; after "You SHOULD avoid large shared fixture files."
- `should-use-property-based-generators-for-coverage`: before "**Property-based generators** (Hypothesis strategies, fast-check arbitraries) for" / "comprehensive input coverage"; after "Property-based generators (Hypothesis strategies, fast-check arbitraries) SHOULD be used for comprehensive input coverage."
- `should-use-inline-literals-for-simple-cases`: before "**Inline literals** for simple cases — `assert parse("hello") == "hello"` is clear"; after "Inline literals SHOULD be used for simple cases — `assert parse("hello") == "hello"` is clear."

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Unfinished**: none.

## test-doubles

`cookbook/guidelines/implementing/testing/test-doubles`: commit c8b8c38a; 5 rules, 9 moved, 0 obsolete.

**Promoted**:

- `should-use-fowlers-taxonomy`: before "Use [Martin Fowler's taxonomy](https://martinfowler.com/bliki/TestDouble.html):"; after "You SHOULD use [Martin Fowler's taxonomy](https://martinfowler.com/bliki/TestDouble.html) for test doubles: dummy, stub, spy, mock and fake."
- `should-mock-your-interface-not-the-third-party-api`: before "Mock your interface, not the third-party API directly."; after "You SHOULD mock your interface, not the third-party API directly."

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Unfinished**: none.

## testing

`cookbook/guidelines/implementing/testing/testing`: commit 64cc8b6b; 14 rules, 13 moved, 0 obsolete.

**Promoted**:

- `must-add-a-regression-test-per-bug-fix`: before "Every bug fix needs a regression test."; after "Every bug fix MUST have a regression test."
- `should-test-transitions-edge-cases-and-round-trips`: before "Test state transitions, edge cases, and serialization round-trips."; after "You SHOULD test state transitions, edge cases, and serialization round-trips."
- `should-test-component-logic-as-unit-tests`: before "UI tests are fragile — prefer testing component logic as unit tests."; after "UI tests are fragile — you SHOULD prefer testing component logic as unit tests."
- `should-use-playwright-for-end-to-end-tests`: before "Use [Playwright](https://playwright.dev/) for end-to-end and visual regression testing."; after "In TypeScript, you SHOULD use [Playwright](https://playwright.dev/) for end-to-end and visual regression testing."
- `should-use-screenshot-comparison-for-snapshot-tests`: before "Screenshot comparison for snapshot tests."; after "In TypeScript, screenshot comparison SHOULD be used for snapshot tests."
- `should-use-storybook-where-applicable`: before "Use Storybook for component catalog and visual tests where applicable."; after "In TypeScript, you SHOULD use Storybook for component catalog and visual tests where applicable."
- `should-use-xunit`: before "[xUnit](https://xunit.net/) with `[Fact]` for single tests and `[Theory]`/`[InlineData]` for parameterized tests."; after "In C#, you SHOULD use [xUnit](https://xunit.net/) with `[Fact]` for single tests and `[Theory]`/`[InlineData]` for parameterized tests."
- `should-use-fluentassertions`: before "[FluentAssertions](https://fluentassertions.com/) for readable assertions."; after "In C#, you SHOULD use [FluentAssertions](https://fluentassertions.com/) for readable assertions."
- `should-use-nsubstitute-for-mocking`: before "[NSubstitute](https://nsubstitute.github.io/) for mocking."; after "In C#, you SHOULD use [NSubstitute](https://nsubstitute.github.io/) for mocking."
- `should-use-pytest`: before "Use `pytest` for all tests."; after "In Python, you SHOULD use `pytest` for all tests."

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Notes**: The intro held two folded copies ("# Comprehensive unit testing" and "# Testing") of near-identical text; both copies' sentences are mapped as moved to the same rules, none marked obsolete. The TypeScript, C# and Python parts were folded into `rules.md` with their language scope kept in each rule; the C# code sample is the `examples` part.

**Unfinished**: none.

## unit-test-patterns (first attempt, refused)

`cookbook/guidelines/implementing/testing/unit-test-patterns`: **not converted on the first attempt, no commit.**

**Unfinished**: `cookr roles check` refuses it with three `name-collision` findings: its build-verifier, reviewer and review-verifier skill names (`verifying-build-testing-unit-test-patterns`, `reviewing-testing-unit-test-patterns`, `verifying-review-testing-unit-test-patterns`) are also derived for `guidelines/cookbook/testing/unit-test-patterns`, which batch 1 already roled (43bb4949). The check's fix is to rename one of the two topics or fold one into the other. Both are outside this brief: a rename touches `index.json` and the other topic's folder, and a fold changes another topic. The draft (6 rules, all bars authored, lossless --draft exit 0) was discarded and the folder left at its base state. An orchestrator decision is needed on the rename or fold.

**Contradictions (R4)**: none found.

## unit-test-patterns (converted after the rename)

`cookbook/guidelines/implementing/testing/unit-test-patterns`: commit fb98e99e; 6 rules, 3 moved, 0 obsolete.

The name collision above is gone: the other topic was renamed to `cookbook/guidelines/cookbook/testing/test-vector-patterns` (58e182fd, 3159f6d1), and `cookr roles check` now passes with no findings. That folder was not touched.

**Promoted**:

- `should-structure-tests-as-arrange-act-assert`: before "**Structure — Arrange, Act, Assert (AAA):**" with its block "// Arrange — set up preconditions / // Act — call the method under test / // Assert — verify the result"; after "Every unit test SHOULD be structured as Arrange, Act, Assert (AAA): Arrange sets up preconditions, Act calls the method under test, and Assert verifies the result."
- `should-use-specification-names`: before "**Naming — use descriptive names that read as specifications:**"; after "Tests SHOULD use descriptive names that read as specifications."

The other four rules keep their source wording and keyword verbatim. The intro's statement paragraph stays in `intro` for GF-01. The AAA comment block is the `structure` part (how-to), and the three sample names are the `naming` part (examples).

**Bars**: look-for authored; a-complete-review-must-establish authored; a-build-must-establish authored.

**Contradictions (R4)**: none found.

**Notes**: "**Rules:**" is a lead-in. `lossless` refuses `obsolete` for a base sentence, so it is mapped as moved to the four rules it introduced.

**Unfinished**: none.
