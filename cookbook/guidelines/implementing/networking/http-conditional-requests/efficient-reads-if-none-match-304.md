
- Clients **SHOULD** send `If-None-Match: <etag>` (echoing the ETag from a prior response) on repeat GET/HEAD requests.
- If the resource is unchanged, the server **MUST** return `304 Not Modified` with no body, including `ETag`, `Cache-Control`, and `Vary` if present. The client reuses its cached representation.
- `If-None-Match` uses weak comparison and **SHOULD** be preferred over `If-Modified-Since` (1-second granularity) when an ETag exists.

