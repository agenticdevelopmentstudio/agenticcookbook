<!-- leaf: plan-networking/api-style-selection · source: guidelines/planning/networking/api-style-selection.md -->

**Rules** (cite as `plan-networking/api-style-selection#<slug>`):

- `boundary-single-system-use-more-than-one` MUST — Pick the API style from who consumes the endpoint and the shape of its traffic, not from fashion. REST, gRPC, and …
- `you-weigh-before-selecting-style` MUST — You MUST weigh these before selecting a style:
- `default-unless-measured-need` SHOULD — It SHOULD be the default unless a measured need (latency, streaming, fan-out) justifies another style.
- `you-not-expose-raw-grpc-public` SHOULD — You SHOULD NOT expose raw gRPC as a public third-party API without a REST/Connect façade.
- `you-mitigate-problem-batching-dataloader` MUST — You MUST mitigate the N+1 problem (e.g. batching/dataloader patterns) and MUST enforce query depth/complexity limits to …
- `system-combine-styles-different-boundaries` MAY — A system MAY combine styles at different boundaries (e.g. gRPC internally, REST or GraphQL at the edge); this is a …
- `boundary-document-own-style-decision` MUST — Each boundary MUST document its own style decision and contract source.

# Choosing an API style (REST, gRPC, GraphQL)

Pick the API style from who consumes the endpoint and the shape of its traffic, not from fashion. REST, gRPC, and GraphQL each optimize for a different boundary; a single system MAY use more than one. The choice **MUST** be recorded as a deliberate decision with its rationale (see the related `api-design` guideline).

## Decision factors

You **MUST** weigh these before selecting a style:

- **Consumer**: public/third-party, first-party web/mobile, or internal service-to-service.
- **Traffic shape**: request/response CRUD, high-frequency low-latency RPC, streaming, or wide-fan-out aggregation across many resources.
- **Tooling and team**: existing client stacks, codegen tolerance, debuggability (human-readable vs binary).
- **Caching**: whether HTTP intermediary/CDN caching is valuable.

## REST (HTTP/JSON)

Default for resource-oriented CRUD, public APIs, and anything that benefits from HTTP semantics.

- **Choose REST when** consumers are diverse/external, resources map cleanly to URLs, and HTTP caching (`ETag`, `Cache-Control`, CDN) adds value.
- It **SHOULD** be the default unless a measured need (latency, streaming, fan-out) justifies another style.
- Strengths: ubiquitous tooling, human-readable, cacheable, easy to debug with `curl`.
- Pin contracts to a dated OpenAPI revision; version the API (`/v1`) per `api-design`.

## gRPC (HTTP/2 + Protocol Buffers)

Use for low-latency internal service-to-service calls and streaming, per the official model (RPC over HTTP/2 with Protocol Buffers as the IDL and serialization; see references).

- **Choose gRPC when** callers are internal services, latency/throughput matter, you want generated client/server stubs across languages, or you need uni-/bi-directional streaming.
- Strengths: compact binary payloads, strict schema via `.proto`, codegen, HTTP/2 multiplexing.
- Trade-offs: not human-readable; browsers need a proxy (e.g. gRPC-Web/Connect); limited intermediary HTTP caching.
- You **SHOULD NOT** expose raw gRPC as a public third-party API without a REST/Connect façade.

## GraphQL

Use when clients drive aggregation across many resources and over/under-fetching with REST is a measured problem.

- **Choose GraphQL when** first-party clients need to compose data from several sources in one round trip and field-level shape varies by screen.
- You **MUST** mitigate the N+1 problem (e.g. batching/dataloader patterns) and **MUST** enforce query depth/complexity limits to bound cost.
- Caching is field-level and client-driven, not HTTP-intermediary; do not assume CDN caching applies.
- Treat the schema as a versioned contract; prefer additive evolution and field deprecation over breaking changes.

## Mixing styles

- A system **MAY** combine styles at different boundaries (e.g. gRPC internally, REST or GraphQL at the edge); this is a normal, deliberate choice, not a smell.
- Each boundary **MUST** document its own style decision and contract source.

## Anti-patterns

- Selecting GraphQL or gRPC for a simple CRUD service "to be modern" — start with REST unless a need is demonstrated (YAGNI).
- Exposing internal gRPC contracts directly to untrusted/public clients.
- Adopting GraphQL without complexity limits or N+1 mitigation in place.
