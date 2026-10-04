
- `Activity.onBackPressed()` and `Dialog.onBackPressed()` are deprecated; intercepting `KeyEvent.KEYCODE_BACK` is no longer supported. Code MUST NOT rely on either — official docs warn of "unexpected behavior in a future release."
- Custom back logic MUST register an `OnBackPressedCallback` on the activity's `OnBackPressedDispatcher`, tied to a `LifecycleOwner` so it is removed automatically.
- Prefer the AndroidX `androidx.activity` APIs over the platform `OnBackInvokedCallback` — AndroidX is backward compatible across versions and is the recommended path. Use the platform `OnBackInvokedCallback` directly ONLY when you have no AndroidX dependency.
- The callback's `isEnabled` MUST be derived from observable UI state (a `StateFlow` or Compose `State`), not toggled imperatively, so the system knows whether the app or the system handles Back.
- Keep callbacks single-responsibility: one callback per back-consuming UI state, ordered by registration. The most recently added enabled callback wins.

```kotlin
val callback = object : OnBackPressedCallback(enabled = uiState.hasUnsavedChanges) {
    override fun handleOnBackPressed() { showDiscardConfirmation() }
}
requireActivity().onBackPressedDispatcher.addCallback(viewLifecycleOwner, callback)
```

