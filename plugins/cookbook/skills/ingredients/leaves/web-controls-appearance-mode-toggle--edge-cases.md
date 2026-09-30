<!-- leaf: ingredients/web-controls-appearance-mode-toggle--edge-cases · source: ingredients/web/controls/appearance-mode-toggle.md -->

# Appearance Mode Toggle

**Rules** (cite as `ingredients/web-controls-appearance-mode-toggle--edge-cases#<slug>`):

- `settings-unavailable` MUST — If site settings cannot be read (e.g., storage quota exceeded, cookies disabled), the control MUST default to auto mode …
- `system-appearance-undefined` MUST — If prefers-color-scheme is not supported by the browser, auto mode MUST default to light.
- `rapid-clicking` MUST — Rapid toggling MUST NOT cause visual glitches or inconsistent state. Each click produces exactly one mode transition.
- `ssr-hydration-mismatch` MUST — If the page is server-rendered, the inline script in <head> handles the initial class. The client-side framework MUST …
- `legacy-storage-migration` SHOULD — If a previous implementation stored the theme under a different key (e.g., theme instead of theme-mode), the …

## Edge Cases

- **Settings unavailable**: If site settings cannot be read (e.g., storage quota exceeded, cookies disabled), the control MUST default to auto mode and degrade gracefully — no errors shown to the user. All settings access MUST be wrapped in try/catch.
- **System appearance undefined**: If `prefers-color-scheme` is not supported by the browser, auto mode MUST default to light.
- **Rapid clicking**: Rapid toggling MUST NOT cause visual glitches or inconsistent state. Each click produces exactly one mode transition.
- **SSR / hydration mismatch**: If the page is server-rendered, the inline script in `<head>` handles the initial class. The client-side framework MUST read the same stored value on hydration to avoid a mismatch.
- **Stale matchMedia queries**: Do NOT call `matchMedia().matches` on demand (e.g., in a click handler or effect). Some browsers/frameworks return stale values from on-demand queries. The always-on listener pattern avoids this entirely.
- **Legacy storage migration**: If a previous implementation stored the theme under a different key (e.g., `theme` instead of `theme-mode`), the initialization logic SHOULD detect and migrate it, then remove the old key.
