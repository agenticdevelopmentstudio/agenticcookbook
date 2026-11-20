
- The decision variable is **how much JavaScript reaches the client, and when**. Frame rendering as an architecture-selection decision, not a framework choice.
- You **SHOULD** select a rendering strategy **per route**, not one strategy for the whole app. A marketing landing page and a logged-in dashboard have different constraints.
- You **MUST NOT** mandate a framework to satisfy this guideline. The same per-route reasoning applies to React, Svelte/SvelteKit, Vue/Nuxt, Astro, SolidStart, Qwik, and others.
- Note: INP replaced FID as a Core Web Vital on 2024-03-12. Optimize for INP and LCP; do **not** target FID.

