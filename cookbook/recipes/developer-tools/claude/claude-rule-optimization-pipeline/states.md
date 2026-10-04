
| State | How to detect | Behavior |
|-------|---------------|----------|
| Auditing | Phase 1 output being produced | Read-only inventory and measurement; no user interaction required |
| Awaiting Confirmation | Phase 2 proposals presented | Pipeline paused; user must confirm, decline, or selectively approve optimizations |
| Optimizing | User confirmed; files being modified | Rule files updated per approved proposals |
| Validating | Phase 3 checks running | Behavioral preservation enumeration and lint-rule checks; read-only |
| Reporting | Phase 4 report being written | Report file created at `.claude/rule-optimization-report.md` |
| Complete | Report file exists; pipeline finished | No further action; user reviews report |
| Failed | Validation found missing constraint or lint FAIL | Pipeline halted; user must fix or revert before re-running |

