
Apple's PWA support is the binding constraint for cross-platform installable apps.

- **Web Push** works **only** for apps the user has added to the Home Screen, and only on **iOS 16.4+**.
- There is **no `beforeinstallprompt`** event and **no automatic install prompt**.
- **Background Sync / Periodic Background Sync are unavailable.**
- **Storage is constrained and evictable**: expect a tight Cache API quota and automatic eviction of script-writable storage (Cache, IndexedDB) after roughly 7 days of non-use.
- (FORECAST: regional policy continues to evolve.)
