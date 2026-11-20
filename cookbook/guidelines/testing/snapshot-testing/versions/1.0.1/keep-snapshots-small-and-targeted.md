
- A snapshot **SHOULD** cover one concern — a single component's rendered output, one function's serialized result — not an entire page or aggregate object graph.
- You **SHOULD** prefer many small inline snapshots (`toMatchInlineSnapshot`, inline approval) over one large external file. Inline snapshots keep the expected value next to the test, so reviewers see intent in the diff.
- You **SHOULD NOT** snapshot output you cannot reason about line by line. A giant auto-generated snapshot that no one reviews is the core anti-pattern: it appears to test much and tests nothing (`yagni`, `explicit-over-implicit`).

