
| ID  | Criterion | How to check | Severity |
|-----|-----------|-------------|----------|
| C01 | Single responsibility | Skill has one clear purpose; not a grab-bag of unrelated instructions | WARN |
| C02 | Task skills have step-by-step instructions | If the skill performs actions (not just reference), it should have numbered steps or a clear workflow | WARN |
| C03 | Reference vs task content appropriate | Reference skills (background knowledge) should not have imperative "do X" steps; task skills should not be pure documentation | WARN |
| C04 | Error handling covered | Instructions address what to do when things go wrong (tool failures, missing files, bad input) | WARN |
| C05 | `$ARGUMENTS` used when skill accepts input | Description implies the skill takes input but body never references `$ARGUMENTS` | WARN |
| C06 | `${CLAUDE_SKILL_DIR}` for file references | Skill references its own supporting files using `${CLAUDE_SKILL_DIR}`, not hardcoded paths | FAIL |
| C07 | Instructions are actionable and specific | Steps tell Claude what to do concretely, not vague directives like "handle errors appropriately" | WARN |
| C08 | No conflicting instructions | Body does not contradict itself (e.g., "always do X" then later "never do X") | FAIL |
| C09 | Well-structured markdown | Uses headings, lists, code blocks; not a wall of unstructured text | WARN |
| C10 | No redundancy with supporting files | SKILL.md and reference files don't duplicate large blocks of the same content | WARN |

---

