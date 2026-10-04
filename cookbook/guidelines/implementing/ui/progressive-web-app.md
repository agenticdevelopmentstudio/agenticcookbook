---
id: 3af6830b-71c9-4e50-929d-38dec20dae24
title: "Progressive Web App installability"
domain: agenticdevelopercookbook://guidelines/implementing/ui/progressive-web-app
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Ship a Web App Manifest plus a service worker with an explicit caching strategy, and account for iOS install/push/storage limits."
platforms:
  - web
  - typescript
tags:
  - web
  - pwa
  - offline
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/networking/offline-and-connectivity
  - agenticdevelopercookbook://guidelines/implementing/ui/modern-css
references:
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - ui-implementation
  - offline-support
---

# Progressive Web App installability

This guideline applies only when an **installable** web app is in scope. An installable app SHOULD ship a Web App Manifest and a service worker with an explicit caching strategy, and MUST account for iOS/Safari limitations. If installability is not a requirement, do not add a service worker for its own sake (YAGNI).

## Installability criteria

To be installable an app **MUST** be served over HTTPS (or `localhost` in development) and **MUST** link a valid Web App Manifest. As of 2025, Chrome and Edge no longer require a service worker merely to surface the install prompt, but you **MUST** still register one if offline behavior or push is in scope.

The manifest **MUST** include, at minimum:

- `name` (or `short_name`), `start_url`, and `display` set to `standalone`, `fullscreen`, or `minimal-ui`.
- `icons` with both a 192x192 and a 512x512 entry. Include a `maskable` icon for adaptive shaping.
- `id` to give the install a stable identity across `start_url` changes.

Validate against Lighthouse / DevTools Application panel before shipping; do not hand-assert installability.

## Service worker and caching

Register the service worker after the page loads and choose a caching strategy per request class — **do not** apply one strategy globally:

| Strategy | Use for |
|----------|---------|
| Cache-first | Versioned, immutable static assets (hashed JS/CSS, fonts) |
| Network-first | HTML navigations and freshness-critical API reads |
| Stale-while-revalidate | Avatars, non-critical data tolerant of brief staleness |

You **MUST** version the cache (e.g. cache name suffix) and delete stale caches in the `activate` event so old assets do not leak. Precache the app shell so navigations resolve offline. Prefer a maintained library (Workbox) over hand-rolled fetch handlers unless the surface is trivial — this is a deliberate trade for correctness on edge cases (range requests, opaque responses), not a mandate.

## iOS / Safari constraints (version-sensitive — verify against current Safari)

Apple's PWA support is the binding constraint for cross-platform installable apps. As of iOS 18 / Safari 18 the following hold; re-verify per release:

- **Web Push** works **only** for apps the user has added to the Home Screen, and only on **iOS 16.4+**. The app **MUST** request notification permission from a user gesture *after* Home Screen install — not on first page load.
- There is **no `beforeinstallprompt`** event and **no automatic install prompt**. You **MUST** provide in-app guidance ("Share -> Add to Home Screen") rather than a programmatic install button.
- **Background Sync / Periodic Background Sync are unavailable.** Do not depend on them; queue writes in IndexedDB and flush on next foreground.
- **Storage is constrained and evictable**: expect a tight Cache API quota and automatic eviction of script-writable storage (Cache, IndexedDB) after roughly 7 days of non-use. Treat all client storage as a cache, never as the source of truth.
- Web Push availability has been subject to EU regulatory variation (iOS 17.4+); confirm behavior in target regions rather than assuming uniform support. (FORECAST: regional policy continues to evolve.)

## Verification

- The manifest passes installability checks in Chrome/Edge and renders correctly when launched standalone.
- Offline reload of the app shell succeeds; cache version bumps purge old entries.
- On a physical iOS device: Home Screen install works, and (if used) push permission prompts and delivers only post-install.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
