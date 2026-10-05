---
id: 73b767b7-e870-45a9-b7ac-be09164db033
title: Android Build & Emulator Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/android/android-build-and-emulator
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Android Build & Emulator Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Android Build & Emulator Tools

**Date:** 2026-03-29
**Context:** Build system and device management tools for Android development with Claude Code. Focused on tools that work in a CLI/headless context and can be invoked from Claude Code via shell-out, MCP servers, or hooks. Covers the full plan/implement/verify loop.

---

## Gradle CLI (implement/verify)

### Core Build Commands

- **Link:** https://developer.android.com/build/building-cmdline
- **What it does:** The Android Gradle Plugin (AGP) is the standard build system for Android. All builds are invoked via the Gradle wrapper (`./gradlew` on macOS/Linux, `gradlew` on Windows). Commands follow camelCase variant naming: `assemble{Flavor}{BuildType}`.
- **Loop phase:** implement, verify
- **Install:** Bundled with every Android project via the Gradle wrapper. No separate install needed.
- **Claude Code integration:** CLI shell-out. All commands are non-interactive and produce structured output.

**Build commands:**

```bash
./gradlew assembleDebug                # Build debug APK
./gradlew assembleRelease              # Build release APK (requires signing config)
./gradlew installDebug                 # Build + install debug APK on connected device/emulator
./gradlew installRelease               # Build + install release APK
./gradlew bundleDebug                  # Build debug App Bundle (.aab)
./gradlew bundleRelease                # Build release App Bundle
./gradlew clean                        # Delete build directory
./gradlew build                        # Assemble + test all variants
```

**Testing commands:**

```bash
./gradlew test                         # Run all unit tests (all variants)
./gradlew testDebugUnitTest            # Run unit tests for debug variant only
./gradlew testReleaseUnitTest          # Run unit tests for release variant only
./gradlew connectedCheck               # Run instrumented tests on connected device/emulator
./gradlew connectedDebugAndroidTest    # Instrumented tests for debug variant
```

**Lint and analysis:**

```bash
./gradlew lint                         # Run lint on all variants
./gradlew lintDebug                    # Run lint on debug variant
./gradlew lintRelease                  # Run lint on release variant
```

**Dependency inspection:**

```bash
./gradlew :app:dependencies                                              # Full dependency tree
./gradlew :app:dependencies --configuration debugCompileClasspath        # Specific configuration
./gradlew :app:dependencyInsight --dependency androidx.core:core-ktx \
  --configuration debugRuntimeClasspath                                  # Single dependency insight
./gradlew tasks                                                          # List all available tasks
```

**Product flavors and build variants:**

```bash
# Pattern: ./gradlew assemble{Flavor}{BuildType}
./gradlew assembleFreeDebug            # Free flavor, debug build type
./gradlew assembleProRelease           # Pro flavor, release build type
./gradlew installFreeDebug             # Build + install free debug
./gradlew testProDebugUnitTest         # Unit tests for pro debug
./gradlew connectedFreeDebugAndroidTest  # Instrumented tests for free debug
```

**Performance flags:**

```bash
./gradlew assembleDebug --parallel              # Parallel project execution
./gradlew assembleDebug --build-cache           # Reuse outputs from previous builds
./gradlew assembleDebug --configuration-cache   # Reuse build configuration
./gradlew assembleDebug --stacktrace            # Print full stack trace on error
./gradlew assembleDebug --info                  # Info-level logging
./gradlew assembleDebug --debug                 # Debug-level logging (very verbose)
./gradlew assembleDebug --scan                  # Generate Gradle build scan
```

**gradle.properties (persistent performance settings):**

```properties
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=true
org.gradle.jvmargs=-Xmx4g -XX:+HeapDumpOnOutOfMemoryError
```

- **Notes:** AGP 8.x (current stable) requires Java 17+. The Gradle wrapper pins the Gradle version per-project, so Claude does not need to manage Gradle versions. Build output lands in `app/build/outputs/apk/` (APKs) and `app/build/outputs/bundle/` (AABs). Test results land in `app/build/test-results/` (unit) and `app/build/outputs/androidTest-results/` (instrumented).

---

## ADB (Android Debug Bridge) (implement/verify)

- **Link:** https://developer.android.com/tools/adb
- **What it does:** Versatile CLI tool for communicating with Android devices and emulators. Handles app install/uninstall, file transfer, screenshots, screen recording, logging, shell access, and device control. Part of the Android SDK Platform Tools.
- **Loop phase:** implement, verify
- **Install:** `sdkmanager "platform-tools"` or download from https://developer.android.com/tools/releases/platform-tools. Also bundled with Android Studio.
- **Claude Code integration:** CLI shell-out. All commands are non-interactive. Also available via MCP servers (see Claude Code Integration section).

**Device management:**

```bash
adb devices -l                         # List connected devices with details
adb -s <serial> <command>              # Target specific device by serial
adb -e <command>                       # Target emulator only
adb -d <command>                       # Target physical device only
adb connect <ip>:<port>                # Connect wirelessly (Wi-Fi debugging)
adb pair <ip>:<port>                   # Pair for wireless debugging (Android 11+)
adb disconnect <ip>:<port>             # Disconnect wireless device
adb start-server                       # Start ADB server
adb kill-server                        # Kill ADB server
```

**App installation:**

```bash
adb install path/to/app.apk           # Install APK
adb install -r path/to/app.apk        # Replace existing app
adb install -t path/to/app.apk        # Allow test APKs
adb install-multiple a.apk b.apk      # Install split APKs
adb uninstall com.example.app          # Uninstall by package name
adb uninstall -k com.example.app       # Uninstall but keep data/cache
```

**Screenshot and screen recording:**

```bash
adb shell screencap /sdcard/screen.png              # Capture screenshot on device
adb exec-out screencap -p > screen.png              # Capture directly to local machine
adb pull /sdcard/screen.png ./screen.png            # Pull screenshot from device

adb shell screenrecord /sdcard/demo.mp4             # Record screen (default 3 min)
adb shell screenrecord --time-limit 30 /sdcard/demo.mp4  # Record for 30 seconds
adb shell screenrecord --size 1280x720 /sdcard/demo.mp4  # Record at specific resolution
adb shell screenrecord --bit-rate 6000000 /sdcard/demo.mp4  # Set bitrate
```

**Logcat (system logging):**

```bash
adb logcat                             # Stream all logs
adb logcat -c                          # Clear log buffer
adb logcat "*:E"                       # Errors only
adb logcat -s MyTag                    # Filter by tag
adb logcat MyTag:D "*:S"              # Debug+ for MyTag, silence others
adb logcat -v time                     # Include timestamps
adb logcat -v threadtime               # Thread ID + timestamp format
adb logcat -d                          # Dump log and exit (non-blocking)
adb logcat -g                          # Print buffer size
```

Priority levels: V(verbose), D(debug), I(info), W(warning), E(error), F(fatal), S(silent).

**Shell commands:**

```bash
adb shell                              # Interactive shell
adb shell am start -n com.example/.MainActivity   # Start activity
adb shell am start -W com.example/.MainActivity   # Start and wait for launch
adb shell am force-stop com.example.app            # Force stop app
adb shell am broadcast -a android.intent.action.BOOT_COMPLETED  # Send broadcast
adb shell pm list packages             # List all packages
adb shell pm list packages -3          # Third-party packages only
adb shell pm clear com.example.app     # Clear app data
adb shell pm grant com.example.app android.permission.CAMERA    # Grant permission
adb shell pm revoke com.example.app android.permission.CAMERA   # Revoke permission
adb shell input tap 500 500            # Simulate tap at coordinates
adb shell input text "hello"           # Type text
adb shell input keyevent 3             # Press HOME key
adb shell dumpsys battery              # Battery info
adb shell dumpsys meminfo              # Memory info
adb shell settings get system screen_brightness    # Read setting
```

**File transfer and port forwarding:**

```bash
adb push local_file /sdcard/remote     # Copy file to device
adb pull /sdcard/remote local_file     # Copy file from device
adb forward tcp:8080 tcp:8080          # Forward host port to device port
adb reverse tcp:8080 tcp:8080          # Forward device port to host port
```

**Device control:**

```bash
adb reboot                             # Reboot device
adb reboot bootloader                  # Reboot to bootloader
adb bugreport                          # Generate bug report zip
```

- **Notes:** ADB 36.0.0+ supports burst mode (`export ADB_BURST_MODE=1`) for faster file transfers. Set `$ANDROID_SERIAL` to target a specific device by default. Claude Code can use `adb exec-out screencap -p > screen.png` for instant local screenshots without a two-step capture-then-pull workflow.

---

## Emulator Management (implement/verify)

### Android Emulator

- **Link:** https://developer.android.com/studio/run/emulator-commandline
- **What it does:** The Android Emulator simulates Android devices on your computer. It supports snapshots, GPU acceleration, network simulation, and headless mode for CI.
- **Loop phase:** implement, verify
- **Install:** `sdkmanager "emulator"` plus a system image (see sdkmanager below).
- **Claude Code integration:** CLI shell-out. Headless mode (`-no-window`) is ideal for Claude Code sessions. MCP servers also available.

**Core commands:**

```bash
emulator -list-avds                    # List available AVDs
emulator -avd Pixel_8_API_34           # Start emulator with named AVD
emulator @Pixel_8_API_34              # Shorthand syntax
```

**Headless / CI mode:**

```bash
emulator @Pixel_8_API_34 -no-window -no-audio -no-boot-anim   # Headless start
emulator @Pixel_8_API_34 -no-window -gpu swiftshader_indirect  # Software GPU for CI
emulator @Pixel_8_API_34 -no-window -gpu host                 # Host GPU acceleration
```

**Snapshot management:**

```bash
emulator @Pixel_8_API_34 -snapshot my_snapshot      # Load named snapshot
emulator @Pixel_8_API_34 -snapshot-list             # List available snapshots
emulator @Pixel_8_API_34 -no-snapshot-load          # Cold boot (ignore saved state)
emulator @Pixel_8_API_34 -no-snapshot-save          # Don't save state on exit
emulator @Pixel_8_API_34 -no-snapshot               # Disable snapshots entirely
emulator @Pixel_8_API_34 -wipe-data                 # Reset to factory defaults
```

**Resource configuration:**

```bash
emulator @Pixel_8_API_34 -memory 2048               # Set RAM (MB)
emulator @Pixel_8_API_34 -partition-size 1024        # System partition size (MB)
emulator @Pixel_8_API_34 -port 5556                  # Console/ADB port
emulator @Pixel_8_API_34 -ports 5556,5559            # Explicit console + ADB ports
```

**Network simulation:**

```bash
emulator @Pixel_8_API_34 -netspeed edge              # Simulate EDGE network
emulator @Pixel_8_API_34 -netdelay gsm               # Simulate GSM latency
emulator @Pixel_8_API_34 -netfast                     # Full speed, no delay
emulator @Pixel_8_API_34 -dns-server 8.8.8.8         # Custom DNS
emulator @Pixel_8_API_34 -http-proxy myproxy:8080    # HTTP proxy
emulator @Pixel_8_API_34 -tcpdump /path/dump.cap     # Capture network traffic
```

**Hardware acceleration:**

```bash
emulator -accel-check                                # Check hypervisor status
emulator @Pixel_8_API_34 -accel auto                 # Auto-detect acceleration
emulator @Pixel_8_API_34 -accel on                   # Force hardware acceleration
emulator @Pixel_8_API_34 -accel off                  # Disable acceleration
```

GPU modes: `auto`, `host` (use host GPU), `swiftshader_indirect` (software rendering, best for CI), `angle_indirect` (ANGLE backend), `guest` (guest-side rendering).

**Debugging:**

```bash
emulator @Pixel_8_API_34 -verbose                    # Show init messages
emulator @Pixel_8_API_34 -show-kernel                # Show kernel messages
emulator @Pixel_8_API_34 -logcat '*:e'               # Logcat error filter
emulator -help                                        # List all options
emulator -help-all                                    # Detailed help
emulator -version                                     # Show version
```

### avdmanager

- **Link:** https://developer.android.com/tools/avdmanager
- **What it does:** CLI tool for creating, deleting, and listing Android Virtual Devices (AVDs). Part of the SDK Command-Line Tools.
- **Loop phase:** implement (setup)
- **Install:** `sdkmanager "cmdline-tools;latest"`

```bash
avdmanager list avd                                  # List existing AVDs
avdmanager list device                               # List available device definitions
avdmanager list target                               # List available system images

avdmanager create avd \
  -n Pixel_8_API_34 \
  -k "system-images;android-34;google_apis;x86_64" \
  -d pixel_8                                          # Create AVD

avdmanager delete avd -n Pixel_8_API_34              # Delete AVD
avdmanager move avd -n old_name -r new_name          # Rename AVD
```

### sdkmanager

- **Link:** https://developer.android.com/tools/sdkmanager
- **What it does:** CLI tool for downloading, updating, and managing Android SDK packages. Essential for CI environments without Android Studio.
- **Loop phase:** implement (setup)
- **Install:** Part of the SDK Command-Line Tools. Download from https://developer.android.com/studio#command-tools.

```bash
sdkmanager --list                                    # List all available and installed packages
sdkmanager --list --include_obsolete                  # Include obsolete packages

# Install packages
sdkmanager "platform-tools"                          # ADB, fastboot, etc.
sdkmanager "emulator"                                # Android Emulator
sdkmanager "platforms;android-34"                     # Android 14 SDK platform
sdkmanager "build-tools;34.0.0"                      # Build tools
sdkmanager "system-images;android-34;google_apis;x86_64"   # System image for emulator
sdkmanager "cmdline-tools;latest"                    # Command-line tools (avdmanager, etc.)
sdkmanager "ndk;26.1.10909125"                       # NDK (for native code)

# Update and licenses
sdkmanager --update                                  # Update all installed packages
sdkmanager --licenses                                # Accept all SDK licenses (interactive)
yes | sdkmanager --licenses                          # Auto-accept licenses (CI)
```

- **Notes:** For CI, a typical bootstrap sequence is: install sdkmanager, run `yes | sdkmanager --licenses`, install platform-tools + emulator + system-image + build-tools, create AVD with avdmanager, start emulator in headless mode. The environment variable `ANDROID_HOME` (or `ANDROID_SDK_ROOT`) must point to the SDK root.

---

## Maestro UI Testing (verify)

- **Link:** https://maestro.dev / https://docs.maestro.dev
- **What it does:** Open-source mobile UI automation framework that uses declarative YAML flows. No compile step, no Appium, no Selenium. Built-in flakiness tolerance with automatic waiting. Supports Android, iOS, and web.
- **Loop phase:** verify
- **Install:** `curl -Ls "https://get.maestro.dev" | bash` (macOS/Linux). Requires Java 17+.
- **Claude Code integration:** CLI shell-out. YAML flows are trivially generated by Claude. Continuous mode (`-c`) re-runs on file save. Screenshot command captures visual state. Also available as MCP tool via `maestro mcp`.

**CLI commands:**

```bash
maestro test flow.yaml                 # Run a single flow
maestro test flows/                    # Run all flows in a directory (suite)
maestro test -c flow.yaml              # Continuous mode — re-runs on file save
maestro test --format junit flow.yaml  # JUnit XML output for CI
maestro record flow.yaml               # Record execution as MP4 video
maestro studio                         # Launch visual test builder in browser
maestro hierarchy                      # Dump current UI hierarchy
maestro download-samples               # Download sample flows and apps
maestro bugreport                      # Generate bug report
maestro start-device                   # Launch emulator/simulator
maestro cloud flows/ --app app.apk     # Run flows on Maestro Cloud
```

**YAML flow commands (core set):**

```yaml
appId: com.example.app
---
- launchApp                            # Launch the app (uses appId)
- launchApp:
    appId: com.example.app
    clearState: true                   # Clear app data before launch
- tapOn: "Login"                       # Tap element by text
- tapOn:
    id: "btn_submit"                   # Tap by accessibility ID
- doubleTapOn: "Item"                  # Double tap
- longPressOn: "Delete"               # Long press
- inputText: "user@example.com"       # Type into focused field
- eraseText: 10                        # Erase 10 characters
- assertVisible: "Welcome"            # Assert element is visible
- assertNotVisible: "Error"           # Assert element is not visible
- scroll                               # Scroll down
- scrollUntilVisible:
    element: "Settings"
- swipe:
    direction: LEFT
    duration: 500
- back                                 # Press back button
- hideKeyboard                         # Dismiss keyboard
- openLink: "https://example.com"     # Open URL
- copyTextFrom: "Balance"             # Copy text from element
- pasteText                            # Paste copied text
- screenshot: "login_screen"          # Capture screenshot
- startRecording: "test_flow"         # Start screen recording
- stopRecording                        # Stop recording
- waitForAnimationToEnd               # Wait for animations
- repeat:
    times: 3
    commands:
      - tapOn: "Next"
- runFlow: shared/login.yaml           # Run a sub-flow
- evalScript: ${output.myVar = 'hello'}  # JavaScript expression
```

- **Notes:** Maestro flows are deterministic YAML files that Claude can generate and iterate on without compilation. The `maestro studio` command provides a visual element inspector that helps write selectors. Maestro Cloud runs flows in hosted infrastructure, eliminating the need for local emulators in CI. Recent versions include an `mcp` subcommand for direct MCP server integration.

---

## UI Automator (verify)

- **Link:** https://developer.android.com/training/testing/other-components/ui-automator
- **What it does:** Google's framework for cross-app functional UI testing on Android. Unlike Espresso (which tests within a single app), UI Automator can interact with any app on the device, including system apps, settings, notifications, and permission dialogs. Works through the Android accessibility framework.
- **Loop phase:** verify
- **Install:** Add dependency to `build.gradle.kts`: `androidTestImplementation("androidx.test.uiautomator:uiautomator:2.3.0")`
- **Claude Code integration:** Tests are Kotlin/Java code compiled and run via `./gradlew connectedCheck`. Claude writes the test code, Gradle runs it.

**Core APIs:**

- `UiDevice` — represents the device; provides `pressHome()`, `pressBack()`, `openNotification()`, `takeScreenshot()`, `click()`, `swipe()`, `waitForIdle()`
- `UiSelector` — finds elements by text, description, resourceId, className, instance
- `UiObject` / `UiObject2` — represents a found element; provides `click()`, `setText()`, `getText()`, `exists()`, `waitForExists()`
- `UiCollection` — select groups of elements
- `UiScrollable` — scroll containers to find elements

**Example test (Kotlin):**

```kotlin
@RunWith(AndroidJUnit4::class)
class SettingsTest {
    private lateinit var device: UiDevice

    @Before
    fun setup() {
        device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())
        device.pressHome()
    }

    @Test
    fun openSettings() {
        // Open Settings via intent
        val context = ApplicationProvider.getApplicationContext<Context>()
        val intent = context.packageManager.getLaunchIntentForPackage("com.android.settings")
        context.startActivity(intent)
        device.wait(Until.hasObject(By.pkg("com.android.settings")), 5000)

        // Find and tap "Battery"
        val battery = device.findObject(UiSelector().text("Battery"))
        battery.click()
        assertTrue(device.findObject(UiSelector().text("Battery usage")).exists())
    }
}
```

**Run via CLI:**

```bash
./gradlew connectedDebugAndroidTest                           # All instrumented tests
./gradlew connectedDebugAndroidTest \
  -Pandroid.testInstrumentationRunnerArguments.class=\
  com.example.SettingsTest                                     # Single test class
```

- **Notes:** UI Automator is slower than Espresso because it works through the accessibility framework. Use Espresso for in-app testing and UI Automator for cross-app or system-level testing. The `uiautomatorviewer` tool (in SDK tools) helps inspect UI hierarchies for writing selectors. Requires API level 18+.

---

## Firebase Test Lab (verify)

- **Link:** https://firebase.google.com/docs/test-lab
- **What it does:** Google's cloud-based testing infrastructure. Runs tests on real devices and virtual devices hosted by Google. Supports Robo tests (automated exploration), instrumented tests (Espresso/UI Automator), and Game Loop tests. Results include logs, screenshots, and video.
- **Loop phase:** verify
- **Install:** `gcloud` CLI from https://cloud.google.com/sdk/docs/install-sdk. Authenticate with `gcloud auth login` and set project with `gcloud config set project PROJECT_ID`.
- **Claude Code integration:** CLI shell-out via `gcloud firebase test android run`. Non-interactive. Returns exit codes: 0 (pass), 10 (test failure), 20 (infrastructure error).

**Setup:**

```bash
gcloud components update                              # Update gcloud components
gcloud auth login                                      # Authenticate
gcloud config set project my-firebase-project          # Set project
```

**Device discovery:**

```bash
gcloud firebase test android models list               # Available device models
gcloud firebase test android versions list             # Available OS versions
gcloud firebase test android locales list              # Available locales
```

**Robo test (no test code needed):**

```bash
gcloud firebase test android run \
  --type robo \
  --app app/build/outputs/apk/debug/app-debug.apk \
  --device model=Pixel8,version=34,locale=en,orientation=portrait \
  --timeout 300s \
  --robo-directives username_field=user@test.com,password_field=testpass123
```

**Instrumented test (Espresso / UI Automator):**

```bash
gcloud firebase test android run \
  --type instrumentation \
  --app app/build/outputs/apk/debug/app-debug.apk \
  --test app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk \
  --device model=Pixel8,version=34,locale=en,orientation=portrait \
  --device model=Pixel7,version=33,locale=fr,orientation=landscape \
  --timeout 600s \
  --environment-variables coverage=true,coverageFile=/sdcard/coverage.ec \
  --directories-to-pull /sdcard/coverage.ec \
  --results-bucket my-bucket \
  --results-dir my-test-run
```

**Device matrix (multiple devices in one run):**

```bash
gcloud firebase test android run \
  --type instrumentation \
  --app app-debug.apk \
  --test app-debug-test.apk \
  --device model=Pixel8,version=34 \
  --device model=Pixel7,version=33 \
  --device model=MediumPhone.arm,version=34 \
  --client-details matrixLabel="Nightly regression"
```

**Time limits:** 45 minutes on physical devices, 60 minutes on virtual devices.

- **Notes:** Robo tests require zero test code — Firebase crawls the app automatically and reports crashes. The free tier (Spark plan) provides 5 virtual device tests/day and 5 physical device tests/day. Results are accessible in the Firebase Console and optionally stored in a GCS bucket. Firebase Test Lab integrates with the Gradle plugin `com.google.firebase:testlab-gradle-plugin` for direct `./gradlew` invocation.

---

## App Bundle & APK Tools (verify)

### bundletool

- **Link:** https://developer.android.com/tools/bundletool / https://github.com/google/bundletool
- **What it does:** The underlying tool Android Studio and Google Play use to build, deploy, and validate Android App Bundles (.aab). Generates device-specific APK sets, installs them on devices, measures sizes, and validates bundles.
- **Loop phase:** verify
- **Install:** Download JAR from https://github.com/google/bundletool/releases. Run with `java -jar bundletool.jar`. Also available via Homebrew: `brew install bundletool`.
- **Claude Code integration:** CLI shell-out via `java -jar bundletool.jar` or `bundletool` (if on PATH).

```bash
# Generate APK set from App Bundle
bundletool build-apks \
  --bundle=app-release.aab \
  --output=app.apks

# Generate APK set with signing
bundletool build-apks \
  --bundle=app-release.aab \
  --output=app.apks \
  --ks=keystore.jks \
  --ks-pass=pass:keystorePassword \
  --ks-key-alias=myAlias \
  --key-pass=pass:keyPassword

# Generate universal APK (single APK for all configs, good for quick testing)
bundletool build-apks \
  --bundle=app-release.aab \
  --output=app.apks \
  --mode=universal

# Generate APKs targeting connected device
bundletool build-apks \
  --bundle=app-release.aab \
  --output=app.apks \
  --connected-device \
  --device-id=emulator-5554

# Install APKs on connected device
bundletool install-apks --apks=app.apks
bundletool install-apks --apks=app.apks --device-id=emulator-5554

# Get device specification JSON
bundletool get-device-spec --output=device-spec.json

# Extract APKs for a specific device spec
bundletool extract-apks \
  --apks=app.apks \
  --output-dir=./extracted \
  --device-spec=device-spec.json

# Measure APK download sizes
bundletool get-size total --apks=app.apks
bundletool get-size total --apks=app.apks --dimensions=ABI,SCREEN_DENSITY

# Validate an App Bundle
bundletool validate --bundle=app-release.aab

# Enable local testing mode (bypasses Play signing)
bundletool build-apks \
  --bundle=app.aab \
  --output=app.apks \
  --local-testing
```

### apkanalyzer

- **Link:** https://developer.android.com/tools/apkanalyzer
- **What it does:** CLI tool for inspecting APK composition: file sizes, manifest details, DEX method counts, class trees, and APK-to-APK comparisons. Useful for verifying APK size budgets and checking method reference counts (the 64K limit).
- **Loop phase:** verify
- **Install:** Part of SDK Command-Line Tools (`sdkmanager "cmdline-tools;latest"`). Located at `$ANDROID_HOME/cmdline-tools/latest/bin/apkanalyzer`.

```bash
# APK overview
apkanalyzer apk summary app-debug.apk              # App ID, version code, version name
apkanalyzer -h apk file-size app-debug.apk          # APK file size (human-readable)
apkanalyzer -h apk download-size app-debug.apk      # Estimated download size
apkanalyzer apk features app-debug.apk              # Features used by APK
apkanalyzer apk compare old.apk new.apk             # Compare two APKs
apkanalyzer apk compare --different-only old.apk new.apk  # Only differences

# Files
apkanalyzer files list app-debug.apk                # List all files in APK
apkanalyzer files cat --file /AndroidManifest.xml app-debug.apk  # Print file contents

# Manifest
apkanalyzer manifest print app-debug.apk            # Full manifest XML
apkanalyzer manifest application-id app-debug.apk   # Application ID
apkanalyzer manifest version-name app-debug.apk     # Version name
apkanalyzer manifest version-code app-debug.apk     # Version code
apkanalyzer manifest min-sdk app-debug.apk           # Minimum SDK version
apkanalyzer manifest target-sdk app-debug.apk        # Target SDK version
apkanalyzer manifest permissions app-debug.apk       # Permissions list
apkanalyzer manifest debuggable app-debug.apk        # Is debuggable?

# DEX analysis
apkanalyzer dex list app-debug.apk                  # List DEX files
apkanalyzer dex references app-debug.apk            # Method reference count (check vs 64K)
apkanalyzer dex packages app-debug.apk              # Class tree (P=package, C=class, M=method)
apkanalyzer dex packages --defined-only app-debug.apk  # Only classes defined in APK
apkanalyzer dex code --class com.example.MyClass app-debug.apk  # Smali bytecode
```

### aapt2 (Android Asset Packaging Tool 2)

- **Link:** https://developer.android.com/tools/aapt2
- **What it does:** Compiles and links Android resources. Bundled with build-tools and used internally by AGP, but available for standalone resource compilation.
- **Loop phase:** implement
- **Install:** Part of SDK Build Tools (`sdkmanager "build-tools;34.0.0"`).

```bash
# Compile a single resource
aapt2 compile src/main/res/drawable/icon.png -o compiled/

# Compile all resources in a directory
aapt2 compile --dir src/main/res/ -o compiled/

# Link compiled resources into APK
aapt2 link -o output.apk \
  -I $ANDROID_HOME/platforms/android-34/android.jar \
  --manifest AndroidManifest.xml \
  -R compiled/*.flat \
  --auto-add-overlay

# Dump APK information
aapt2 dump badging app-debug.apk       # Package name, version, permissions
aapt2 dump resources app-debug.apk     # Resource table
aapt2 dump xmltree app-debug.apk AndroidManifest.xml  # XML tree
```

- **Notes:** Most Android developers interact with aapt2 indirectly through AGP. Direct use is primarily for CI scripts, custom build pipelines, or resource validation.

---

## CI/CD Integration (verify)

### GitHub Actions

- **Link:** https://github.com/android-actions/setup-android / https://github.com/ReactiveCircus/android-emulator-runner
- **What it does:** GitHub Actions provides first-party and community actions for Android CI/CD. `actions/setup-java` configures JDK. `android-actions/setup-android` installs the Android SDK. `ReactiveCircus/android-emulator-runner` boots an emulator with hardware acceleration for instrumented tests.
- **Loop phase:** verify
- **Claude Code integration:** Claude can generate and edit `.github/workflows/*.yml` files.

**Typical workflow:**

```yaml
name: Android CI
on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'zulu'
          java-version: '17'
      - uses: android-actions/setup-android@v3
      - run: ./gradlew testDebugUnitTest lintDebug

  instrumented-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'zulu'
          java-version: '17'
      - name: Enable KVM
        run: |
          echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' \
            | sudo tee /etc/udev/rules.d/99-kvm4all.rules
          sudo udevadm control --reload-rules
          sudo udevadm trigger --name-match=kvm
      - uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          target: google_apis
          arch: x86_64
          script: ./gradlew connectedCheck
```

- **Notes:** GitHub Actions has supported hardware-accelerated Android virtualization on Linux runners since April 2024. The KVM enable step is required on ubuntu-latest. ReactiveCircus/android-emulator-runner handles SDK install, AVD creation, emulator boot, waiting for boot, running the test script, and emulator teardown.

### Bitrise

- **Link:** https://bitrise.io/solutions/technologies/android
- **What it does:** Mobile-first CI/CD platform with pre-built steps for Android builds, unit tests, instrumented tests, and deployment. Configured via `bitrise.yml`.
- **Loop phase:** verify

```yaml
workflows:
  primary:
    steps:
      - git-clone: {}
      - android-build@1:
          inputs:
            - module: app
            - variant: debug
      - android-unit-test@1:
          inputs:
            - module: app
            - variant: debug
            - project_location: $BITRISE_SOURCE_DIR
```

Key steps: `android-build`, `android-unit-test`, `android-lint`, `virtual-device-testing-for-android` (Firebase Test Lab integration), `deploy-to-bitrise-io`.

### Codemagic

- **Link:** https://codemagic.io/android-continuous-integration/
- **What it does:** CI/CD platform supporting native Android, Flutter, React Native, and more. Configured via `codemagic.yaml` or the web UI. Supports emulator-based testing and Firebase Test Lab integration.
- **Loop phase:** verify

```yaml
workflows:
  android-workflow:
    name: Android Workflow
    instance_type: mac_mini_m2
    environment:
      java: 17
      android_signing:
        - my_keystore
    scripts:
      - name: Build debug APK
        script: ./gradlew assembleDebug
      - name: Run unit tests
        script: ./gradlew testDebugUnitTest
      - name: Run instrumented tests
        script: |
          emulator -avd test_avd -no-window -no-audio &
          adb wait-for-device
          ./gradlew connectedCheck
    artifacts:
      - app/build/outputs/**/*.apk
    publishing:
      firebase:
        firebase_token: $FIREBASE_TOKEN
```

### CircleCI

- **Link:** https://circleci.com/developer/orbs/orb/circleci/android
- **What it does:** CI/CD platform with a dedicated Android orb providing executors, commands, and jobs for building and testing Android apps. Supports emulator-based instrumented testing via `android/start-emulator-and-run-tests`.
- **Loop phase:** verify

```yaml
version: 2.1
orbs:
  android: circleci/android@2.5

jobs:
  test:
    executor:
      name: android/android-machine
      tag: 2025.03.1
    steps:
      - checkout
      - android/restore-gradle-cache
      - run: ./gradlew testDebugUnitTest lintDebug
      - android/save-gradle-cache
      - android/start-emulator-and-run-tests:
          system-image: system-images;android-34;google_apis;x86_64
          run-tests-working-directory: .
          test-command: ./gradlew connectedCheck

workflows:
  build-and-test:
    jobs:
      - test
```

The orb provides: `create_avd`, `start_emulator`, `wait_for_emulator`, `run_tests` commands with automatic retry support.

---

## Claude Code Integration (all phases)

### Kotlin Language Server (LSP)

- **Link:** https://claude.com/plugins/kotlin-lsp / https://github.com/Piebald-AI/claude-code-lsps
- **What it does:** Provides IDE-level code intelligence for Kotlin in Claude Code: go-to-definition, find-references, hover documentation, document symbols, and diagnostics. Released December 2025.
- **Loop phase:** all (plan, implement, verify)
- **Install:** `brew install JetBrains/utils/kotlin-lsp` (requires Java 17+). Then install the Claude Code plugin: `/plugin install kotlin-language-server@claude-code-lsps`.
- **Claude Code integration:** Native LSP tool integration. Once installed, Claude Code gains five LSP operations: `goToDefinition`, `findReferences`, `hover`, `documentSymbol`, `getDiagnostics`.

**LSP capabilities:**

- `goToDefinition` — jump to where a symbol is defined
- `findReferences` — find all usages of a symbol
- `hover` — show type info and documentation
- `documentSymbol` — list all symbols in a file
- `getDiagnostics` — show compiler errors and warnings

- **Notes:** Currently supports JVM-only Kotlin Gradle projects. Multiplatform Kotlin support is in progress. The LSP provides real-time diagnostics that Claude can use to catch errors before running a build.

### MCP Servers for Android

Several MCP servers bridge Claude Code to Android device/emulator control:

**mobile-mcp (recommended)**

- **Link:** https://github.com/mobile-next/mobile-mcp
- **What it does:** Platform-agnostic MCP server for both Android and iOS automation. Provides device management, app management, screen interaction (tap, swipe, type), screenshot capture, and element inspection.
- **Install for Claude Code:** `claude mcp add mobile-mcp -- npx -y @mobilenext/mobile-mcp@latest`
- **Requires:** Node.js v22+, Android Platform Tools (ADB), running emulator or connected device.

**android-mcp-server**

- **Link:** https://github.com/minhalvp/android-mcp-server
- **What it does:** Android-only MCP server exposing ADB commands as MCP tools. Device management, app install/uninstall, screenshots, logcat, shell commands.
- **Install:** Clone the repo and configure in Claude Code's MCP settings.

**adb-mcp**

- **Link:** https://github.com/srmorete/adb-mcp
- **What it does:** TypeScript-based MCP server for ADB interaction. Bridges AI models to Android device functionality.
- **Install:** npm-based, configured via MCP JSON settings.

**android_emulator_mcp**

- **Link:** https://lobehub.com/mcp/amm-ar-android_emulator_mcp
- **What it does:** MCP server specifically for emulator control — AVD management, APK install, tap, swipe, type, screenshots, logcat.

### Direct CLI Shell-Out (always available)

Claude Code can invoke any Android tool directly via shell without MCP servers:

```bash
# Build
./gradlew assembleDebug

# Install and launch
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n com.example.app/.MainActivity

# Capture screenshot for visual verification
adb exec-out screencap -p > /tmp/screen.png

# Read logs
adb logcat -d "*:E"

# Run tests
./gradlew testDebugUnitTest
./gradlew connectedCheck

# Run Maestro flow
maestro test flows/login.yaml
```

- **Notes:** For most Android development tasks in Claude Code, direct CLI shell-out is sufficient. MCP servers add value when you want Claude to interact with the device more fluidly (e.g., tap, inspect elements, capture screenshots as part of a conversation flow). The Kotlin LSP is the highest-value integration for code quality during the implement phase.

---

## Sources

- [Build your app from the command line - Android Developers](https://developer.android.com/build/building-cmdline)
- [Android Debug Bridge (adb) - Android Developers](https://developer.android.com/tools/adb)
- [Start the emulator from the command line - Android Developers](https://developer.android.com/studio/run/emulator-commandline)
- [Maestro Documentation](https://docs.maestro.dev/)
- [UI Automator - Android Developers](https://developer.android.com/training/testing/other-components/ui-automator)
- [Firebase Test Lab gcloud CLI](https://firebase.google.com/docs/test-lab/android/command-line)
- [bundletool - Android Developers](https://developer.android.com/tools/bundletool)
- [apkanalyzer - Android Developers](https://developer.android.com/tools/apkanalyzer)
- [ReactiveCircus/android-emulator-runner](https://github.com/ReactiveCircus/android-emulator-runner)
- [android-actions/setup-android](https://github.com/android-actions/setup-android)
- [CircleCI Android Orb](https://circleci.com/developer/orbs/orb/circleci/android)
- [Bitrise Android CI/CD](https://bitrise.io/solutions/technologies/android)
- [Codemagic Android CI/CD](https://codemagic.io/android-continuous-integration/)
- [Kotlin LSP - Claude Plugin](https://claude.com/plugins/kotlin-lsp)
- [Piebald-AI/claude-code-lsps](https://github.com/Piebald-AI/claude-code-lsps)
- [mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp)
- [minhalvp/android-mcp-server](https://github.com/minhalvp/android-mcp-server)
- [srmorete/adb-mcp](https://github.com/srmorete/adb-mcp)
- [ADB Commands List 2025 - MattInTech](https://mattintech.github.io/tools/adb-cmd/)
- [Gradle Command-Line Interface](https://docs.gradle.org/current/userguide/command_line_interface.html)
- [Gradle Build Performance](https://docs.gradle.org/current/userguide/performance.html)
