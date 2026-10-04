
| ID  | Criterion | How to check | Severity |
|-----|-----------|-------------|----------|
| B01 | Verification method provided | Agent includes how to validate it completed successfully | WARN |
| B02 | Does not replicate native capabilities | Agent doesn't teach Claude things it already knows | WARN |
| B05 | Examples or usage patterns included | Body or description includes expected usage context | WARN |
| B06 | No kitchen-sink anti-pattern | Agent doesn't try to do everything — stays focused on its stated purpose | FAIL |
| B07 | No infinite-exploration anti-pattern | Agent scopes its investigation; doesn't read unbounded numbers of files | WARN |
| B08 | Not a CLAUDE.md dump | Agent content is agent-appropriate, not a copy-paste of project rules that belong in CLAUDE.md | WARN |
| B10 | Model override appropriate | If `model:` is set, it matches the agent's complexity | WARN |
| B12 | Description concise for context budget | Description is under ~200 characters to avoid consuming excessive context | WARN |

---

