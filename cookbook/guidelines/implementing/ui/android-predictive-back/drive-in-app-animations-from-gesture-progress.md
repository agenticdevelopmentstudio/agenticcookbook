
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
