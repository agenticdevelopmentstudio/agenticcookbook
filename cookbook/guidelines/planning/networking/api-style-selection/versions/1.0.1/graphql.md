
Use when clients drive aggregation across many resources and over/under-fetching with REST is a measured problem.

- **Choose GraphQL when** first-party clients need to compose data from several sources in one round trip and field-level shape varies by screen.
- You **MUST** mitigate the N+1 problem (e.g. batching/dataloader patterns) and **MUST** enforce query depth/complexity limits to bound cost.
- Caching is field-level and client-driven, not HTTP-intermediary; do not assume CDN caching applies.
- Treat the schema as a versioned contract; prefer additive evolution and field deprecation over breaking changes.

