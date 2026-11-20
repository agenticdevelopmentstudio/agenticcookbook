
- Fetching in a `useEffect` and writing the result into a global store, then manually refetching on focus/interval — that is reimplementing a query cache poorly.
- A single "app state" store that mixes the user list (server) with `isSidebarOpen` (client).
- Putting frequently-changing values in React Context and triggering app-wide re-renders.
- Treating the client store as the source of truth for data that actually lives on the server.

