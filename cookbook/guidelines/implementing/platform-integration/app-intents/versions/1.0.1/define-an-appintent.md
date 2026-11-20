
A unit of app behavior is a type conforming to `AppIntent`. It needs a `title` and a `perform()` method; expose user-supplied inputs as `@Parameter` properties.

- An intent type **MUST** conform to `AppIntent` and implement `func perform() async throws -> some IntentResult`.
- Each intent **MUST** declare a static `title: LocalizedStringResource` and **SHOULD** set `description` so the action reads clearly in Shortcuts and Spotlight.
- User inputs **MUST** use `@Parameter` with a typed, `IntentParameter`-supported type (primitives, `AppEnum`, or an `AppEntity`).
- `perform()` **MUST** be idempotent-safe where the system may retry, and **MUST** throw a typed error rather than failing silently.
- Return value **SHOULD** use the most specific `IntentResult` (e.g. `.result(value:)`, `&ProvidesDialog`, `&ReturnsValue`) so results chain into other actions.

