
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

