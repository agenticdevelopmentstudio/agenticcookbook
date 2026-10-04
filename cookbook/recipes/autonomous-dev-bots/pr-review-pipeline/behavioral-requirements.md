
### Trigger & Execution

- **webhook-trigger**: The pipeline MUST trigger when a GitHub `pull_request` event (opened, synchronize, reopened) is received at the OpenClaw webhook endpoint (`POST /hooks/agent`).
- **poll-fallback**: The pipeline SHOULD fall back to polling via `gh pr list` on a cron schedule if webhooks are unavailable.
- **isolated-session**: Each pipeline run MUST execute in an isolated OpenClaw agent session to prevent cross-contamination between PR reviews.
- **sequential-phases**: Phases MUST run sequentially: Phase 1 → Phase 2 → Phase 3.
- **short-circuit**: The pipeline MUST stop and not run subsequent phases if a phase posts "Request Changes".
- **rerun-on-update**: The pipeline MUST rerun from Phase 1 when new commits are pushed to the PR branch.

### Contributor Preferences

- **fix-preference-prompt**: The `/contribute-to-cookbook` skill MUST ask the contributor before PR submission: "If the review pipeline finds fixable issues, would you like us to fix them automatically, or review each change?"
- **fix-preference-default**: The default preference MUST be "fix automatically".
- **fix-preference-storage**: The preference MUST be stored in the PR body as metadata (e.g., `<!-- fix-preference: auto -->` or `<!-- fix-preference: review -->`).
- **fix-preference-honored**: The refactoring agent MUST honor the stored preference — committing directly for "auto", posting suggested changes for "review".

### Phase 1: Review

- **structural-validation**: Phase 1 MUST run all applicable checks from `/validate-cookbook` (frontmatter integrity, content structure, cross-references, indexes, file placement).
- **markdownlint**: Phase 1 MUST run markdownlint-cli2 and auto-fix fixable issues.
- **vale-cookbook-style**: Phase 1 MUST run Vale with the custom Cookbook style checking for: vague terms, ambiguous quantifiers, hedging, implicit references, casual RFC 2119 keywords, double negatives, ambiguous pronouns.
- **llm-clarity-pass**: Phase 1 MUST run an LLM-based clarity analysis checking for: ambiguous antecedents, implicit assumptions, terminology inconsistency across sections, self-containment of sections, unresolved references.
- **content-completeness**: Phase 1 MUST verify all required sections are present and non-empty (or explicitly N/A with reason), MUST requirements have test vectors, appearance values are concrete, logging messages are exact strings, platform notes cover all declared platforms.
- **convention-compliance**: Phase 1 MUST verify named requirements use kebab-case, RFC 2119 keywords are used correctly, domain identifiers match file paths, template variables are used where appropriate.
- **fix-loop**: Phase 1 MUST attempt to fix issues in a loop, max 3 iterations. Each iteration: fix auto-fixable issues (markdownlint, frontmatter), attempt LLM fixes (prose rewrites, inferrable values), re-validate. After 3 iterations, remaining issues are flagged as unfixable.
- **fix-categorization**: Each issue MUST be categorized as: auto-fixable (deterministic tool fix), LLM-fixable (LLM can infer the correction), or human-required (needs contributor or reviewer decision).

### Phase 2: Refactoring & Scoping

- **placement-analysis**: Phase 2 MUST verify the recipe is in the correct directory for its type and that the domain identifier matches the file path.
- **granularity-check**: Phase 2 MUST assess whether the recipe covers exactly one coherent concept. Flag recipes with more than 15 MUST requirements or more than 8 states as potentially too broad. Flag recipes with fewer than 3 requirements as potentially too narrow.
- **overlap-detection**: Phase 2 MUST compare the new/changed content against ALL existing cookbook content (principles, guidelines, and recipes) for conceptual overlap. This includes: identical or near-identical requirement names, duplicate behavioral descriptions, redefinition of concepts that have their own specs.
- **ecosystem-fit**: Phase 2 MUST check whether existing recipes should reference the new content (backlinks), whether new terminology conflicts with established terms, and whether relevant guidelines are referenced.
- **refactoring-proposal**: When overlap or scope issues are found, Phase 2 MUST produce a concrete refactoring proposal specifying exact changes: which requirements to move, merge, or split, and which files are affected.
- **granular-assessment**: Refactoring proposals MUST be per-requirement/section, not per-recipe. A recipe with 10 parts where 2 are valuable MUST have a proposal that extracts those 2.

### Phase 3: Evaluate

- **value-scoring**: Phase 3 MUST score the contribution on: novelty (fills a gap), demand signal (multiple projects would use this), quality (how clean was the Phase 1/2 pass), completeness (platform coverage, test vector thoroughness), ecosystem integration (quality of depends-on/related links).
- **risk-scoring**: Phase 3 MUST assess: breaking changes to existing content, conflicts with engineering principles, scope appropriateness for the cookbook, contributor track record (first-time vs established).
- **external-research**: Phase 3 MUST research beyond the repo: search GitHub for similar patterns, check platform SDK documentation to see if the concept is built-in, assess whether the pattern is well-established or novel.
- **recommendation**: Phase 3 MUST produce a structured recommendation: value (HIGH/MEDIUM/LOW), confidence (HIGH/MEDIUM/LOW), recommendation (ACCEPT/ACCEPT WITH REFACTORING/PARTIAL ACCEPT/REJECT), with per-section rationale.
- **human-escalation**: Phase 3 MUST post its recommendation as a PR review. The human reviewer makes the final decision — Phase 3 recommends but never merges.

### Rejection & Appeal

- **rejection-format**: A rejecting phase MUST post a PR review with "Request Changes" status, including per-issue explanation of what failed and why.
- **branch-protection**: The repository MUST be configured to require approval from all three phase bot GitHub Apps plus a human reviewer before merging is allowed.
- **appeal-process**: If a contributor replies to a rejection comment disputing the decision, the pipeline MUST flag the PR for human review rather than re-running automatically.
- **rerun-after-fix**: After the refactoring agent applies fixes, the pipeline MUST rerun from Phase 1 on the updated content.

### Refactoring Agent

- **dedicated-persona**: All automated fixes and refactoring MUST be applied by a single dedicated refactoring agent with its own GitHub App identity, distinct from the three phase bots.
- **fix-or-suggest**: The refactoring agent MUST commit directly if the contributor chose "fix automatically", or post GitHub suggested changes if the contributor chose "review each change".
- **scope-of-fixes**: The refactoring agent handles fixes from all phases: structural fixes from Phase 1, refactoring proposals approved by the human reviewer from Phase 2.

