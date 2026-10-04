
- The `android:enableOnBackInvokedCallback` flag controls predictive back during migration. It is a per-`<application>` flag and MAY be overridden per `<activity>` for gradual rollout of multi-activity apps.
- Setting it `false` disables system predictive animations and ignores the platform `OnBackInvokedCallback`; AndroidX `OnBackPressedCallback` still works. Set it `true` (or omit it where the default is on) to receive system animations.
- FORECAST: default-on behavior and removal of any opt-out are tied to evolving target-SDK rules across Android 15/16 (API 35/36). Pin the exact behavior to your `targetSdk` and re-check the linked doc before shipping — do not assume a fixed default across versions.

