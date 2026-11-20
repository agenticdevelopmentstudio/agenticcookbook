
- `separate-server-and-client`: whether server state and client state are managed by separate mechanisms
- `no-hand-cached-server-state`: whether any server data is hand-cached in a global client store
- `query-layer-for-server-state`: whether server state lives in a query/cache layer with the server as the source of truth
- `local-state-for-client-state`: whether client state uses the lightest mechanism that works
- `context-for-slow-changing-config`: whether context carries only slow-changing, app-wide configuration
- `choose-a-mechanism-in-decision-order`: whether each piece of state's mechanism follows the decision order
- `name-the-role-not-the-brand`: whether the design names roles rather than brands
- `treat-the-tool-as-an-implementation-detail`: whether the library is treated as a swappable implementation detail
- `client-store-only-when-local-state-falls-short`: whether each client store is justified by local state and lifting falling short
