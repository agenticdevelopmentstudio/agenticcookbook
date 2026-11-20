
```kotlin
ViewCompat.setOnApplyWindowInsetsListener(view) { v, windowInsets ->
    val bars = windowInsets.getInsets(
        WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout()
    )
    v.updatePadding(bars.left, bars.top, bars.right, bars.bottom)
    WindowInsetsCompat.CONSUMED
}
```
