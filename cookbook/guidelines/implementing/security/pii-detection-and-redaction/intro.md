
# PII detection and redaction

Finding personal data is a detection problem before it is a redaction problem: you cannot
scrub what you did not recognize. Detect in layers, redact with the operation that fits the
use, and verify with a backstop that fails closed. Classification, encryption, and log hygiene
live in `pii-handling`; this page covers *finding* PII in free text, data, and repositories and
*removing* it safely. This is engineering guidance and NOT legal advice; confirm obligations
with counsel.

