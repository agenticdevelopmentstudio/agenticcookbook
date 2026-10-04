
# Jetpack Compose performance and stability

Compose performance is dominated by recomposition cost. Make UI state stable, defer state reads, and let the compiler skip unchanged composables — then verify with measurement, never intuition. UI state SHOULD be stable and state reads SHOULD be deferred so the runtime can skip unnecessary recomposition.

