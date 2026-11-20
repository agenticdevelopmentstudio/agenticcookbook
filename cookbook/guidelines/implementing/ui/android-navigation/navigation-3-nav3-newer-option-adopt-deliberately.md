
`androidx.navigation3` reached 1.0 stable on 2025-11-19.

- Nav3 models the back stack as a plain observable `List` of keys (a `SnapshotStateList`) that you mutate directly (`backStack.add(key)` / `removeLastOrNull()`); `NavDisplay` renders the top entries. This makes the back stack first-class app state.
- Navigation Compose (Nav2) remains supported and is a correct default for most apps.
