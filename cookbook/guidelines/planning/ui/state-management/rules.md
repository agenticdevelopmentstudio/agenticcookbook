
- **separate-server-and-client**: Server state and client state MUST be managed by separate mechanisms. Do not store fetched server data in the same construct used for UI toggles.
- **no-hand-cached-server-state**: Server data SHOULD NOT be hand-cached in a global client store (e.g., copying a fetch result into Redux/Zustand and manually keeping it fresh). This is a named anti-pattern: you end up reimplementing caching, deduplication, and invalidation by hand, and the copy drifts from the source of truth.
- **query-layer-for-server-state**: Server state SHOULD live in a dedicated query/cache layer that provides caching, request deduplication, background refetching, and mutation-with-invalidation. The server, not your store, remains the source of truth.
- **local-state-for-client-state**: Client state SHOULD use the lightest mechanism that works — component-local state first, lifting state up when genuinely shared, and a small global store only when many distant components need the same value.
- **context-for-slow-changing-config**: Framework context (e.g., React Context) SHOULD carry slow-changing, app-wide configuration (theme, locale, authenticated user, feature flags) — NOT high-frequency or rapidly-mutating state, because every context value change re-renders all consumers.

- **choose-a-mechanism-in-decision-order**: You SHOULD choose a state mechanism by asking, in order:
  1. **Is it server data?** Put it in a query/cache layer. Cache key = the request identity. Read from the cache; mutate, then invalidate the affected keys to trigger refetch. Do not mirror it elsewhere.
  2. **Does only one component need it?** Use component-local state.
  3. **Do a few nearby components need it?** Lift the state to the nearest common ancestor and pass it down.
  4. **Do many distant components need it?** Use a small client store scoped to that concern.
  5. **Is it app-wide config that rarely changes?** Use context.
- **name-the-role-not-the-brand**: State libraries are deliberate, swappable choices; you SHOULD name the role, not the brand.
- **treat-the-tool-as-an-implementation-detail**: Libraries in this space churn; you SHOULD treat the pattern as durable and the tool as an implementation detail.
- **client-store-only-when-local-state-falls-short**: You SHOULD reach for one client-store library only when local state and lifting genuinely fall short (see YAGNI).
