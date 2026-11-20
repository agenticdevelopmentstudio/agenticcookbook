
1. **Is it server data?** Put it in a query/cache layer. Cache key = the request identity. Read from the cache; mutate, then invalidate the affected keys to trigger refetch. Do not mirror it elsewhere.
2. **Does only one component need it?** Use component-local state.
3. **Do a few nearby components need it?** Lift the state to the nearest common ancestor and pass it down.
4. **Do many distant components need it?** Use a small client store scoped to that concern.
5. **Is it app-wide config that rarely changes?** Use context.

