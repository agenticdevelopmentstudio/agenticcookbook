
| Situation | Strategy |
|-----------|----------|
| Default / general tables | `INTEGER PRIMARY KEY` |
| Audit log or ledger — IDs must never reuse | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| Distributed / multi-device sync | UUIDv7 as TEXT or BLOB |
| Exposing IDs in a public API | Separate UUID column + integer PK internally |
| Non-integer or composite key, small rows | `WITHOUT ROWID` |
| Maximum performance, local-only database | `INTEGER PRIMARY KEY` |

