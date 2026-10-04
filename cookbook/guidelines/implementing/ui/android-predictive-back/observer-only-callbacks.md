
- Android 16 (API 36) adds `PRIORITY_SYSTEM_NAVIGATION_OBSERVER` for callbacks that watch Back without consuming it (e.g. analytics). Use it ONLY for non-consuming side effects; it MUST NOT alter navigation.

