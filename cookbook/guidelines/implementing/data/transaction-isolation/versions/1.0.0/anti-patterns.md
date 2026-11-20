
- Treating `40001` as a hard error and surfacing it to the user — it is expected under contention and MUST be retried.
- Using Read Committed for a check-then-update invariant (read balance, then debit) — this loses updates; use `SELECT ... FOR UPDATE` or Serializable.
- Emitting side effects (charge a card, send a webhook) inside a Serializable transaction body that may be retried.

