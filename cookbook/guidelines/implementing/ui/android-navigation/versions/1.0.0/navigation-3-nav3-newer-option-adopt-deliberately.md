
`androidx.navigation3` reached 1.0 stable on 2025-11-19. Pin a current `1.x` release before relying on it; APIs and supporting libraries (e.g. `material3-adaptive-navigation3`) are still maturing, so treat specific surface details as evolving (FORECAST) and re-check the release notes.

- Nav3 models the back stack as a plain observable `List` of keys (a `SnapshotStateList`) that you mutate directly (`backStack.add(key)` / `removeLastOrNull()`); `NavDisplay` renders the top entries. This makes the back stack first-class app state.
- Choose Nav3 as a **deliberate decision** when you need full control over the back stack, multi-pane/adaptive layouts, or custom transitions — not as a blanket mandate. Navigation Compose (Nav2) remains supported and is a correct default for most apps.
- Do **NOT** mix Nav2 `NavHost` and Nav3 `NavDisplay` for the same flow; pick one model per navigation graph and migrate a flow at a time.

