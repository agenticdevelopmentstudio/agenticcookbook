
- Entitlements are a declaration of what the app is allowed to do. Add one only for a capability the app uses, and review every added key as a security change.
- Keep one `.entitlements` file per target and configuration need (for example a sandboxed macOS app and its helper), referenced through the `CODE_SIGN_ENTITLEMENTS` setting.
- Never copy an entitlements file from another app wholesale. A leftover key grants capability nobody remembers.

