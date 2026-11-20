
- **two-identifier-classes**: You MUST treat two classes as PII. *Direct identifiers* name a
  person alone (name, email, phone, SSN, credit-card, account/device IDs). *Quasi-identifiers*
  are harmless alone but re-identify a person **in combination** (date of birth + ZIP + gender
  uniquely identifies most individuals, and links against public datasets).
- **use-a-coverage-checklist**: You **SHOULD** enumerate categories against a fixed list so you do not miss a
  type. HIPAA Safe Harbor's 18 identifiers are the ready-made checklist: names; all geography
  finer than state; all dates but year (and ages 90+); phone; fax; email; SSN; medical-record,
  health-plan, account, certificate/license, vehicle, and device numbers; URLs; IP addresses;
  biometric identifiers; full-face photos; and any other unique code.
- **linked-and-linkable**: Per NIST SP 800-122, PII is anything that *distinguishes or traces*
  an identity **or** is *linked or linkable* to a person. You **SHOULD** rate each instance's confidentiality
  impact (low / moderate / high) by identifiability, quantity, field sensitivity, and context
  of use, and size controls to the impact.
- **detect-in-layers**: You **SHOULD** combine rule-based and ML detection (the approach
  Microsoft Presidio's analyzer takes: recognizers → context enhancer → anonymizer).
- **regex-for-structured**: You **SHOULD** use anchored patterns for structured types (email, phone, SSN,
  credit-card, IBAN, IP).
- **validate-with-checksums**: You MUST run format-specific validators to cut false positives.
  A 16-digit run that fails the **Luhn** check is not a card number; apply the equivalent check
  (IBAN mod-97, etc.) before treating a match as PII.
- **context-words**: Detection SHOULD gate or boost confidence on nearby lemmas ("card", "ssn", "dob",
  "patient").
- **ner-for-unstructured**: You **SHOULD** use a
  Named-Entity-Recognition model (spaCy or a transformer) for names, places, and organizations, and register custom
  recognizers for your domain's ID formats.
- **favor-recall**: You **SHOULD** tune toward **recall**
  (optimize the F2 / β=2 score, which weights recall over precision) and triage false positives
  after.
- **should-not-ship-precision-chosen-detector**: You **SHOULD NOT** ship a detector chosen for a clean precision number.
- **default-deny**: Where feasible, you **SHOULD** allowlist what may leave the boundary rather than blocklist
  what must be hidden.
- **drop-structurally**: You **SHOULD** remove PII-bearing fields at the schema or serialization boundary, not
  by string-scrubbing them out of an already-built payload. See `pii-handling`.
- **pick-operation-by-need**: You **SHOULD** pick the redaction operation by whether you need reversibility or downstream utility.
- **redact-published-data**: Redaction **SHOULD** be the default for published or exported data.
- **pseudonymized-is-not-anonymized**: You **SHOULD NOT** treat pseudonymized data as anonymized: it is
  **still personal data** under GDPR Article 4 when re-identification is feasible.
- **generalize-and-suppress**: For quasi-identifiers, you **SHOULD** coarsen (year not date, 3-digit ZIP, age
  band) or drop entirely; bound linkage risk with k-anonymity, l-diversity, or t-closeness.
- **anonymization**: You **SHOULD** only call data anonymized when re-identification is not reasonably feasible
  (de-identified **and** irreversible). Everything short of that remains in scope.
- **fail-closed-backstop**: After redaction you MUST re-scan the serialized output and hard-fail
  the emit or build if any pattern survives.
- **defense-in-depth**: You **SHOULD** layer independent gates (surface reduction → structural drop → prose
  substitution → assertion) so one layer's miss is caught by the next.
- **golden-tests**: You **SHOULD** keep a known-leaky fixture and assert end-to-end that nothing survives.
- **freeze-edge-cases**: You **SHOULD** freeze real edge cases as regression tests — e.g. a `git@github.com:` SSH remote that looks
  email-shaped but must be kept, or a `~/tool` path that must not be redacted like a home path.
- **scan-history-not-just-the-tip**: You **SHOULD** treat a public repo's history as part of the exposed surface.
- **remediate-then-rotate**: You **SHOULD** purge with `git filter-repo` (or BFG Repo-Cleaner), force-update
  the remote, and **rotate** any exposed secret.
  - `gitleaks` (fast regex/entropy, good in a pre-commit hook) and
    `trufflehog` (verifies whether a found credential is still live, good for full-history scans)
    are the standard scanners.
- **assume-public-credentials-compromised**: A purged credential that was public **MUST** be assumed compromised.
