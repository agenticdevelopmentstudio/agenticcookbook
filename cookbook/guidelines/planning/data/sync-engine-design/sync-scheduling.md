
SHOULD implement at least two scheduling modes:

**Periodic:** Run the sync cycle every N seconds (e.g., 30s) while the app is active. Simple, predictable, battery-friendly. Use as the safety net to catch any missed event-driven syncs.

**Event-driven:** Trigger a sync immediately after a user mutation (or after a batch of mutations within a short debounce window). More responsive but can burst traffic — always throttle with a minimum interval between syncs (e.g., no more than once per 2 seconds).

**Background daemon:** Use platform-specific APIs to sync when the app is closed:
- iOS/macOS: Background App Refresh or XPC service
- Android: WorkManager with network constraints
- Web: Service Worker Periodic Sync API

**Connectivity-aware:** Pause sync when offline. Resume immediately on reconnection, then fall back to the periodic schedule.

