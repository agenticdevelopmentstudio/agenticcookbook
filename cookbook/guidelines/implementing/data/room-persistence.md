---
id: a4f57a3c-f909-42aa-a85f-1ac76ac3ab24
title: "Room persistence on Android"
domain: agenticdevelopercookbook://guidelines/implementing/data/room-persistence
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Use Room with KSP, Flow-returning observable reads, suspend writes, and @Transaction-wrapped multi-step operations on Android."
platforms:
  - kotlin
tags:
  - android
  - database
  - persistence
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/data/transaction-isolation
references:
  - https://developer.android.com/training/data-storage/room
  - https://android-developers.googleblog.com/2026/03/room-30-modernizing-room.html
  - https://developer.android.com/kotlin/multiplatform/room
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - database-operations
  - data-modeling
---

# Room persistence on Android

Room is Google's recommended SQLite persistence layer for Android. It is the concrete Android instantiation of the cookbook's transaction, normalization, and indexing guidance. Prefer coroutine-first DAO APIs: observable reads as `Flow`, one-shot writes as `suspend`, and multi-statement work wrapped in `@Transaction`.

## Version landscape (as of 2026-06)

- **Room 2.8.4** is the current stable line. Stable Kotlin Multiplatform (KMP) support arrived in **2.7.0** (Android + iOS + JVM desktop). State KMP support as "2.7.0+" — do not back-port the claim to older versions.
- **Room 3.0.0-alpha01** (released 2026-03-11) is a major, breaking, KMP-first line that adds JS/WASM targets, generates only Kotlin, drops KAPT (KSP-only), and disallows blocking DAO functions. **Room 3.0 is ALPHA — treat its API and the `androidx.room3:room3-*` artifact rename as a FORECAST, not a shipped default. Do not migrate production code to it yet.**
- Pin the Room version explicitly in the version catalog; do not float to `+`.

## Compiler

- You **MUST** use **KSP** (`androidx.room:room-compiler` via the KSP plugin) for the annotation processor. KAPT is legacy and roughly 2x slower; Room 3.0 removes KAPT support entirely.
- You **SHOULD** enable schema export (`room.schemaLocation`) and commit the generated JSON schema so migrations can be diffed and tested.

## DAO async shape

- Observable reads **SHOULD** return `kotlinx.coroutines.flow.Flow<T>` (or `Flow<List<T>>`). Room re-emits automatically whenever an underlying table changes — no manual invalidation.
- One-shot reads and all writes (`@Insert`, `@Update`, `@Delete`, `@Query` DML) **SHOULD** be `suspend` functions so they run off the main thread on a Room-managed dispatcher.
- You **MUST NOT** call blocking (non-`suspend`, non-reactive) DAO functions on the main thread; Room throws `IllegalStateException` unless `allowMainThreadQueries()` is set, which you **SHOULD NOT** use outside tests.
- Reactive return types (`Flow`, and `Flowable`/`Observable` via the RxJava artifact) **MUST NOT** be marked `suspend`.

## Transactions

- Any operation that issues **more than one statement and must be atomic** (read-modify-write, multi-table insert, batch upsert with dependent rows) **MUST** be wrapped in a single transaction — annotate the DAO method with `@Transaction`, or call `db.withTransaction { ... }` from suspend code.
- `@Transaction` is also **REQUIRED** on `@Query` methods that return a `@Relation`-bearing POJO, so the parent and child reads see a consistent snapshot.
- Keep transactions short; do no network or long CPU work inside `withTransaction`. See `agenticdevelopercookbook://guidelines/implementing/data/transaction-isolation` for isolation semantics.

## Schema and indexing

- Define one `@Entity` per normalized table. Declare relationships with `@ForeignKey` and load them via `@Relation`, not by denormalizing.
- Every `@ForeignKey` column **MUST** be indexed (`@Entity(indices = [Index("owner_id")])`). Room emits a build warning for unindexed foreign keys; treat it as an error to fix.
- Add an `@Index(unique = true)` for natural-key uniqueness instead of relying on app-side checks.

## Migrations

- On every schema change you **MUST** bump the database `version` and supply a `Migration` (or an `@DeleteColumn`/`@RenameColumn`-driven auto-migration spec). You **MUST NOT** ship `fallbackToDestructiveMigration()` in a release build — it silently drops user data.
- You **SHOULD** add a `MigrationTestHelper`-based instrumented test that opens the exported schema at version N and migrates to N+1, asserting data survives.

## MUST NOT

- Do not hold the `RoomDatabase` instance per-screen; build one application-scoped singleton via `Room.databaseBuilder(...)`.
- Do not expose `LiveData` for new code when the consumer is a coroutine/Compose layer; prefer `Flow`.
- Do not perform multi-step writes as separate suspend calls without a transaction — a crash between calls leaves a partial, inconsistent state.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
