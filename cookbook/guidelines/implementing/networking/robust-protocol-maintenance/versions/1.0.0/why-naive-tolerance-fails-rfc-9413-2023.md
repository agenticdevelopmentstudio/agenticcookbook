
- Silently accepting malformed input creates a **pathological feedback cycle**: the deviation goes unreported, spreads, and becomes load-bearing.
- The cure is **active maintenance** — designers, implementers, and deployers evolve the spec and deployments together — not permanent tolerance.
- This is a deliberate, cited correction of a contested heuristic, **not** a claim that Postel was wrong in all contexts. Tolerance still has a place at the human-facing edge (see below).

