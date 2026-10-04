
### Profile structure

- **profile-structure**: Each profile MUST have: a unique ID (UUID), a display name, an appearance preference (dark/light/auto), font name, font size, cursor style, a color palette, and a deletable flag.
- **palette-format**: The color palette MUST contain: foreground, background, cursor, and selection colors as `#rrggbb` hex strings, plus an array of exactly 16 ANSI colors (indices 0–15: 8 normal + 8 bright).

### Built-in profiles

- **built-in-profiles**: The app MUST ship with at least these built-in profiles (non-deletable, non-editable):

  | Name | Appearance | Background | Foreground |
  |------|-----------|-----------|-----------|
  | Solarized Dark | dark | #002b36 | #839496 |
  | Solarized Light | light | #fdf6e3 | #657b83 |
  | Dracula | dark | #282a36 | #f8f8f2 |
  | Nord | dark | #2e3440 | #d8dee9 |
  | Tokyo Night | dark | #1a1b26 | #a9b1d6 |
  | GitHub Light | light | #ffffff | #24292e |
  | Gruvbox Dark | dark | #282828 | #ebdbb2 |
  | Catppuccin Mocha | dark | #1e1e2e | #cdd6f4 |

- **stable-builtin-uuids**: Built-in profiles MUST have stable, fixed UUIDs so references survive app updates.

### User profiles

- **duplicate-profile**: Users MUST be able to duplicate any profile to create a custom copy.
- **editable-custom-profiles**: Custom profiles MUST be editable: name, appearance, font size, cursor style.
- **deletable-custom-only**: Custom profiles MUST be deletable. Built-in profiles MUST NOT be deletable.

### Active profile

- **single-active-profile**: Exactly one profile MUST be active at a time. The active profile ID MUST be persisted in user settings.
- **fallback-to-default**: If the stored active profile ID is invalid (deleted or not found), the app MUST fall back to the first built-in profile (Solarized Dark).

### Appearance mode

- **auto-appearance-mode**: Profiles with `auto` appearance MUST follow the system dark/light mode — using a dark profile when in dark mode and a light profile when in light mode. The specific dark/light mapping is a **Design Decision**.

