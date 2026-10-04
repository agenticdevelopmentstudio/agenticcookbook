
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

