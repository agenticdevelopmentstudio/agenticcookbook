
- `must-use-problem-details`: every error response has an RFC 9457 Problem Details body and `Content-Type: application/problem+json`
- `must-include-type`: every problem body has a `type` URI
- `must-keep-title-stable`: each error `type` has one fixed `title`
- `must-mirror-status`: each problem body's `status` equals the response's HTTP status code
- `may-add-extension-fields`: any extra error data is in named extension fields (`errors`, `trace_id`)
- `must-not-show-raw-status-codes`: no raw HTTP status code is shown to the user
