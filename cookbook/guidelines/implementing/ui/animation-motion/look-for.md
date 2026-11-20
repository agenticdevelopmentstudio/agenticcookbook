
- `should-make-motion-purposeful`: an animation that guides no attention, shows no spatial relationship and gives no feedback
- `must-not-animate-for-decoration`: an animation that exists only for decoration
- `should-use-duration-defaults`: a hand-picked duration outside the default range for its interaction where no platform value exists
- `should-prefer-platform-curves`: linear or custom bezier curves where a platform-native spring/easing curve exists
- `must-respect-reduced-motion`: an animation that still runs when reduced motion is enabled, instead of an instant state change or simple cross-fade
- `should-not-cover-large-distances-loop-or-flash`: motion across large distances, continuous loops, or flashing
- `should-use-duration-defaults`: CSS transitions and JS animations use correct duration ranges per interaction type;
- `must-respect-reduced-motion`: `prefers-reduced-motion: reduce` media query disables/simplifies all animations;
