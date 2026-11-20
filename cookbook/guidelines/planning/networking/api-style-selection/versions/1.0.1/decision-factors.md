
You **MUST** weigh these before selecting a style:

- **Consumer**: public/third-party, first-party web/mobile, or internal service-to-service.
- **Traffic shape**: request/response CRUD, high-frequency low-latency RPC, streaming, or wide-fan-out aggregation across many resources.
- **Tooling and team**: existing client stacks, codegen tolerance, debuggability (human-readable vs binary).
- **Caching**: whether HTTP intermediary/CDN caching is valuable.

