
These are deliberate, swappable choices — name the role, not the brand. Libraries in this space churn; treat the pattern as durable and the tool as an implementation detail.

- **Server-state / query layer**: TanStack Query (formerly React Query) is a common choice and provides caching, dedup, background refetch, and mutation + invalidation. SWR and RTK Query fill the same role. The framework-agnostic lesson is "use a query cache," not "use this package."
- **Client store**: Zustand and Jotai are lightweight options; Redux Toolkit suits larger apps with structured updates. Reach for one only when local state and lifting genuinely fall short (see YAGNI).
- **Config context**: the framework's built-in context API.

