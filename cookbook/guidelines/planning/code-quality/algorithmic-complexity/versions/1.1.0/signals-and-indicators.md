
**Sorting and search patterns:**

- Explicit sort calls with custom comparators — note whether the comparator is simple (field comparison) or compound (multi-key, weighted)
- Binary search implementations or calls to `binarySearch`, `lower_bound`, `upper_bound` — implies sorted input requirement
- Linear scan patterns over large collections — potential O(n) performance risk
- Priority queue usage (`PriorityQueue`, `Heap`, `sorted` sets) — implies ordering-sensitive processing

**Graph and tree traversals:**

- Explicit adjacency list or matrix construction
- BFS/DFS implementations — note cycle detection, visited sets
- Tree traversal patterns — in-order, pre-order, post-order, level-order
- Shortest path algorithms — Dijkstra, Bellman-Ford, A*
- Topological sort — implies dependency graph processing

**Caching and memoization:**

- `NSCache`, `LRUCache`, dictionary-as-cache patterns with explicit eviction logic
- `@cached_property`, `lazy var`, `lazy` computed properties — single-computation caches
- Memoization wrappers — functions that store prior results indexed by input
- Cache invalidation logic — expiry timestamps, version keys, dependency tracking
- Write-through vs write-back cache patterns

**Data structure choices:**

- Hash maps / dictionaries — O(1) lookup; note when used for frequency counting, grouping, or deduplication
- Sets for membership testing — note when used to eliminate duplicates from a stream
- Queues and deques — FIFO processing, sliding window patterns
- Linked lists — unusual in high-level languages; presence often indicates specialized ordering or O(1) insert/delete requirements
- Bloom filters or probabilistic structures — indicates performance-critical membership testing
- Tries — prefix search, autocomplete, routing tables
- Segment trees, Fenwick trees — range query optimization

**Recursion:**

- Deep recursion without tail-call optimization — stack overflow risk in large inputs
- Mutually recursive functions — complex control flow, harder to profile
- Trampoline patterns — recursive logic rewritten iteratively for stack safety

**Nested loops and complexity indicators:**

- Double nested loops over the same collection — O(n²) risk
- Triple or deeper nesting — O(n³) or worse; flag immediately
- Early-exit conditions (`break`, `guard`, `return`) that may redeem apparent O(n²) to amortized O(n)
- Outer loop over data, inner loop over configuration — often O(n×m) where m is small and bounded

**Parallelism and concurrency in computation:**

- `DispatchQueue.concurrentPerform`, `parallel()`, `ParallelStream`, `PLINQ`, `async/await` over collections — parallel computation patterns
- GPU compute (Metal, Vulkan, WebGPU compute shaders) — highly parallel numeric computation
- SIMD operations — vectorized arithmetic

**Numeric and signal processing:**

- Floating point accumulation patterns — summation, running averages; note precision concerns
- FFT or frequency domain processing
- Matrix multiplication — note if using accelerated libraries (Accelerate, BLAS, NumPy)
- Statistical computation — mean, variance, standard deviation, percentile calculation

