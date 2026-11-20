
| ID  | Criterion | How to check | Severity |
|-----|-----------|-------------|----------|
| C01 | Single responsibility | Rule addresses one coherent concern — not a grab-bag of unrelated instructions | WARN |
| C07 | Instructions are actionable and specific | Every instruction tells the LLM what to do concretely, not vague directives like "handle errors appropriately" | WARN |
| C08 | No conflicting instructions | Rule does not contradict itself (e.g., "always do X" then later "never do X") | FAIL |
| C09 | Well-structured markdown | Uses headings, lists, code blocks; not a wall of unstructured text | WARN |

---

