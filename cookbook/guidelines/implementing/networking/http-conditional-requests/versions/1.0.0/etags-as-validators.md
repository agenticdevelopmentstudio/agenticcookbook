
- The server **MUST** return an `ETag` response header on representations that participate in conditional requests. An ETag is an opaque token identifying a specific resource version.
- Strong ETags (`"abc"`) assert byte-for-byte equivalence; weak ETags (`W/"abc"`) assert only semantic equivalence. The server **SHOULD** emit strong ETags for write concurrency, since `If-Match` uses the strong comparison.
- Clients **MUST** treat ETag values as opaque — do not parse, compare substrings of, or derive meaning from them.

