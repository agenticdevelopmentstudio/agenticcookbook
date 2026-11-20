
- Dynamic color derives the scheme from the user's wallpaper on Android 12+ (`Build.VERSION_CODES.S`). Treat it as a deliberate decision, not a default — opt in when brand identity allows the OS to drive palette.
- **SHOULD** guard the API level and fall back to your branded scheme:
  ```kotlin
  val scheme = when {
      dynamicColorEnabled && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ->
          if (dark) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
      dark -> DarkColors
      else -> LightColors
  }
  ```
- When brand color fidelity is a hard requirement, prefer a fixed branded scheme over dynamic color.

