
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

