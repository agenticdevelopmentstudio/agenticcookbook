
- **Server-state / query layer**: TanStack Query (formerly React Query) is a common choice and provides caching, dedup, background refetch, and mutation + invalidation. SWR and RTK Query fill the same role. The framework-agnostic lesson is "use a query cache," not "use this package."
- **Client store**: Zustand and Jotai are lightweight options; Redux Toolkit suits larger apps with structured updates.
- **Config context**: the framework's built-in context API.
