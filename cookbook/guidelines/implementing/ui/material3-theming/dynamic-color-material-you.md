
Dynamic color derives the scheme from the user's wallpaper on Android 12+ (`Build.VERSION_CODES.S`).

```kotlin
val scheme = when {
    dynamicColorEnabled && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ->
        if (dark) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
    dark -> DarkColors
    else -> LightColors
}
```
