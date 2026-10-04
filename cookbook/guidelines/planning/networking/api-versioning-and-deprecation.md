---
id: c4273664-4d26-477b-b778-ac1e9b51f385
title: "API versioning and deprecation"
domain: agenticdevelopercookbook://guidelines/planning/networking/api-versioning-and-deprecation
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Evolve APIs additively; when versioning is unavoidable pick one scheme and run a header-driven deprecation lifecycle."
platforms: []
tags:
  - api
  - versioning
  - lifecycle
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/planning/networking/api-design
  - agenticdevelopercookbook://guidelines/reviewing/networking/observable-behavior-contract
references:
  - https://www.rfc-editor.org/rfc/rfc8594.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - api-integration
---

# API versioning and deprecation

Most API change can be additive and never needs a new version. When a breaking change is genuinely required, version it deliberately and run a disciplined, header-driven deprecation lifecycle so consumers get a removal date and a migration window — never a silent break.

## Evolve additively first

- You **MUST** treat additive changes (new optional fields, new endpoints, new optional query params, new enum values consumers can ignore) as non-breaking and ship them without a version bump.
- You **MUST** treat these as breaking and requiring a version: removing or renaming a field, changing a type or units, tightening validation, changing defaults, altering status codes, or changing pagination/auth semantics.
- Clients **MUST** tolerate unknown fields (ignore, don't reject) so the server can add fields freely. Per the observable-behavior-contract guideline (Hyrum's Law), assume consumers depend on *every* observable detail — undocumented field order, error text, timing — so changing those can break someone even when the spec did not.

## Choosing a versioning scheme (a decision, not a mandate)

Pick ONE scheme and apply it consistently across the whole surface. Each is a deliberate trade-off:

| Scheme | Form | Trade-off |
|--------|------|-----------|
| URI path | `/v2/orders` | Most visible and cacheable; couples version to URL, harder for fine-grained evolution |
| Media-type / header | `Accept: application/vnd.acme.v2+json` | Keeps URLs stable, content-negotiation friendly; less obvious, easy to omit |
| Query param | `/orders?version=2` | Simple; pollutes URLs and caches, easy to forget |

- You **MUST NOT** mix schemes within one API.
- You **SHOULD** version at a coarse grain (major version per breaking batch), not per endpoint or per field.
- Unversioned requests **SHOULD** resolve to a documented, pinned default version rather than "latest", so default behavior cannot shift under a client.

## Deprecation lifecycle

When retiring a version or endpoint, run this sequence and publish the timeline before the first signal ships:

1. **Announce** — set the `Deprecation` response header (RFC 9745, published March 2025) on affected responses. Value is the deprecation timestamp or `true`. You **SHOULD** add a `Link` header with `rel="deprecation"` and `rel="successor-version"` pointing at migration docs.
2. **Set a removal date** — add the `Sunset` header (RFC 8594) with the HTTP-date after which behavior is undefined. The `Sunset` time **MUST NOT** be earlier than the `Deprecation` time.
3. **Document** — record the change, replacement, and dates in a public changelog and the OpenAPI/spec (`deprecated: true`).
4. **Honor a migration window** — give consumers a published, generous window before removal; do not shorten it after announcement.

```
Deprecation: @1717200000
Sunset: Wed, 31 Mar 2027 23:59:59 GMT
Link: <https://api.acme.com/docs/migrate-v2>; rel="successor-version"
```

- Breaking changes **MUST** be versioned, never shipped in place.
- Deprecations **SHOULD** use `Deprecation` + `Sunset` headers plus a changelog entry; headers are hints, so they **MUST** be paired with documentation, not used alone.
- You **SHOULD** emit metrics on deprecated-version traffic and notify identifiable high-volume consumers directly before removal.

## Anti-patterns

- Silently changing behavior of an existing version (breaks the observable-behavior-contract).
- Removing an endpoint with no `Sunset` date or before the announced window.
- Auto-upgrading unversioned clients to "latest".
- A new major version per trivial change, multiplying surfaces you must maintain.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
