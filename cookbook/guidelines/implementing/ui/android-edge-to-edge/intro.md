
# Android edge-to-edge and window insets

When an app targets `targetSdk 35` (Android 15) or higher and runs on Android 15+, the system draws the app behind the status, caption, and navigation bars by default. The app MUST consume `WindowInsets` so that content, controls, and the keyboard are never obscured.

