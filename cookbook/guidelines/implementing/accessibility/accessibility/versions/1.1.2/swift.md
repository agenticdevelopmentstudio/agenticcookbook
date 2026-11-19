
Components MUST respond to these SwiftUI environment values:

| Setting | Environment Key | Action |
|---------|----------------|--------|
| Reduce Motion | `\.accessibilityReduceMotion` | Replace animations with crossfades or instant transitions |
| Reduce Transparency | `\.accessibilityReduceTransparency` | Use opaque backgrounds instead of blurs/vibrancy |
| Differentiate Without Color | `\.accessibilityDifferentiateWithoutColor` | Add icons/shapes/patterns alongside color indicators |
| Increase Contrast | `\.colorSchemeContrast` | Use higher-contrast color pairs |
| Invert Colors | `isInvertColorsEnabled` | Mark images/video with `accessibilityIgnoresInvertColors` |
| Cross-Fade Transitions | `prefersCrossFadeTransitions` | Use cross-fade instead of slide/zoom transitions |

