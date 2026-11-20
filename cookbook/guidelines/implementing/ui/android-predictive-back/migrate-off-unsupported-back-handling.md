
```kotlin
val callback = object : OnBackPressedCallback(enabled = uiState.hasUnsavedChanges) {
    override fun handleOnBackPressed() { showDiscardConfirmation() }
}
requireActivity().onBackPressedDispatcher.addCallback(viewLifecycleOwner, callback)
```
