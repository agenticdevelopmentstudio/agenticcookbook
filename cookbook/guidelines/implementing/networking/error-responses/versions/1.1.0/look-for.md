
- `must-use-problem-details`: an error body in an ad-hoc shape, or one sent as `application/json` instead of `application/problem+json`.
- `must-include-type`: a problem response with no `type` URI.
- `must-keep-title-stable`: a `title` built from the occurrence (ids, counts, field names) so it changes between occurrences of the same error.
- `must-mirror-status`: a `status` field that differs from the HTTP status code of the response.
- `may-add-extension-fields`: occurrence data (such as per-field errors or a trace id) packed into `detail` or `title` instead of extension fields.
