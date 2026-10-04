
- Do not hold the `RoomDatabase` instance per-screen; build one application-scoped singleton via `Room.databaseBuilder(...)`.
- Do not expose `LiveData` for new code when the consumer is a coroutine/Compose layer; prefer `Flow`.
- Do not perform multi-step writes as separate suspend calls without a transaction — a crash between calls leaves a partial, inconsistent state.

