
| State | Behavior |
|-------|----------|
| Closed | No database handle is open |
| Open | A handle is open on a database file; `exec` and query functions may run |
| Failed | An operation threw a `SQLiteError`; the caller decides whether to surface or recover |

