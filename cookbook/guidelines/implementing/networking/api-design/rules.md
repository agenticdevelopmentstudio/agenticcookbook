
- **should-use-consistent-rest**: APIs SHOULD use REST with consistent conventions.
- **should-follow-platform-api-guidelines**: APIs SHOULD follow the platform API guidelines (Microsoft, Google, Zalando) for details.

**URL conventions:**
- **must-use-lowercase-hyphenated-urls**: URLs MUST be lowercase with hyphens: `/order-items` not `/orderItems`
- **must-use-plural-collection-nouns**: Collections MUST use plural nouns: `/users`, `/orders`
- **should-nest-urls-shallowly**: Nesting SHOULD be shallow (max 2 levels): `/users/{id}/orders`
- **must-not-put-verbs-in-urls**: URLs MUST NOT contain verbs — the HTTP method is the verb
- **must-not-use-trailing-slashes**: Trailing slashes MUST NOT be used
- **should-filter-and-sort-with-query-params**: Filtering and sorting SHOULD use query params: `/users?status=active&sort=-created_at`

**HTTP methods:**
- **should-follow-http-method-semantics**: Each HTTP method SHOULD carry the semantics, idempotency and success code the HTTP methods table gives it.

**Status codes — use the right one:**
- **should-use-the-right-status-code**: Responses SHOULD use the right status code, from the status codes listed.

**Versioning:**
- **should-version-in-the-url-path**: APIs SHOULD use URL path versioning (`/v1/users`).
- **should-bump-major-only-for-breaking-changes**: APIs SHOULD bump the major version only for breaking changes.
- **should-display-field-level-errors-for-422**: Clients SHOULD display field-level errors for 422 responses.
