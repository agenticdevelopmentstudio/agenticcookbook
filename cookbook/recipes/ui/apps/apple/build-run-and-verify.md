
### Step 1: Generate

```bash
cd Tests/Projects/Apple && xcodegen generate
```

### Step 2: Build all targets

```bash
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestiOS -destination 'platform=iOS Simulator,name=iPhone 17 Pro' build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestMac build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestWatch -destination 'platform=watchOS Simulator,name=Apple Watch Series 11 (46mm)' build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestTV -destination 'platform=tvOS Simulator,name=Apple TV 4K (3rd generation)' build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestVision -destination 'platform=visionOS Simulator,name=Apple Vision Pro' build
```

### Step 3: Run and verify logs

Launch the macOS app (fastest for iteration) and stream logs to verify spec-defined messages:

```bash
# In one terminal: stream logs filtered to the test app subsystem
log stream --predicate 'subsystem == "com.litterbox.test.mac"' --level debug

# In another terminal: launch the app
open /Users/$USER/Library/Developer/Xcode/DerivedData/LitterboxTests-*/Build/Products/Debug/LitterboxTestMac.app
```

Verify these log messages appear:
- `ComponentCatalog: launched with N components` — on app launch
- `ComponentCatalog: selected "ComponentName"` — when selecting a catalog entry

For simulator targets, use `xcrun simctl` to launch and check logs:

```bash
# Boot simulator and launch app
xcrun simctl boot "iPhone 17 Pro"
xcrun simctl launch --console-pty booted com.litterbox.test.ios
```

### Step 4: Test accessibility options

After verifying basic functionality, test with accessibility options toggled:

```bash
# Test with RTL layout
xcrun simctl spawn booted defaults write com.litterbox.test.ios AppleTextDirection -bool YES
xcrun simctl spawn booted defaults write com.litterbox.test.ios NSForceRightToLeftWritingDirection -bool YES

# Test with increased text size (accessibility large)
xcrun simctl spawn booted defaults write com.litterbox.test.ios UIPreferredContentSizeCategoryName UICTContentSizeCategoryAccessibilityExtraLarge

# Reset after testing
xcrun simctl spawn booted defaults delete com.litterbox.test.ios AppleTextDirection
xcrun simctl spawn booted defaults delete com.litterbox.test.ios NSForceRightToLeftWritingDirection
xcrun simctl spawn booted defaults delete com.litterbox.test.ios UIPreferredContentSizeCategoryName
```

On macOS, toggle Reduce Motion and other options in System Settings > Accessibility to verify component responses.

