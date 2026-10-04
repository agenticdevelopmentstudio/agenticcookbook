
Use Service Workers for background sync (`BackgroundSyncManager`) and push notification handling. Use the Periodic Background Sync API for recurring data refresh (requires PWA install and user engagement). Use Web Workers for CPU-intensive tasks that shouldn't block the UI thread. Fall back to `requestIdleCallback` for low-priority deferred work.

