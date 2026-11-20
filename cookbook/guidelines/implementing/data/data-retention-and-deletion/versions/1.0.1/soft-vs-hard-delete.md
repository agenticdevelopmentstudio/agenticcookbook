
| Choice | When to use | Caution |
|---|---|---|
| Soft delete (tombstone flag) | Undo windows, referential integrity, short-lived audit needs | Data still present — **MUST NOT** count as erasure for a privacy request |
| Hard delete (row removed) | Erasure requests, PII past retention | Irreversible; verify cascade first |
| Anonymize / pseudonymize | Keep aggregates/analytics without identifying a person | **MUST** be irreversible (no re-identification key retained) |

- Decide soft vs. hard **per category**, not globally. Erasure obligations **MUST** resolve to hard delete or true anonymization within the source and all derived stores.

