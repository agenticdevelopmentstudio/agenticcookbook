---
id: B6237653-7419-4587-B5D5-DA096956F4E3
title: "Internationalization"
domain: agenticdevelopercookbook://compliance/internationalization
type: compliance
version: 1.0.1
status: draft
language: en
created: 2026-03-28
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compliance checks for string externalization, RTL support, locale-aware formatting, and Unicode handling."
platforms: []
tags: [compliance, internationalization]
depends-on: []
related:
  - agenticdevelopercookbook://compliance/accessibility
  - agenticdevelopercookbook://compliance/platform-compliance
references: []
---

# Internationalization

Internationalization checks ensure that recipes and guidelines properly support multiple languages, locales, and writing systems. These checks are derived from internationalization guidelines and apply to any component with user-visible text or locale-sensitive formatting.

## Applicability

All recipes with user-visible text or locale-sensitive formatting. Guidelines covering UI text, date/number display, or layout.

## Checks

### string-externalization

All user-visible strings MUST be externalized into localization resource files.

**Applies when:** recipe displays text to users.

**Guidelines:**
- [Localization](agenticdevelopercookbook://guidelines/implementing/internationalization/localization)

---

### rtl-layout-support

Layout MUST adapt correctly for right-to-left languages.

**Applies when:** recipe renders UI that may be used in RTL locales.

**Guidelines:**
- [RTL Support](agenticdevelopercookbook://guidelines/implementing/internationalization/rtl-support)

---

### locale-aware-formatting

Dates, numbers, and currencies MUST use locale-aware formatting APIs.

**Applies when:** recipe displays dates, numbers, or currency values.

**Guidelines:**
- [Localization](agenticdevelopercookbook://guidelines/implementing/internationalization/localization)

---

### plural-forms

Pluralized strings MUST use locale-appropriate plural rules, not simple singular/plural.

**Applies when:** recipe displays counted or quantified items.

**Guidelines:**
- [Localization](agenticdevelopercookbook://guidelines/implementing/internationalization/localization)

---

### text-expansion-tolerance

Layout MUST accommodate text expansion of up to 200% without truncation or overflow.

**Applies when:** recipe renders UI with translated text.

**Guidelines:**
- [Localization](agenticdevelopercookbook://guidelines/implementing/internationalization/localization)

---

### unicode-support

All text processing MUST support the full Unicode character set including emoji.

**Applies when:** recipe processes, stores, or displays user-provided or translated text.

**Guidelines:**
- [Localization](agenticdevelopercookbook://guidelines/implementing/internationalization/localization)

---

### no-hardcoded-strings

User-visible strings MUST NOT be hardcoded in source code.

**Applies when:** recipe contains source code with user-facing text.

**Guidelines:**
- [Localization](agenticdevelopercookbook://guidelines/implementing/internationalization/localization)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |
