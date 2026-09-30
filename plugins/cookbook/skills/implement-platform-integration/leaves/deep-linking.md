<!-- leaf: implement-platform-integration/deep-linking · source: guidelines/implementing/platform-integration/deep-linking.md -->

**Rules** (cite as `implement-platform-integration/deep-linking#<slug>`):

- `feature-points-views-deep-linkable-using-platform` MUST — All significant feature points and views MUST be deep linkable using the platform's native URL/deep link mechanism:
- `spec-include-deep-linking-section` SHOULD — Each spec SHOULD include a Deep Linking section defining URL patterns.
- `feature-points-views-deep-linkable-using-platform-2` MUST — All significant feature points and views MUST be deep linkable using the platform's native URL/deep link mechanism. …
- `view-have-unique-shareable-url` MUST — Every view MUST have a unique, shareable URL. Use framework routing (React Router, Next.js routing, etc.).

# Deep linking

All significant feature points and views MUST be deep linkable using the platform's native URL/deep link mechanism:

- **Apple**: Universal Links + custom URL schemes. `onOpenURL` in SwiftUI, `NavigationPath` for state restoration.
- **Android**: App Links + intent filters. Navigation component deep link support.
- **Web**: URL routing. Every view should have a unique, shareable URL.
- **Windows**: Protocol activation via `<uap:Protocol>` declaration in manifest. `AppInstance.GetActivatedEventArgs()` for rich activation handling.

Each spec SHOULD include a **Deep Linking** section defining URL patterns.

---

# Deep Linking

All significant feature points and views MUST be deep linkable using the platform's native URL/deep link mechanism. Each spec SHOULD include a **Deep Linking** section defining URL patterns.

## TypeScript

Every view MUST have a unique, shareable URL. Use framework routing (React Router, Next.js routing, etc.).

## Windows

Declare protocol handlers in `Package.appxmanifest` and handle activation through the Windows App SDK lifecycle APIs.

- Declare: `<uap:Protocol Name="myapp"/>` in manifest
- Handle via `AppInstance.GetActivatedEventArgs()` in `App.OnLaunched`
- Parse URI to determine target page/state, navigate accordingly
- Use `AppInstance.FindOrRegisterForKey()` for single-instancing (recommended for deep links)
