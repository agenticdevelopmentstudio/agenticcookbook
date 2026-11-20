
- For custom transitions (sheets, drawers, multi-step flows), guidance SHOULD animate with the gesture rather than snapping at release.
- Compose: use `PredictiveBackHandler`, collecting the `Flow<BackEventCompat>` and reading `progress` (0f..1f). Commit the navigation when the flow completes; reset UI on `CancellationException` (gesture cancelled).
- Views: extend `OnBackPressedCallback` and implement `handleOnBackStarted` / `handleOnBackProgressed` / `handleOnBackCancelled` (API 34+) to animate, with `handleOnBackPressed` committing the result.

```kotlin
PredictiveBackHandler(enabled = sheetIsOpen) { progress: Flow<BackEventCompat> ->
    try {
        progress.collect { event -> sheetOffset = event.progress }
        closeSheet() // committed
    } catch (e: CancellationException) {
        resetSheetOffset() // cancelled
    }
}
```

