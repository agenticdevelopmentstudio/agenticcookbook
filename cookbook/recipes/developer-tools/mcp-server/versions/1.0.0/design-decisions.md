
**Decision**: Make `mcp-tool` the only required ingredient; treat resources and prompts as in-recipe primitive choices rather than separate ingredients.
**Rationale**: A server with no tools has nothing model-invocable to offer, so at least one tool is the floor (yagni — do not require ingredients that may not exist yet). Resources and prompts share the same transport, handshake, and auth surface as tools and are selected by purpose within this recipe; promoting them to separate ingredients now would be speculative structure (design-for-deletion, small-reversible-decisions). They can be extracted into their own ingredients later if their specs grow.
**Approved: pending**

**Decision**: Pin protocol/transport guidance to the 2025-11-25 revision and authorization/security guidance to the 2025-06-18 revision, negotiating the revision at `initialize` rather than hard-coding it.
**Rationale**: The two concern areas stabilized on different dated revisions; citing each to its authoritative revision is explicit-over-implicit and avoids overstating where a single revision governs everything. Negotiating at runtime (rather than baking in a constant) keeps the server portable across hosts and optimizes-for-change as the spec advances. Release-candidate revisions are forecasts and stay behind opt-in to avoid building on unstable ground.
**Approved: pending**

