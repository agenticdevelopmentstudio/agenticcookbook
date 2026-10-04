
- Use the **same-document View Transitions API** (`document.startViewTransition`) for animated state/route changes in SPAs. It is Newly available, so it **MUST** degrade gracefully: when unsupported, the DOM update still applies, just without animation. Feature-detect with `if (document.startViewTransition) { ... } else { /* apply update directly */ }`.
- **Cross-document (MPA) View Transitions are a FORECAST for full interoperability** — they ship in Chromium and Safari but not Firefox as of this writing, so they are NOT Baseline. Use them as pure progressive enhancement only; never make navigation depend on them.
- Respect `prefers-reduced-motion: reduce` and disable or shorten transitions accordingly.

