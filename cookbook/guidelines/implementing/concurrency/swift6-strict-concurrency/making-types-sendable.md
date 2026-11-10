
- Prefer immutable value types (`struct`/`enum` with `let` `Sendable` stored properties) — they **SHOULD** be `Sendable` automatically; see [adc.principle.immutability-by-default](cookbook:a7ce3621-2fed-478f-8767-b186014c5923).
- A `final class` with only immutable `Sendable` state **MAY** declare `Sendable` conformance explicitly.
- A class whose safety the compiler cannot prove but that you guarantee (e.g. internal locking) **MAY** use `@unchecked Sendable` — but this **MUST** be justified in a comment, and the class **MUST NOT** expose mutable state without synchronization.
- Mutable shared state **SHOULD** be wrapped in an `actor`, not retrofitted with `@unchecked Sendable`.

