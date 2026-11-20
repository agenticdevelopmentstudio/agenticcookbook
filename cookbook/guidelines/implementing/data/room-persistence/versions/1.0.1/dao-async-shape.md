
- Observable reads **SHOULD** return `kotlinx.coroutines.flow.Flow<T>` (or `Flow<List<T>>`). Room re-emits automatically whenever an underlying table changes — no manual invalidation.
- One-shot reads and all writes (`@Insert`, `@Update`, `@Delete`, `@Query` DML) **SHOULD** be `suspend` functions so they run off the main thread on a Room-managed dispatcher.
- You **MUST NOT** call blocking (non-`suspend`, non-reactive) DAO functions on the main thread; Room throws `IllegalStateException` unless `allowMainThreadQueries()` is set, which you **SHOULD NOT** use outside tests.
- Reactive return types (`Flow`, and `Flowable`/`Observable` via the RxJava artifact) **MUST NOT** be marked `suspend`.

