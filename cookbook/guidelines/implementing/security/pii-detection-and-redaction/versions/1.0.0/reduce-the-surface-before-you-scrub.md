
- **default-deny** — where feasible, allowlist what may leave the boundary rather than blocklist
  what must be hidden. An unrecognized new field, project, or source is then excluded by
  default, so a gap **fails closed** instead of silently publishing.
- **drop-structurally** — remove PII-bearing fields at the schema or serialization boundary, not
  by string-scrubbing them out of an already-built payload. A dropped field cannot leak; a
  scrubbed one relies on the scrubber being perfect. See `pii-handling`.

