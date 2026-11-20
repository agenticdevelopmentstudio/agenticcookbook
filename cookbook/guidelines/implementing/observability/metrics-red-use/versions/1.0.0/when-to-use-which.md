
- **RED** — request-handling work: HTTP/gRPC endpoints, message consumers, RPC handlers, queue workers. Measures the caller's experience (external/workload view).
- **USE** — finite resources: CPU, memory, disk, network interfaces, connection pools, thread pools, queues, file descriptors (internal/resource view).
- A single component often needs both: a service emits RED for its endpoints AND USE for its connection pool and worker queue.

