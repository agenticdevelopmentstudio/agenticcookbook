
- `must-use-problem-details`: whether every error response uses RFC 9457 Problem Details with `Content-Type: application/problem+json`
- `must-include-type`: whether every problem response carries a `type` URI
- `must-keep-title-stable`: whether each `title` is stable across occurrences
- `must-mirror-status`: whether `status` matches the response's HTTP status code
- `may-add-extension-fields`: whether extra error data goes in extension fields
