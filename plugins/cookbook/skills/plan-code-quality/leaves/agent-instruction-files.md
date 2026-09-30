<!-- leaf: plan-code-quality/agent-instruction-files · source: guidelines/planning/code-quality/agent-instruction-files.md -->

**Rules** (cite as `plan-code-quality/agent-instruction-files#<slug>`):

- `ai-coding-agents-ship-machine-targeted-instruction` MUST — A repository consumed by AI coding agents MUST ship a machine-targeted instruction file at its root that tells an agent …
- `repo-ship-least-one-such` MUST — The repo MUST ship at least one such file. To serve both Claude Code and other agents from one source, you SHOULD keep …
- `build-test-run` MUST
- `conventions` SHOULD
- `layout` SHOULD
- `out-of-scope` SHOULD
- `include-commit-pr-conventions` MAY — It MAY include commit/PR conventions, security gotchas, and deployment steps.
- `package-repos-you-place-scoped-instruction-file` SHOULD — For multi-package repos you SHOULD place a scoped instruction file inside each package. Agents read the nearest file up …
- `root-file-hold-repo-wide-guidance` SHOULD — The root file SHOULD hold repo-wide guidance; nested files SHOULD hold only what differs for that package, to avoid …
- `file-stay-concise-high-signal` MUST — The file MUST stay concise and high-signal. A widely-reported failure mode is that bloated, stale instruction files get …
- `noise-so-you-delete-instructions-obsolete-obvious` SHOULD — Note this is a practitioner heuristic, not a settled empirical result; the durable principle is signal-to-noise, so you …
- `instruction-specific-verifiable-command-path` SHOULD — Every instruction SHOULD be specific and verifiable (a command, a path, a named rule) rather than vague aspiration …
- `you-review-file-whenever-build` SHOULD — You SHOULD review the file whenever build/test commands or project structure change, treating it as code that rots.

# Agent instruction files (AGENTS.md / CLAUDE.md)

A repository consumed by AI coding agents **MUST** ship a machine-targeted instruction file at its root that tells an agent how to build, test, and run the project, plus the conventions and boundaries a new teammate would need. This is the agent equivalent of a good onboarding README.

## Which file to ship

- **AGENTS.md** is the vendor-neutral, cross-tool convention. As of 2026 it is stewarded by the Agentic AI Foundation under the Linux Foundation and is read by many agent tools. (Adoption breadth is broad but cross-vendor counts come from project maintainers — treat specific repo-count figures as vendor-reported, not independently audited.)
- **CLAUDE.md** is Claude Code's equivalent. Per Anthropic's documentation it is loaded into context automatically at the start of a session.
- The repo **MUST** ship at least one such file. To serve both Claude Code and other agents from one source, you **SHOULD** keep a single canonical file and make the other a symlink (e.g. `CLAUDE.md` → `AGENTS.md`) rather than maintaining two copies that drift.

## What to include

- **build-test-run**: It **MUST** state the exact commands to build, test, and run the project (e.g. `npm test`, `make build`), including any required setup or environment variables.
- **conventions**: It **SHOULD** state code style, naming, and project-specific patterns the agent must follow.
- **layout**: It **SHOULD** describe the project layout — where source, tests, and config live — so the agent navigates without guessing.
- **out-of-scope**: It **SHOULD** state what is off-limits: files or directories not to edit, commands not to run, and any "ask first" actions.
- It **MAY** include commit/PR conventions, security gotchas, and deployment steps.

## Monorepos: nest per-directory files

- For multi-package repos you **SHOULD** place a scoped instruction file inside each package. Agents read the **nearest** file up the directory tree, so the closest one takes precedence over the root file.
- The root file **SHOULD** hold repo-wide guidance; nested files **SHOULD** hold only what differs for that package, to avoid duplication.

## Keep it lean — prune ruthlessly

- The file **MUST** stay concise and high-signal. A widely-reported failure mode is that bloated, stale instruction files get partially ignored and can degrade task success — keep durable, load-bearing instructions only.
- Note this is a practitioner heuristic, not a settled empirical result; the durable principle is signal-to-noise, so you **SHOULD** delete instructions that are obsolete, obvious, or contradicted by the code.
- Every instruction **SHOULD** be specific and verifiable (a command, a path, a named rule) rather than vague aspiration ("write clean code").
- You **SHOULD** review the file whenever build/test commands or project structure change, treating it as code that rots.
