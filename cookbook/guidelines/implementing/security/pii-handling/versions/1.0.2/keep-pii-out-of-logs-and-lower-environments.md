
- **no-pii-logs** — PII MUST NOT be written to logs, traces, error messages, or analytics
  events. Redact or hash identifiers at the logging boundary. See `sensitive-data`.
- **anonymize-analytics** — analytics SHOULD use anonymized or aggregated data; pseudonymized
  data still counts as personal data if re-identification is feasible.
- **non-prod-data** — development, test, and staging environments SHOULD use synthetic or
  anonymized data and MUST NOT contain production `sensitive-pii`.

