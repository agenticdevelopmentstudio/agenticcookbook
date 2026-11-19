
# Debug mode

Apps MUST include a debug-only configuration panel (not in release builds):

- Feature flag overrides
- Analytics event log
- A/B test variant picker
- Environment info (version, build, OS, device)

Access methods:
- **Apple (iOS)**: Shake gesture, guarded by `#if DEBUG`
- **Apple (macOS)**: Debug menu item, guarded by `#if DEBUG`
- **Android**: Shake gesture, guarded by `BuildConfig.DEBUG`
- **Web**: `/debug` route, guarded by `NODE_ENV === 'development'`
- **Windows**: Debug-only settings page, guarded by `#if DEBUG`

---

# Debug Mode

Apps MUST include a debug-only configuration panel (not in release builds) with:

- Feature flag overrides
- Analytics event log
- A/B test variant picker
- Environment info (version, build, OS, device)

