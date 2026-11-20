
- Keep the Info.plist small. Prefer build-setting substitution (`$(PRODUCT_NAME)`, `$(MARKETING_VERSION)`) over literals, so a version or name is set once in the xcconfig.
- Every privacy usage-description key an API needs (camera, microphone, location and so on) MUST be present with text that tells the user why. A missing key crashes the app when it asks for access.
- Remove keys for features the app no longer has.

