<!-- leaf: compliance/internationalization · source: compliance/internationalization.md -->

**Rules** (cite as `compliance/internationalization#<slug>`):

- `user-visible-strings-externalized-into-localization-resource` MUST — All user-visible strings MUST be externalized into localization resource files.
- `layout-adapt-correctly-right-left` MUST — Layout MUST adapt correctly for right-to-left languages.
- `dates-numbers-currencies-use-locale-aware-formatting` MUST — Dates, numbers, and currencies MUST use locale-aware formatting APIs.
- `pluralized-strings-use-locale-appropriate-plural` MUST — Pluralized strings MUST use locale-appropriate plural rules, not simple singular/plural.
- `layout-accommodate-text-expansion-up` MUST — Layout MUST accommodate text expansion of up to 200% without truncation or overflow.
- `text-processing-support-full-unicode-character` MUST — All text processing MUST support the full Unicode character set including emoji.
- `user-visible-strings-not-hardcoded-source-code` MUST — User-visible strings MUST NOT be hardcoded in source code.

# Internationalization

Internationalization checks ensure that recipes and guidelines properly support multiple languages, locales, and writing systems. These checks are derived from internationalization guidelines and apply to any component with user-visible text or locale-sensitive formatting.

## Applicability

All recipes with user-visible text or locale-sensitive formatting. Guidelines covering UI text, date/number display, or layout.

## Checks

### string-externalization

All user-visible strings MUST be externalized into localization resource files.

**Applies when:** recipe displays text to users.

**Guidelines:**
- Localization

---

### rtl-layout-support

Layout MUST adapt correctly for right-to-left languages.

**Applies when:** recipe renders UI that may be used in RTL locales.

**Guidelines:**
- RTL Support

---

### locale-aware-formatting

Dates, numbers, and currencies MUST use locale-aware formatting APIs.

**Applies when:** recipe displays dates, numbers, or currency values.

**Guidelines:**
- Localization

---

### plural-forms

Pluralized strings MUST use locale-appropriate plural rules, not simple singular/plural.

**Applies when:** recipe displays counted or quantified items.

**Guidelines:**
- Localization

---

### text-expansion-tolerance

Layout MUST accommodate text expansion of up to 200% without truncation or overflow.

**Applies when:** recipe renders UI with translated text.

**Guidelines:**
- Localization

---

### unicode-support

All text processing MUST support the full Unicode character set including emoji.

**Applies when:** recipe processes, stores, or displays user-provided or translated text.

**Guidelines:**
- Localization

---

### no-hardcoded-strings

User-visible strings MUST NOT be hardcoded in source code.

**Applies when:** recipe contains source code with user-facing text.

**Guidelines:**
- Localization
