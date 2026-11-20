
# Android predictive back

The predictive back gesture (introduced in Android 13 / API 33, enabled by default for opted-in apps from Android 15) shows a peek of where Back will go before the user commits. Apps MUST migrate off the unsupported `onBackPressed()` and `KEYCODE_BACK` interception to `OnBackPressedDispatcher` and SHOULD drive in-app transitions from the gesture's progress.

