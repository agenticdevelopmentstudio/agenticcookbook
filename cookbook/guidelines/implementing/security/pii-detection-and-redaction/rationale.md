
- `two-identifier-classes`: A feed can be
  email-free and still leak identity through quasi-identifiers — scanning only for direct
  identifiers is the most common blind spot.
- `detect-in-layers`: No single technique is sufficient.
- `regex-for-structured`: Necessary but noisy: raw patterns over-flag benign strings that share
  a shape.
- `context-words`: Context lowers both false positives and misses without new patterns.
- `ner-for-unstructured`: Regex cannot find names, places, or organizations in unstructured text.
- `favor-recall`, `should-not-ship-precision-chosen-detector`: For PII a miss is worse than a false alarm.
- `default-deny`: An unrecognized new field, project, or source is then excluded by
  default, so a gap **fails closed** instead of silently publishing.
- `drop-structurally`: A dropped field cannot leak; a
  scrubbed one relies on the scrubber being perfect.
- `pick-operation-by-need`: These are not interchangeable.
- `fail-closed-backstop`: A filter that silently misses is worse than none,
  because the output *looks* safe.
- `scan-history-not-just-the-tip`: Redacting the working tree does NOT purge PII or secrets
  already committed; git retains them in prior commits even after the file changes, so scan the history, not just the tip.
