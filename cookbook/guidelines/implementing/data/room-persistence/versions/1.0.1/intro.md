
# Room persistence on Android

Room is Google's recommended SQLite persistence layer for Android. It is the concrete Android instantiation of the cookbook's transaction, normalization, and indexing guidance. Prefer coroutine-first DAO APIs: observable reads as `Flow`, one-shot writes as `suspend`, and multi-statement work wrapped in `@Transaction`.

