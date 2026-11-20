
- `must-use-problem-details`: whether every error response uses RFC 9457 Problem Details with `Content-Type: application/problem+json`
- `must-include-type`: whether every problem response carries a `type` URI
- `must-keep-title-stable`: whether each `title` is stable across occurrences
- `must-mirror-status`: whether `status` matches the response's HTTP status code
- `may-add-extension-fields`: whether extra error data goes in extension fields
- `may-add-extension-fields`: field errors from `errors[]` shown inline;
- `must-not-show-raw-status-codes`: no raw status codes shown to user;
- `may-add-extension-fields`: field-level errors use `errors` array;
