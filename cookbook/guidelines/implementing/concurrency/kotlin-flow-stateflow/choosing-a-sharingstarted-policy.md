
Choosing a SharingStarted policy, by when the upstream must run:

| Policy | When to use |
|--------|-------------|
| `WhileSubscribed(5_000)` | Default for UI state — stops upstream shortly after UI stops collecting. |
| `Eagerly` | Pipeline must run for the ViewModel's whole life regardless of subscribers (rare). |
| `Lazily` | Start on first subscriber, never stop. Use only when restart cost is unacceptable. |
