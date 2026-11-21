
- Frontmatter first, complete, `type: ingredient`, and the H1 equal to the `title`.
- Sections in the prescribed order, each present one under its specified heading and level, and none left empty without a one-line "none".
- An Overview that says what the component is, when to use it, when not to and why to.
- Behavioral requirements in one style, each named and carrying the RFC 2119 keyword of its level, and test vectors that pair an input with its outcome, name the requirements they test, and cover passed, failed and inapplicable.
- Accessibility that gives role, label, how state changes are announced, keyboard interaction and a target size per platform, not one value; and, for an infrastructure ingredient, why accessibility is out of scope.
- States that include every state the component takes, hover and selected among them where they apply, with contrast holding in each.
- An ingredient that shows text carrying `## Accessibility Options` with its 200 percent text resizing.
- Edge cases that list assumptions, limitations and exceptions, and what is out of scope and why.
- Platform specifics taken from the platform: verified https deep links, Firebase-valid event names, Apple's meaning for subsystem and category, an entry per targeted platform.
- Privacy that says what is collected, kept, transmitted and encrypted, even when the answer is none.
- Design decisions that carry their status; compliance rows linked by UUID, with `inapplicable` for a check that does not apply.
- A Change History row per version with ISO 8601 dates, and no released version edited in place.

