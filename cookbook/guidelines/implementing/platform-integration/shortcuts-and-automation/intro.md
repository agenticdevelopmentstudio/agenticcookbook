
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

