
Default for resource-oriented CRUD, public APIs, and anything that benefits from HTTP semantics.

- **Choose REST when** consumers are diverse/external, resources map cleanly to URLs, and HTTP caching (`ETag`, `Cache-Control`, CDN) adds value.
- It **SHOULD** be the default unless a measured need (latency, streaming, fan-out) justifies another style.
- Strengths: ubiquitous tooling, human-readable, cacheable, easy to debug with `curl`.
- Pin contracts to a dated OpenAPI revision; version the API (`/v1`) per `api-design`.

