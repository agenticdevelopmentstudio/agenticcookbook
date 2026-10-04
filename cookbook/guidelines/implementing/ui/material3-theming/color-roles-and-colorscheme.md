
- Components **MUST** consume semantic color roles (`primary`, `onPrimary`, `surface`, `onSurface`, `surfaceContainer`, `error`, `outline`, …), never raw `Color(0xFF…)` literals or app-defined palettes.
- The theme **MUST** provide both a `lightColorScheme()` and a `darkColorScheme()` and select between them based on `isSystemInDarkTheme()`.
- A `ColorScheme` is generated from five key colors (primary, secondary, tertiary, neutral, neutral-variant), each expanded into a 13-tone tonal palette. Generate schemes with the Material Theme Builder rather than hand-authoring every role.
- Read colors at use sites via `MaterialTheme.colorScheme.<role>`. **MUST NOT** read a hard-coded color when a role exists.

