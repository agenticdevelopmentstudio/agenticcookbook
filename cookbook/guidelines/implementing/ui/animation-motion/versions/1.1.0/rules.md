
- **should-make-motion-purposeful**: Motion SHOULD be purposeful — guide attention, show spatial relationships, and provide feedback.
- **must-not-animate-for-decoration**: Motion MUST NOT be used for decoration — never animate for decoration.
- **should-use-duration-defaults**: When no platform value exists, durations SHOULD follow the duration defaults (see *Duration defaults*).
- **should-prefer-platform-curves**: Platform-native spring/easing curves SHOULD be preferred over linear or custom beziers
- **must-respect-reduced-motion**: **Reduced-motion preferences MUST be respected** — see [adc.guideline.implementing.accessibility.accessibility](cookbook:3d970d6a-2d71-48f3-9f84-69c1d823d6e8) and each platform
  file's accessibility settings table. When reduced motion is enabled, replace animations
  with instant state changes or simple cross-fades.
- **should-not-cover-large-distances-loop-or-flash**: Motion SHOULD NOT cover large distances, loop continuously, or flash
