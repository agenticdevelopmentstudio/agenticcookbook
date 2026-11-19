
# Localizability

All user-facing strings MUST be localizable — no hardcoded strings:

- **Apple**: `String(localized:)` or `NSLocalizedString`. Store in `.xcstrings` or `.strings`.
- **Android**: `strings.xml` resources. Reference via `R.string.*` or `stringResource()`.
- **Web**: i18n library (`react-intl`, `i18next`). Extract to message catalogs.
- **Windows**: `.resw` resource files with `x:Uid` in XAML. `ResourceLoader` from MRT Core for code-behind access.

---

# Localization

All user-facing strings MUST be localizable. No hardcoded strings. Store strings in platform-standard resource files and reference them through the platform's localization API.

