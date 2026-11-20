
INP captures the worst (near-worst) interaction latency across the page's lifetime, so a single janky handler fails it. Mitigations, in order of leverage:

- **Break up long tasks** — split work > 50ms into smaller chunks so the main thread can paint and handle input between them.
- **Yield to the main thread.** Prefer `scheduler.yield()` where available — note it is **Chromium-supported but NOT yet Baseline** as of 2026 (limited availability). Provide a fallback: feature-detect and degrade to `await new Promise(r => setTimeout(r))` (loses the prioritized continuation) or the `scheduler-polyfill`.
- **Move heavy computation to a Web Worker** (parsing, diffing, crypto, image work) to keep the main thread free for rendering and input.
- **Avoid layout thrashing** — batch DOM reads then writes; never interleave reads/writes in a loop that forces synchronous reflow.
- **Keep the DOM small** — oversized DOM trees (thousands of nodes) inflate style/layout cost on every interaction. Virtualize long lists.
- **Defer non-critical work** to idle time (`requestIdleCallback`) or post-interaction.

