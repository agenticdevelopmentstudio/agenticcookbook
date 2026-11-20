
# RTL layout support

All layouts MUST support right-to-left languages:

1. Use **leading/trailing** (not left/right) for alignment and padding
2. Mirror icons with directional meaning (forward/back arrows)
3. Do NOT mirror non-directional icons (checkmarks, clocks)
4. Test with RTL locale enabled

Platform notes:
- **Apple**: Use `.environment(\.layoutDirection, .rightToLeft)` in previews. SwiftUI handles leading/trailing automatically.
- **Android**: Set `android:supportsRtl="true"`. Use `start`/`end` instead of `left`/`right`.
- **Web**: Use `dir="rtl"` attribute. Use CSS logical properties (`margin-inline-start` not `margin-left`).
- **Windows**: Use `FlowDirection` property. WinUI 3 XAML handles leading/trailing automatically.

---

# RTL Support

All layouts MUST support right-to-left languages. Use leading/trailing (not left/right) for alignment and padding. Mirror icons with directional meaning (forward/back arrows). Do NOT mirror non-directional icons (checkmarks, clocks). Test with an RTL locale enabled.

