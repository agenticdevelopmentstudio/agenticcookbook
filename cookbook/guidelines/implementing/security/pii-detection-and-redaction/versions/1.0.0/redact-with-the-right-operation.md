
These are not interchangeable — pick by whether you need reversibility or downstream utility.

- **redaction** — irreversible replacement with a fixed token (`[redacted-email]`) or blank.
  The default for published or exported data.
- **masking** — keep a partial value (last-4) for operational reference while hiding the rest.
- **tokenization** — substitute a vault-mapped placeholder; reversible only through the vault.
- **pseudonymization** — a stable surrogate that preserves patterns for analytics. It is
  **still personal data** under GDPR Article 4 when re-identification is feasible — do NOT treat
  pseudonymized data as anonymized.
- **generalize-and-suppress** — for quasi-identifiers, coarsen (year not date, 3-digit ZIP, age
  band) or drop entirely; bound linkage risk with k-anonymity, l-diversity, or t-closeness.
- **anonymization** — only call data anonymized when re-identification is not reasonably feasible
  (de-identified **and** irreversible). Everything short of that remains in scope.

