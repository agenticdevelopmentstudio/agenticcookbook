
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

