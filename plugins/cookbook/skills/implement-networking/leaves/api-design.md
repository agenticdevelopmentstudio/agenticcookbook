<!-- leaf: implement-networking/api-design · source: guidelines/implementing/networking/api-design.md -->

**Rules** (cite as `implement-networking/api-design#<slug>`):

- `urls-lowercase-hyphens-order-items` MUST — URLs MUST be lowercase with hyphens: /order-items not /orderItems
- `collections-use-plural-nouns-users` MUST — Collections MUST use plural nouns: /users, /orders
- `nesting-shallow-max-levels-users` SHOULD — Nesting SHOULD be shallow (max 2 levels): /users/{id}/orders
- `urls-not-contain-verbs-http-method` MUST — URLs MUST NOT contain verbs — the HTTP method is the verb
- `trailing-slashes-not-used` MUST — Trailing slashes MUST NOT be used

# API Design

Use REST with consistent conventions. Follow the platform API guidelines (Microsoft, Google,
Zalando) for details — the essentials below are consensus across all three.

**URL conventions:**
- URLs MUST be lowercase with hyphens: `/order-items` not `/orderItems`
- Collections MUST use plural nouns: `/users`, `/orders`
- Nesting SHOULD be shallow (max 2 levels): `/users/{id}/orders`
- URLs MUST NOT contain verbs — the HTTP method is the verb
- Trailing slashes MUST NOT be used
- Query params for filtering/sorting: `/users?status=active&sort=-created_at`

**HTTP methods:**

| Method | Semantics | Idempotent | Success Code |
|--------|-----------|------------|-------------|
| GET | Read | Yes | 200 |
| POST | Create | No | 201 + Location |
| PUT | Full replace | Yes | 200 |
| PATCH | Partial update | No | 200 |
| DELETE | Remove | Yes | 204 (no body) |

**Status codes — use the right one:**
- **200** OK — **201** Created — **204** No Content — **202** Accepted (async)
- **400** Bad Request — **401** Unauthorized — **403** Forbidden — **404** Not Found
- **409** Conflict — **422** Unprocessable Entity — **429** Too Many Requests
- **500** Internal Server Error — **503** Service Unavailable

**Versioning:** URL path versioning (`/v1/users`). Simple, explicit, industry consensus. Bump
major version only for breaking changes.
