
# Choose a rendering strategy per route, minimize client JS

The amount of JavaScript that reaches the client — and *when* it arrives — is the primary lever on Interaction to Next Paint (INP) and Largest Contentful Paint (LCP). There is no single winning strategy: the industry has converged on hybrid, per-route rendering. Choose the strategy per route based on that route's job, and default to shipping less client JS.

