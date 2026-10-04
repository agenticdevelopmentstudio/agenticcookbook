
- **mica-for-long-lived-windows**: Long-lived top-level windows (main app, Settings) **SHOULD** use Mica as the base backdrop. Mica samples the wallpaper once, so it is the performant default and aids focus by falling back to a neutral tint when the window deactivates.
- **mica-alt-for-tabbed-titlebars**: Apps with a tabbed title bar or strong title-bar/commanding contrast **SHOULD** use Mica Alt (stronger wallpaper tint). Mica Alt requires Windows App SDK 1.1+ on Windows 11 build 22000+.
- **acrylic-for-transient-surfaces**: Transient/in-app surfaces — flyouts, context menus, tooltips, command bars, light-dismiss panes — **SHOULD** use Acrylic, not Mica. Acrylic blurs what is behind it in real time, which suits momentary surfaces but is heavier than Mica.
- **one-backdrop-per-window**: An app **MUST NOT** apply a backdrop material more than once per window, and **MUST NOT** apply backdrop material to an individual UI element (it only shows through transparent layers).

