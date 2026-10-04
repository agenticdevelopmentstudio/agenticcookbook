
- **MUST NOT** return `WindowInsetsCompat.CONSUMED` from a parent if child views also need the same insets — consuming stops dispatch downward.
- **MUST NOT** mix `fitsSystemWindows="true"` with manual inset listeners on the same view; pick one strategy per view.
- Test in both gesture and 3-button navigation, with a display cutout, and with the keyboard open.

