<!-- leaf: implement-internationalization/rtl-support · source: guidelines/implementing/internationalization/rtl-support.md -->

**Rules** (cite as `implement-internationalization/rtl-support#<slug>`):

- `layouts-support-right-left-languages` MUST — All layouts MUST support right-to-left languages:
- `layouts-support-right-left-languages-2` MUST — All layouts MUST support right-to-left languages. Use leading/trailing (not left/right) for alignment and padding. …

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

## Kotlin

Set `android:supportsRtl="true"` in the manifest. Use `start`/`end` instead of `left`/`right` in layouts. Force RTL in developer options for testing.

## TypeScript

Use CSS logical properties throughout:

- `margin-inline-start` instead of `margin-left`
- `padding-inline-end` instead of `padding-right`
- `inset-inline-start` instead of `left`

Set `dir="rtl"` attribute on the root element for RTL locales.

## Windows

- Set `FlowDirection="RightToLeft"` on the root element for RTL locales
- WinUI 3 XAML layout handles leading/trailing automatically when FlowDirection is set
- Mirror icons with directional meaning (forward/back arrows)
- Do NOT mirror non-directional icons (checkmarks, clocks)
- Test with RTL language packs installed
