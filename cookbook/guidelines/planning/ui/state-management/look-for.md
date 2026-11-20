
- `no-hand-cached-server-state`: Fetching in a `useEffect` and writing the result into a global store, then manually refetching on focus/interval — that is reimplementing a query cache poorly.
- `separate-server-and-client`: A single "app state" store that mixes the user list (server) with `isSidebarOpen` (client).
- `context-for-slow-changing-config`: Putting frequently-changing values in React Context and triggering app-wide re-renders.
- `query-layer-for-server-state`: Treating the client store as the source of truth for data that actually lives on the server.
- `local-state-for-client-state`: client state held in a global store when component-local state or lifting would do
- `choose-a-mechanism-in-decision-order`: a mechanism chosen out of order, such as server data mirrored outside the query layer, or a store where one component's local state would do
- `name-the-role-not-the-brand`: a design that names a library where it should name the role it fills
- `treat-the-tool-as-an-implementation-detail`: a design coupled to one library's API rather than to the pattern
- `client-store-only-when-local-state-falls-short`: a client store added where local state and lifting were enough
