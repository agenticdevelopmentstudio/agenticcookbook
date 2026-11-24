
This section is informative; the record below is an illustration, not a required format.

A selection record for one change:

```text
Base: 4e1f0a2 (latest main commit with a green CI run)   Head: 9c7d3b1
Changed files (3): lib/pricing/discount.ts, lib/pricing/discount.test.ts, package-lock.json
Selected by graph:
  lib/pricing/discount.ts      -> pricing:test (declared input), checkout:test (depends
                                  on pricing), cart:test (depends on pricing)
  lib/pricing/discount.test.ts -> pricing:test (declared input)
Fallback: yes, for package-lock.json, a shared input the graph cannot trace to tests.
Selected by fallback (package-lock.json): every test that uses an npm dependency:
  pricing:test, checkout:test, cart:test, search:test
Selected by history (window: last 10 runs): tools:test (failed 2 runs ago)
Not selected: docs:test (uses no npm dependency, has no path to a changed file and
  has not been added, changed, failed or flaky in the last 10 runs)
Full suite: runs after merge to main
```

