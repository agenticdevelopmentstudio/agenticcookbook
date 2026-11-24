
This section is informative; the record below is an illustration, not a required format.

A selection record for one change:

```text
Base: 4e1f0a2 (latest main commit with a green CI run)   Head: 9c7d3b1
Changed files (3): lib/pricing/discount.ts, lib/pricing/discount.test.ts, package-lock.json
Fallback: yes. package-lock.json is a shared input the graph cannot trace to tests,
  so every test that uses an npm dependency is selected.
Selected by graph: pricing:test (input lib/pricing/discount.ts), checkout:test
  (depends on pricing), cart:test (depends on pricing)
Selected by history: search:test (failed on the previous run)
Not selected: tools:test (uses no npm dependency and has no path to a changed file)
Full suite: runs after merge to main
```

