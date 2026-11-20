
- `separate-server-and-client`: no construct holds both fetched server data and UI toggles
- `no-hand-cached-server-state`: no global client store holds a hand-cached copy of server data, or the work says why
- `query-layer-for-server-state`: server state is read through a query/cache layer with caching, dedup, background refetch and mutation-with-invalidation, or the work says why not
- `local-state-for-client-state`: each piece of client state uses component-local state, lifted state, or a small store only for many distant consumers, or the work says why not
- `context-for-slow-changing-config`: context values are slow-changing, app-wide configuration only, or the work says why not
- `choose-a-mechanism-in-decision-order`: each piece of state sits in the mechanism the decision order gives it, or the work says why not
- `name-the-role-not-the-brand`: the design names each library's role, or the work says why not
- `treat-the-tool-as-an-implementation-detail`: the library can be swapped without changing the pattern, or the work says why not
- `client-store-only-when-local-state-falls-short`: each client store names where local state and lifting fell short, or the work says why not
