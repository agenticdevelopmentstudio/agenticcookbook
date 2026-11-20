
### The Three Tiers

**Tier 1 — Always-on (rules, CLAUDE.md):** One-line directives and pointers. This tier pays per-turn cost, so every byte must earn its place. A rule that says "When authoring skills, invoke `/lint-skill` after every change" costs one line per turn. A rule that inlines the entire lint checklist costs 50 lines per turn for something needed once per session.

**Tier 2 — On-demand (skills, agent prompts):** Guidelines, checklists, and procedures loaded when the workflow step requires them. A skill pulls in the relevant cookbook guidelines when it reaches the step that needs them — not at startup. An agent receives narrow instructions for its specific task.

**Tier 3 — Deep reference (research, full cookbook):** Read only when investigating a specific question or making a decision that requires background.

### Applying Progressive Disclosure

- **Rules**: Instead of inlining a 38-item checklist, write a one-line pointer: "Run the checklist in `<path>` before marking complete." The checklist loads once when needed, not on every turn.
- **Skills**: Step 3 reads the guidelines it needs when step 3 begins.

