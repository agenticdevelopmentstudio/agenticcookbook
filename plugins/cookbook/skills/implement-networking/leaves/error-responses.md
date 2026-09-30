<!-- leaf: implement-networking/error-responses · source: guidelines/implementing/networking/error-responses.md -->

**Rules** (cite as `implement-networking/error-responses#<slug>`):

- `error-responses-use-rfc-9457-problem` MUST — Error responses MUST use RFC 9457 Problem Details format with Content-Type: application/problem+json:
- `type` MUST (URI)
- `title` MUST
- `status` MUST

# Error Responses

Error responses MUST use [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457) format with
`Content-Type: application/problem+json`:

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "Request body contains 2 validation errors.",
  "instance": "/orders/abc-123",
  "errors": [
    { "field": "email", "message": "Must be a valid email address" },
    { "field": "age", "message": "Must be >= 0" }
  ]
}
```

- **type** (URI) — machine-readable error identifier (MUST be present)
- **title** — short human-readable summary (MUST be stable across occurrences)
- **status** — HTTP status code (MUST mirror response)
- **detail** — explanation specific to this occurrence
- **instance** — identifies the specific request
- Add extension fields (`errors`, `trace_id`) as needed
