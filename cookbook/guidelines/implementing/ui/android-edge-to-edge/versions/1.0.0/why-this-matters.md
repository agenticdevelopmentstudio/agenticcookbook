
- Google Play has required `targetSdk 35` for app updates since 2024-08-31, so edge-to-edge is effectively unavoidable for maintained apps.
- Not handling insets is the single most common visual regression of this era: clipped toolbars, FABs under the gesture bar, and text behind the status bar.
- The temporary opt-out attribute `android:windowOptOutEdgeToEdgeEnforcement` is **deprecated as of Android 16 (API 36)** and will stop being honored in a future release. Apps **MUST NOT** depend on it.

