
- Log every deletion (who/what/when, category, request reference) to a tamper-evident, separately retained **audit trail** — the log of a deletion is not the deleted data.
- Reconcile periodically: scan for records past their `expires_at` that were not purged, and alert. Treat a reconciliation miss as a defect (fail fast).

