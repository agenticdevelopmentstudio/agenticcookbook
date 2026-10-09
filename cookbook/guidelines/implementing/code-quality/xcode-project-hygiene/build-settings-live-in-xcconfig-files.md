
- Put build settings in `.xcconfig` files, not in the project editor's Build Settings tab. A configuration file is plain text, so a setting change is a one-line diff, and the file can be edited without Xcode.
- Keep one shared file for settings common to every target and one per configuration or target for the differences. Add only the settings you want to change.
- Xcode applies the project's settings, then the configuration file's settings, then the target's settings. Leave the target-level Build Settings tab empty for any setting an xcconfig already owns, or the target value silently wins.
- The format is `SettingName = value`, one per line. If a setting appears twice in a file, the last one wins.
- Create the file with "Configuration Settings File" and deselect all targets so Xcode does not embed it in the bundle.
- Look up each setting name in the build settings reference before you use it. Do not guess a name; an unknown setting is ignored without an error.

