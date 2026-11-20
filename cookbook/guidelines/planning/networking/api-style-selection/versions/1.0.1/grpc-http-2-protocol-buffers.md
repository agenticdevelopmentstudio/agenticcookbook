
Use for low-latency internal service-to-service calls and streaming, per the official model (RPC over HTTP/2 with Protocol Buffers as the IDL and serialization; see references).

- **Choose gRPC when** callers are internal services, latency/throughput matter, you want generated client/server stubs across languages, or you need uni-/bi-directional streaming.
- Strengths: compact binary payloads, strict schema via `.proto`, codegen, HTTP/2 multiplexing.
- Trade-offs: not human-readable; browsers need a proxy (e.g. gRPC-Web/Connect); limited intermediary HTTP caching.
- You **SHOULD NOT** expose raw gRPC as a public third-party API without a REST/Connect façade.

