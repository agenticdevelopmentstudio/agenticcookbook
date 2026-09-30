<!-- leaf: implement-ui/android-edge-to-edge · source: guidelines/implementing/ui/android-edge-to-edge.md -->

**Rules** (cite as `implement-ui/android-edge-to-edge#<slug>`):

- `bars-default-app-consume-windowinsets-so-content` MUST — When an app targets targetSdk 35 (Android 15) or higher and runs on Android 15+, the system draws the app behind the …
- `future-release-apps-not-depend` MUST — The temporary opt-out attribute android:windowOptOutEdgeToEdgeEnforcement is deprecated as of Android 16 (API 36) and …
- `apps-handle-window-insets-under` MUST — Apps MUST handle window insets under edge-to-edge; do not assume system bars leave a content-safe area.
- `apps-not-rely-android-windowoptoutedgetoedgeenforcement-long` MUST — Apps MUST NOT rely on android:windowOptOutEdgeToEdgeEnforcement as a long-term fix. Treat it only as a one-release …
- `must-not` MUST — return WindowInsetsCompat.CONSUMED from a parent if child views also need the same insets — consuming stops dispatch …
- `must-not-2` MUST — mix fitsSystemWindows="true" with manual inset listeners on the same view; pick one strategy per view.

# Android edge-to-edge and window insets

When an app targets `targetSdk 35` (Android 15) or higher and runs on Android 15+, the system draws the app behind the status, caption, and navigation bars by default. The app MUST consume `WindowInsets` so that content, controls, and the keyboard are never obscured.

## Why this matters

- Google Play has required `targetSdk 35` for app updates since 2024-08-31, so edge-to-edge is effectively unavoidable for maintained apps.
- Not handling insets is the single most common visual regression of this era: clipped toolbars, FABs under the gesture bar, and text behind the status bar.
- The temporary opt-out attribute `android:windowOptOutEdgeToEdgeEnforcement` is **deprecated as of Android 16 (API 36)** and will stop being honored in a future release. Apps **MUST NOT** depend on it.

## Core requirements

- Apps **MUST** handle window insets under edge-to-edge; do not assume system bars leave a content-safe area.
- Apps **MUST NOT** rely on `android:windowOptOutEdgeToEdgeEnforcement` as a long-term fix. Treat it only as a one-release emergency stopgap, if at all.
- For backward compatibility on Android 14 (API 34) and below, call `enableEdgeToEdge()` in `onCreate()` so behavior is consistent across versions.
- Prefer the `safeDrawing` inset type for general content; it composes `systemBars`, `displayCutout`, and `ime`.

## Enabling (consistent across versions)

Call this in `Activity.onCreate()` before `setContent` / `setContentView`:

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    enableEdgeToEdge() // androidx.activity, no-op shape on Android 15+ but normalizes older versions
    super.onCreate(savedInstanceState)
    // ...
}
```

`enableEdgeToEdge()` makes system bars transparent and adjusts icon contrast for the current theme. On 3-button navigation it applies a translucent scrim automatically.

## Jetpack Compose

- Wrap top-level UI in `Scaffold`; it applies `safeDrawing` insets and exposes the consumed `innerPadding`. **Apply that padding** — ignoring it reintroduces the bug.
- For manual control, use `Modifier.windowInsetsPadding(...)` with the right inset type:
  - `WindowInsets.safeDrawing` — default for scrollable/static content.
  - `WindowInsets.systemBars` — status + navigation + caption bars only.
  - `WindowInsets.ime` — keyboard; combine via `WindowInsets.safeDrawing` or `Modifier.imePadding()` for input fields.
- Let content scroll **edge to edge** but pad the interactive/last items, e.g. apply `contentPadding` to a `LazyColumn` instead of padding the whole list, so content draws under the bars while items stay reachable.

```kotlin
Scaffold { innerPadding ->
    LazyColumn(contentPadding = innerPadding) { /* items */ }
}
```

## Android Views

- Set a listener on the relevant view and consume insets:

```kotlin
ViewCompat.setOnApplyWindowInsetsListener(view) { v, windowInsets ->
    val bars = windowInsets.getInsets(
        WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout()
    )
    v.updatePadding(bars.left, bars.top, bars.right, bars.bottom)
    WindowInsetsCompat.CONSUMED
}
```

- Use `WindowInsetsCompat.Type.ime()` for keyboard-aware layouts; do not hardcode bottom padding.
- For Android 10 (API 29) and below, call `ViewGroupCompat.installCompatInsetsDispatch(rootView)` (androidx-core 1.16.0+) before consuming so sibling views still receive insets.
- Many Material Components (`BottomAppBar`, `BottomNavigationView`, `NavigationRailView`, `NavigationView`) consume insets automatically; `AppBarLayout` does not — add `android:fitsSystemWindows="true"` for its top inset.

## Pitfalls

- **MUST NOT** return `WindowInsetsCompat.CONSUMED` from a parent if child views also need the same insets — consuming stops dispatch downward.
- **MUST NOT** mix `fitsSystemWindows="true"` with manual inset listeners on the same view; pick one strategy per view.
- Test in both gesture and 3-button navigation, with a display cutout, and with the keyboard open.
