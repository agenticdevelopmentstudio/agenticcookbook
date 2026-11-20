
- You **SHOULD** record the chosen strategy per route (e.g. in the route's plan or a routing manifest) with a one-line rationale, so the decision is reversible and auditable.
- You **SHOULD** keep strategies swappable: avoid coupling business logic to a rendering mode so a route can move from SSR to SSG (or vice versa) as requirements change.
- You **MUST** validate the choice against real metrics (INP, LCP, TTFB, JS transfer size) on representative routes before locking it in.

