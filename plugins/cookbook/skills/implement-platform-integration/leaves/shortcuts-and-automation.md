<!-- leaf: implement-platform-integration/shortcuts-and-automation · source: guidelines/implementing/platform-integration/shortcuts-and-automation.md -->

**Rules** (cite as `implement-platform-integration/shortcuts-and-automation#<slug>`):

- `components-flows-scriptable-where-platform-supports` SHOULD — Components and flows SHOULD be scriptable where the platform supports it:
- `components-flows-scriptable-where-platform-supports-2` SHOULD — Components and flows SHOULD be scriptable where the platform supports it. Automation enables power users to integrate …

# Scriptable and automatable

Components and flows SHOULD be scriptable where the platform supports it:

- **Apple (macOS)**: `AppIntents` for Shortcuts, AppleScript via `NSScriptCommand`
- **Apple (iOS)**: `AppIntents` for Shortcuts and Siri integration
- **Android**: `AppActions` for Google Assistant, `Intent`-based automation
- **Web**: API endpoints or query parameter-driven actions
- **Windows**: Protocol activation, command-line activation, `AppInstance` APIs. WinUI 3 has limited scripting support compared to other platforms.

---

# Shortcuts and Automation

Components and flows SHOULD be scriptable where the platform supports it. Automation enables power users to integrate app functionality into workflows, voice assistants, and third-party tools.

## Swift

Use the `AppIntents` framework for Shortcuts and Siri integration. On macOS, support AppleScript via `NSScriptCommand` where appropriate.

## Kotlin

Use `AppActions` for Google Assistant integration. Support `Intent`-based automation.
