
- `should-make-motion-purposeful`: whether every animation guides attention, shows a spatial relationship or provides feedback
- `must-not-animate-for-decoration`: whether any animation is purely decorative
- `should-use-duration-defaults`: whether, where no platform value exists, each duration follows the default for its interaction
- `should-prefer-platform-curves`: whether animations use platform-native spring/easing curves rather than linear or custom beziers
- `must-respect-reduced-motion`: whether every animation is replaced by an instant state change or simple cross-fade when reduced motion is enabled
- `should-not-cover-large-distances-loop-or-flash`: whether any motion covers large distances, loops continuously or flashes
- `must-respect-reduced-motion`: `prefers-reduced-motion` media query handled in CSS;
- `should-use-duration-defaults`: transition durations within specified ranges for interaction type
