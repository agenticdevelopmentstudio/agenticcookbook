
Use `NSUserActivity` to advertise the current activity. Set `isEligibleForHandoff = true` and populate `userInfo` with state needed to restore context. Implement `application(_:continue:)` on the receiving device. Activities also appear in Spotlight and Siri Suggestions when `isEligibleForSearch` and `isEligibleForPrediction` are set. Support Universal Clipboard for cross-device copy/paste.

