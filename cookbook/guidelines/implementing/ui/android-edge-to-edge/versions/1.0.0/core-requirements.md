
- Apps **MUST** handle window insets under edge-to-edge; do not assume system bars leave a content-safe area.
- Apps **MUST NOT** rely on `android:windowOptOutEdgeToEdgeEnforcement` as a long-term fix. Treat it only as a one-release emergency stopgap, if at all.
- For backward compatibility on Android 14 (API 34) and below, call `enableEdgeToEdge()` in `onCreate()` so behavior is consistent across versions.
- Prefer the `safeDrawing` inset type for general content; it composes `systemBars`, `displayCutout`, and `ime`.

