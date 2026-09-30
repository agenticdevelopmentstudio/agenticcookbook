<!-- leaf: implement-ui/form-design · source: guidelines/implementing/ui/form-design.md -->

**Rules** (cite as `implement-ui/form-design#<slug>`):

- `single-column-layout-used-outperforms-multi-column` SHOULD — Single-column layout SHOULD be used — outperforms multi-column for completion rate
- `validation-not-fire-while-user-still` MUST — Validation MUST NOT fire while the user is still actively typing in a field
- `errors-shown-inline-directly-below` MUST — Errors MUST be shown inline, directly below the field — not only at the top of the form

# Form Design

Forms are where users do real work. Reduce friction at every step.

###  Layout
- Single-column layout SHOULD be used — outperforms multi-column for completion rate
- Top-aligned or floating labels — fastest to scan and complete
- Group related fields visually with spacing or section headers
- Place primary action (Submit/Save) at the bottom, aligned with the form fields

###  Validation
- Validate on **blur** (when user leaves the field), not on every keystroke
- Validate the **full form on submit** as a final safety net
- Validation MUST NOT fire while the user is still actively typing in a field
- Success indicators (checkmarks) only for fields where the user genuinely wonders if
  input was accepted (e.g., username availability)

###  Error messages
- Errors MUST be shown **inline, directly below the field** — not only at the top of the form
- Use color + icon + text (never color alone)
- Be specific and actionable: "Password must be at least 8 characters" not "Invalid input"
- Don't blame the user

###  Other principles
- Use placeholder text for format hints, not as label replacement — placeholders disappear on focus
- Pre-fill and default where possible to reduce effort
- Mark optional fields, not required ones (most fields should be required; if they're not,
  reconsider asking)

References:
- [NNGroup: Form Design Guidelines](https://www.nngroup.com/articles/web-form-design/)
- [NNGroup: Error Messages in Forms](https://www.nngroup.com/articles/errors-forms-design-guidelines/)
- [Apple HIG: Text Fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)
- [Material Design: Text Fields](https://m3.material.io/components/text-fields/guidelines)
