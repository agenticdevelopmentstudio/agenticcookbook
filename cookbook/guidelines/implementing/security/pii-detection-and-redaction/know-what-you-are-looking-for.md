
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

