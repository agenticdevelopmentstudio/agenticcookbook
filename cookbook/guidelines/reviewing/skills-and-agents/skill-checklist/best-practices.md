
| ID  | Criterion | How to check | Severity |
|-----|-----------|-------------|----------|
| B01 | Verification method provided | Skill includes how to validate it worked (run tests, check output, verify file exists) | WARN |
| B02 | Does not replicate native capabilities | Skill doesn't teach Claude things it already knows (basic git, standard coding, etc.) | WARN |
| B03 | `disable-model-invocation` for side-effect skills | Skills that deploy, commit, send messages, or modify external state should set `disable-model-invocation: true` | WARN |
| B04 | `context: fork` considered for isolated tasks | Task skills that do heavy reading/fetching and return a result benefit from fork isolation | INFO |
| B05 | Examples or usage patterns included | Skill body or references include at least one example invocation or expected output | WARN |
| B06 | No kitchen-sink anti-pattern | Skill doesn't try to do everything — stays focused on its stated purpose | FAIL |
| B07 | No infinite-exploration anti-pattern | Task skills scope their investigation; don't read unbounded numbers of files | WARN |
| B08 | Not a CLAUDE.md dump | Skill content is skill-appropriate, not a copy-paste of project rules that belong in CLAUDE.md | WARN |
| B09 | `allowed-tools` used if tool restriction needed | If the skill should only use certain tools, `allowed-tools` is set | INFO |
| B10 | Model override appropriate | If `model:` is set, it matches the skill's complexity (don't use opus for trivial tasks) | WARN |
| B11 | Dynamic context injection correct | If `` !`command` `` syntax is used, the command is safe, fast, and deterministic | WARN |
| B12 | Description concise for context budget | Description is under ~200 characters to avoid consuming excessive context | WARN |

