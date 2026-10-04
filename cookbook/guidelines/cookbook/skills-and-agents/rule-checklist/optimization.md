
Rules in `.claude/rules/` are injected into the system prompt on **every turn** — not just at session start. Every byte costs context on every user message, tool call, and response. These checks flag common sources of per-turn waste.

| ID  | Criterion | How to check | Severity |
|-----|-----------|-------------|----------|
| O01 | Rule file under 200 lines / ~8KB | Count lines and bytes; larger rules should move content to on-demand skills or external references | WARN |
| O02 | No content duplicated from another rule | Compare against other `.md` files in the same `.claude/rules/` directory; overlapping instructions are processed twice per turn | WARN |
| O03 | `globs` frontmatter present when scoped | If the rule only applies to specific file patterns (e.g., `.claude/**`, `site/**`), it should have `globs` frontmatter to prevent loading on unrelated work | WARN |
| O04 | MUST NOT items are unique | Each MUST NOT adds a constraint not already expressed imperatively in the body text; restating "You MUST NOT skip this phase" from line 50 in the MUST NOT section wastes per-turn context | WARN |
| O05 | External refs have high content ratio | If an external file reference points to a file where frontmatter exceeds 50% of total lines, suggest inlining the useful content instead | INFO |
| O06 | No more than 5 unconditional external reads | Rules that mandate reading 6+ external files before any work create high entry cost; consider summaries, on-demand reads, or iterative approaches | WARN |

