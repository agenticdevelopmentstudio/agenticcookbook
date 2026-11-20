
Call this in `Activity.onCreate()` before `setContent` / `setContentView`:

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    enableEdgeToEdge() // androidx.activity, no-op shape on Android 15+ but normalizes older versions
    super.onCreate(savedInstanceState)
    // ...
}
```

`enableEdgeToEdge()` makes system bars transparent and adjusts icon contrast for the current theme. On 3-button navigation it applies a translucent scrim automatically.

