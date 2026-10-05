
| State | How to detect | Behavior |
|-------|---------------|----------|
| Validating | Validation checks running | Behavioral preservation enumeration and lint-rule checks; read-only |
| Reporting | Report being written | Report file created at `.claude/rule-optimization-report.md` |
| Complete | Report file exists; pipeline finished | No further action; user reviews report |
| Failed | Validation found missing constraint or lint FAIL | Pipeline halted; user must fix or revert before re-running |

