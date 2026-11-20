
- **must-use-problem-details**: Error responses MUST use [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457) format with `Content-Type: application/problem+json`.
- **must-include-type**: **type** (URI) — the machine-readable error identifier MUST be present.
- **must-keep-title-stable**: **title** — the short human-readable summary MUST be stable across occurrences.
- **must-mirror-status**: **status** — the HTTP status code MUST mirror the response.
- **may-add-extension-fields**: Error responses MAY add extension fields (`errors`, `trace_id`) as needed.
