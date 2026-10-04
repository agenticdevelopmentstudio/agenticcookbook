
# Animation & Motion

Motion should be purposeful — guide attention, show spatial relationships, and provide
feedback. Never animate for decoration.

**Duration defaults** (when no platform value exists):

| Interaction | Duration |
|------------|----------|
| Micro-feedback (ripple, highlight) | 50-100ms |
| State change (hover, toggle, press) | 100-200ms |
| Component enter/exit | 200-350ms |
| Page/navigation transition | 300-500ms |
| Complex choreography (rare) | 500-1000ms |

- Under 100ms feels instant. Over 500ms feels sluggish.
- Platform-native spring/easing curves SHOULD be preferred over linear or custom beziers
- **Reduced-motion preferences MUST be respected** — see agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility and each platform
  file's accessibility settings table. When reduced motion is enabled, replace animations
  with instant state changes or simple cross-fades.
- Motion SHOULD NOT cover large distances, loop continuously, or flash

References:
- [Apple HIG: Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- [Material Design: Motion](https://m3.material.io/styles/motion/overview)
- [Fluent Design: Timing and Easing](https://learn.microsoft.com/en-us/windows/apps/design/motion/timing-and-easing)

