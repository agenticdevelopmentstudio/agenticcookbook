
Apple's PWA support is the binding constraint for cross-platform installable apps. As of iOS 18 / Safari 18 the following hold; re-verify per release:

- **Web Push** works **only** for apps the user has added to the Home Screen, and only on **iOS 16.4+**. The app **MUST** request notification permission from a user gesture *after* Home Screen install — not on first page load.
- There is **no `beforeinstallprompt`** event and **no automatic install prompt**. You **MUST** provide in-app guidance ("Share -> Add to Home Screen") rather than a programmatic install button.
- **Background Sync / Periodic Background Sync are unavailable.** Do not depend on them; queue writes in IndexedDB and flush on next foreground.
- **Storage is constrained and evictable**: expect a tight Cache API quota and automatic eviction of script-writable storage (Cache, IndexedDB) after roughly 7 days of non-use. Treat all client storage as a cache, never as the source of truth.
- Web Push availability has been subject to EU regulatory variation (iOS 17.4+); confirm behavior in target regions rather than assuming uniform support. (FORECAST: regional policy continues to evolve.)

