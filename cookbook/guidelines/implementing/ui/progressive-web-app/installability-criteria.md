
To be installable an app **MUST** be served over HTTPS (or `localhost` in development) and **MUST** link a valid Web App Manifest. As of 2025, Chrome and Edge no longer require a service worker merely to surface the install prompt, but you **MUST** still register one if offline behavior or push is in scope.

The manifest **MUST** include, at minimum:

- `name` (or `short_name`), `start_url`, and `display` set to `standalone`, `fullscreen`, or `minimal-ui`.
- `icons` with both a 192x192 and a 512x512 entry. Include a `maskable` icon for adaptive shaping.
- `id` to give the install a stable identity across `start_url` changes.

Validate against Lighthouse / DevTools Application panel before shipping; do not hand-assert installability.

