
- Define an explicit **`@layer`** order (e.g. `@layer reset, base, components, utilities`) so cascade precedence is by layer, not by escalating specificity. Import third-party CSS into a low-priority layer to keep it overridable without `!important`.
- Use **`:has()`** to drive conditional styling from descendant or sibling state instead of toggling classes in JavaScript (e.g. `form:has(:invalid)`, `.card:has(> img)`).
- Use **native nesting** for co-locating related rules; do not nest deeply — flat, shallow rules stay readable and greppable.

