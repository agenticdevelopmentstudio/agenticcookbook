
Load only what's needed for the current step. This is the single highest-leverage optimization for Claude Code extensions.

### The Cost Model

Files in `.claude/rules/` and CLAUDE.md are injected into the system prompt on **every turn** — every user message, every tool call, every response. In a 50-turn conversation, a 10KB rule file consumes ~500KB of context. This cost is invisible and compounding.

Content loaded via tool calls (reading files, invoking skills) is paid once at the point of use. This makes on-demand loading dramatically cheaper for anything not needed on every turn.

### The Three Tiers

**Tier 1 — Always-on (rules, CLAUDE.md):** One-line directives and pointers. This tier pays per-turn cost, so every byte must earn its place. A rule that says "When authoring skills, invoke `/lint-skill` after every change" costs one line per turn. A rule that inlines the entire lint checklist costs 50 lines per turn for something needed once per session.

Target: rule files SHOULD be under 200 lines / ~8KB. Rules that apply to narrow workflows SHOULD be under 10 lines.

**Tier 2 — On-demand (skills, agent prompts):** Guidelines, checklists, and procedures loaded when the workflow step requires them. A skill pulls in the relevant cookbook guidelines when it reaches the step that needs them — not at startup. An agent receives narrow instructions for its specific task.

**Tier 3 — Deep reference (research, full cookbook):** Read only when investigating a specific question or making a decision that requires background. Never loaded unconditionally.

### Applying Progressive Disclosure

- **Rules**: Rules MUST be kept to the minimum directive. Instead of inlining a 38-item checklist, write a one-line pointer: "Run the checklist in `<path>` before marking complete." The checklist loads once when needed, not on every turn.
- **Skills**: Skills SHOULD structure each step to load its own context. A five-step skill SHOULD NOT front-load all five steps' reference material. Step 3 reads the guidelines it needs when step 3 begins.
- **Agents**: Agents MUST receive narrow, specific instructions for one task. Background context SHOULD NOT be included "in case they need it." If the agent needs additional context, it can read it.
- **CLAUDE.md**: CLAUDE.md SHOULD contain only project identity, directory structure, and workflow pointers. Detailed procedures SHOULD be moved into skills. Enforcement SHOULD be moved into rules.

### Real-World Impact

The agenticdevelopercookbook's own rules went from 381 lines / 17,689 bytes per turn to 10 lines / 358 bytes per turn — a 97% reduction — by applying progressive disclosure. The behavioral constraints were preserved; only the delivery mechanism changed.

