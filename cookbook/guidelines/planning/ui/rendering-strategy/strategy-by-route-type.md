
| Route type | Recommended strategy | Why |
|---|---|---|
| Content-heavy, mostly static (docs, blog, marketing) | Static generation (SSG) + islands | Near-zero client JS; hydrate only interactive islands |
| Dynamic but cacheable | SSR with caching / ISR-style revalidation | Fresh HTML, cheap to serve, fast LCP |
| Personalized / data-driven app pages | Streaming SSR with Suspense | First paint streams while data resolves; lower TTFB-to-content |
| Highly interactive, slow-startup-dominated | Resumability (e.g. Qwik) or aggressive code-splitting | Avoids large hydration cost at startup |
| Behind auth, no SEO need | Client-side render (SPA) only if SSR adds no value | Simplicity when crawlability and first-paint don't matter |

