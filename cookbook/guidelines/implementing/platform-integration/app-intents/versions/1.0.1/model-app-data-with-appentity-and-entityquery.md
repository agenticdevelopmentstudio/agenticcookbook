
To let intents accept or return your domain objects, make them discoverable.

- A domain type exposed to intents **MUST** conform to `AppEntity` (stable `id`, `displayRepresentation`, and a `defaultQuery`).
- Provide an `EntityQuery` (or `EntityStringQuery`/`EnumerableEntityQuery`) so the system can resolve entities by id, by search string, or by enumeration.
- Queries **SHOULD** be backed by your real data layer, not hardcoded — they are how Siri and Shortcuts fetch live values.

