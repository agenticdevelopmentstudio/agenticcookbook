
MUST monitor network reachability and adjust sync behavior accordingly:

- When offline: queue writes locally, do not attempt sync
- On reconnection: trigger an immediate sync cycle
- When online: run periodic background sync (e.g., every 30 seconds while the app is active)
- When backgrounded: use platform-specific background sync APIs (WorkManager on Android, Background App Refresh on iOS, Service Worker Periodic Sync on web)

Never retry sync in a tight loop on reconnection. Apply exponential backoff starting from the first failure, even after regaining connectivity, in case the server is under load.

