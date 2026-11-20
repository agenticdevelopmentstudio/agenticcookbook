
### Structure & Format

- **must-have-yaml-frontmatter**: The skill file MUST have YAML frontmatter: it starts with `---` and has a closing `---`. (S01, FAIL)
- **should-have-name-field**: The frontmatter SHOULD contain a `name:` field. (S02, WARN)
- **must-use-kebab-case-name**: The `name` MUST be lowercase kebab-case of at most 64 characters, matching `^[a-z][a-z0-9-]{0,63}$`. (S03, FAIL)
- **must-have-description-field**: The frontmatter MUST contain a `description:` field. (S04, FAIL)
- **should-use-natural-trigger-keywords**: The description SHOULD use natural trigger keywords: phrases users would say, neither too vague ("does stuff") nor too narrow ("only for X on Tuesdays"). (S05, WARN)
- **should-keep-skill-md-under-500-lines**: SKILL.md SHOULD be at most 500 lines (`wc -l SKILL.md`). (S06, WARN)
- **should-put-supporting-files-in-subdirectories**: Supporting files (non-SKILL.md) SHOULD be in references/, scripts/ or examples/, not loose at the skill root. (S07, WARN)
- **should-reference-supporting-files**: If references/ exists, SKILL.md SHOULD mention those files or use `${CLAUDE_SKILL_DIR}` to load them. (S08, WARN)
- **should-match-directory-to-name**: The directory basename SHOULD match the frontmatter `name`. (S09, WARN)
- **should-have-argument-hint-when-using-arguments**: If SKILL.md uses `$ARGUMENTS` or `$1`, `$2`, the frontmatter SHOULD have `argument-hint:`. (S10, WARN)
- **should-be-in-skills-directory**: The skill SHOULD be in `.claude/skills/` or `~/.claude/skills/`. (S11, WARN)
- **should-use-only-recognized-frontmatter-fields**: The frontmatter SHOULD use only recognized fields: name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model, effort, context, agent, hooks, paths, shell. (S12, WARN)
- **must-name-main-file-skill-md**: The main file MUST be named exactly `SKILL.md`, not `skill.md` or `Skill.md`; Claude Code looks for this exact name. (S13, FAIL)
- **should-use-lowercase-descriptive-supporting-names**: Files in references/, scripts/ and examples/ SHOULD match `^[a-z][a-z0-9-]*(\.[a-z]+)+$` and have names that describe their content (not `doc1.md`). (S14, WARN)

### Content Quality

- **should-have-single-responsibility**: The skill SHOULD have one clear purpose, not a grab-bag of unrelated instructions. (C01, WARN)
- **should-give-task-skills-step-by-step-instructions**: If the skill performs actions (not just reference), it SHOULD have numbered steps or a clear workflow. (C02, WARN)
- **should-keep-reference-and-task-content-apart**: Reference skills (background knowledge) SHOULD NOT have imperative "do X" steps, and task skills SHOULD NOT be pure documentation. (C03, WARN)
- **should-cover-error-handling**: Instructions SHOULD address what to do when things go wrong (tool failures, missing files, bad input). (C04, WARN)
- **should-use-arguments-when-accepting-input**: If the description implies the skill takes input, the body SHOULD reference `$ARGUMENTS`. (C05, WARN)
- **must-use-claude-skill-dir-for-file-references**: The skill MUST reference its own supporting files using `${CLAUDE_SKILL_DIR}`, not hardcoded paths. (C06, FAIL)
- **should-give-actionable-specific-instructions**: Steps SHOULD tell Claude concretely what to do, not give vague directives like "handle errors appropriately". (C07, WARN)
- **must-not-conflict-with-itself**: The body MUST NOT contradict itself (e.g., "always do X" then later "never do X"). (C08, FAIL)
- **should-use-well-structured-markdown**: The skill SHOULD use headings, lists and code blocks, not a wall of unstructured text. (C09, WARN)
- **should-not-duplicate-supporting-files**: SKILL.md and reference files SHOULD NOT duplicate large blocks of the same content. (C10, WARN)

### Best Practices

- **should-provide-verification-method**: The skill SHOULD include how to validate it worked (run tests, check output, verify file exists). (B01, WARN)
- **should-not-replicate-native-capabilities**: The skill SHOULD NOT teach Claude things it already knows (basic git, standard coding, etc.). (B02, WARN)
- **should-disable-model-invocation-for-side-effects**: Skills that deploy, commit, send messages, or modify external state SHOULD set `disable-model-invocation: true`. (B03, WARN)
- **may-use-context-fork-for-isolated-tasks**: Task skills that do heavy reading/fetching and return a result MAY use `context: fork`, since they benefit from fork isolation. (B04, INFO)
- **should-include-usage-examples**: The skill body or references SHOULD include at least one example invocation or expected output. (B05, WARN)
- **must-not-be-kitchen-sink**: The skill MUST NOT try to do everything; it stays focused on its stated purpose. (B06, FAIL)
- **should-not-explore-unbounded**: Task skills SHOULD scope their investigation and not read unbounded numbers of files. (B07, WARN)
- **should-not-be-claude-md-dump**: Skill content SHOULD be skill-appropriate, not a copy-paste of project rules that belong in CLAUDE.md. (B08, WARN)
- **may-use-allowed-tools-for-restriction**: If the skill should only use certain tools, it MAY set `allowed-tools`. (B09, INFO)
- **should-match-model-override-to-complexity**: If `model:` is set, it SHOULD match the skill's complexity (don't use opus for trivial tasks). (B10, WARN)
- **should-keep-dynamic-context-injection-safe**: If `` !`command` `` syntax is used, the command SHOULD be safe, fast, and deterministic. (B11, WARN)
- **should-keep-description-under-200-characters**: The description SHOULD be under ~200 characters to avoid consuming excessive context. (B12, WARN)
