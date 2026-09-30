<!-- leaf: implement-security/pii-detection-and-redaction · source: guidelines/implementing/security/pii-detection-and-redaction.md -->

**Rules** (cite as `implement-security/pii-detection-and-redaction#<slug>`):

- `two-identifier-classes` MUST
- `validate-with-checksums` MUST
- `context-words` SHOULD
- `fail-closed-backstop` MUST

# PII detection and redaction

Finding personal data is a detection problem before it is a redaction problem: you cannot
scrub what you did not recognize. Detect in layers, redact with the operation that fits the
use, and verify with a backstop that fails closed. Classification, encryption, and log hygiene
live in `pii-handling`; this page covers *finding* PII in free text, data, and repositories and
*removing* it safely. This is engineering guidance and NOT legal advice; confirm obligations
with counsel.

## Know what you are looking for

- **two-identifier-classes** — you MUST treat two classes as PII. *Direct identifiers* name a
  person alone (name, email, phone, SSN, credit-card, account/device IDs). *Quasi-identifiers*
  are harmless alone but re-identify a person **in combination** (date of birth + ZIP + gender
  uniquely identifies most individuals, and links against public datasets). A feed can be
  email-free and still leak identity through quasi-identifiers — scanning only for direct
  identifiers is the most common blind spot.
- **use-a-coverage-checklist** — enumerate categories against a fixed list so you do not miss a
  type. HIPAA Safe Harbor's 18 identifiers are the ready-made checklist: names; all geography
  finer than state; all dates but year (and ages 90+); phone; fax; email; SSN; medical-record,
  health-plan, account, certificate/license, vehicle, and device numbers; URLs; IP addresses;
  biometric identifiers; full-face photos; and any other unique code.
- **linked-and-linkable** — per NIST SP 800-122, PII is anything that *distinguishes or traces*
  an identity **or** is *linked or linkable* to a person. Rate each instance's confidentiality
  impact (low / moderate / high) by identifiability, quantity, field sensitivity, and context
  of use, and size controls to the impact.

## Detect in layers

No single technique is sufficient; combine rule-based and ML detection (the approach
Microsoft Presidio's analyzer takes: recognizers → context enhancer → anonymizer).

- **regex-for-structured** — use anchored patterns for structured types (email, phone, SSN,
  credit-card, IBAN, IP). Necessary but noisy: raw patterns over-flag benign strings that share
  a shape.
- **validate-with-checksums** — you MUST run format-specific validators to cut false positives.
  A 16-digit run that fails the **Luhn** check is not a card number; apply the equivalent check
  (IBAN mod-97, etc.) before treating a match as PII.
- **context-words** — SHOULD gate or boost confidence on nearby lemmas ("card", "ssn", "dob",
  "patient"). Context lowers both false positives and misses without new patterns.
- **ner-for-unstructured** — regex cannot find names, places, or organizations; use a
  Named-Entity-Recognition model (spaCy or a transformer) for those, and register custom
  recognizers for your domain's ID formats.
- **favor-recall** — for PII a miss is worse than a false alarm, so tune toward **recall**
  (optimize the F2 / β=2 score, which weights recall over precision) and triage false positives
  after. Do not ship a detector chosen for a clean precision number.

## Reduce the surface before you scrub

- **default-deny** — where feasible, allowlist what may leave the boundary rather than blocklist
  what must be hidden. An unrecognized new field, project, or source is then excluded by
  default, so a gap **fails closed** instead of silently publishing.
- **drop-structurally** — remove PII-bearing fields at the schema or serialization boundary, not
  by string-scrubbing them out of an already-built payload. A dropped field cannot leak; a
  scrubbed one relies on the scrubber being perfect. See `pii-handling`.

## Redact with the right operation

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

## Verify — do not trust the filter

- **fail-closed-backstop** — after redaction you MUST re-scan the serialized output and hard-fail
  the emit or build if any pattern survives. A filter that silently misses is worse than none,
  because the output *looks* safe.
- **defense-in-depth** — layer independent gates (surface reduction → structural drop → prose
  substitution → assertion) so one layer's miss is caught by the next.
- **golden-tests** — keep a known-leaky fixture and assert end-to-end that nothing survives.
  Freeze real edge cases as regression tests — e.g. a `git@github.com:` SSH remote that looks
  email-shaped but must be kept, or a `~/tool` path that must not be redacted like a home path.

## Repositories keep history

- **scan-history-not-just-the-tip** — redacting the working tree does NOT purge PII or secrets
  already committed; git retains them in prior commits even after the file changes. Treat a
  public repo's history as part of the exposed surface.
- **remediate-then-rotate** — purge with `git filter-repo` (or BFG Repo-Cleaner), force-update
  the remote, and **rotate** any exposed secret — a purged credential that was public must be
  assumed compromised. `gitleaks` (fast regex/entropy, good in a pre-commit hook) and
  `trufflehog` (verifies whether a found credential is still live, good for full-history scans)
  are the standard scanners.
