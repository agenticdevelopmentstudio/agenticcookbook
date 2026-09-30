<!-- leaf: implement-feature-management/debug-mode · source: guidelines/implementing/feature-management/debug-mode.md -->

**Rules** (cite as `implement-feature-management/debug-mode#<slug>`):

- `apps-include-debug-only-configuration` MUST — Apps MUST include a debug-only configuration panel (not in release builds):
- `apps-include-debug-only-configuration-2` MUST — Apps MUST include a debug-only configuration panel (not in release builds) with:

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

## TypeScript

Access via `/debug` route or keyboard shortcut (`Ctrl+Shift+D`), guarded by `process.env.NODE_ENV === 'development'`.

## Windows

Dev-only settings page guarded by `#if DEBUG`:

- Feature flag overrides
- Analytics event log
- Environment info (app version, OS version, device)
- Access via navigation menu item visible only in debug builds
