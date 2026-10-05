
Claude Code rule files in `.claude/rules/` are injected into the system prompt on every turn, so a 200-line rule costs 200 lines times the number of turns in a session. The rule audit is the read-only first phase of rule optimization: it inventories every rule file, measures the aggregate per-turn cost, and finds the waste (duplicated constraints, rules that should be scoped by `globs`, and instructions that force external file reads). It changes nothing; its findings feed the rule optimizer.

### Metrics Collected

| Metric | ID | Unit |
|--------|----|------|
| Per-turn cost (lines) | `per-turn-lines` | integer |
| Per-turn cost (bytes) | `per-turn-bytes` | integer |
| Rule file count | `rule-count` | integer |
| Mandatory external reads | `mandatory-reads` | integer |
| Duplication ratio | `duplication-ratio` | percentage |
| Ungated rule count | `ungated-count` | integer |
| Redundant MUST NOT count | `redundant-must-nots` | integer |
| Frontmatter-heavy refs | `high-metadata-refs` | integer |

