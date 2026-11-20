
- **AGENTS.md** is the vendor-neutral, cross-tool convention. As of 2026 it is stewarded by the Agentic AI Foundation under the Linux Foundation and is read by many agent tools. (Adoption breadth is broad but cross-vendor counts come from project maintainers — treat specific repo-count figures as vendor-reported, not independently audited.)
- **CLAUDE.md** is Claude Code's equivalent. Per Anthropic's documentation it is loaded into context automatically at the start of a session.
- The repo **MUST** ship at least one such file. To serve both Claude Code and other agents from one source, you **SHOULD** keep a single canonical file and make the other a symlink (e.g. `CLAUDE.md` → `AGENTS.md`) rather than maintaining two copies that drift.

