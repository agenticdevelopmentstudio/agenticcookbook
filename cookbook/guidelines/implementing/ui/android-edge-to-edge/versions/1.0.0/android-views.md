
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

