
- Frontmatter first, complete, `type: ingredient`, and the H1 equal to the `title`.
- Sections in the prescribed order, each present one under its specified heading and level, and none left empty without a one-line "none".
- An Overview that says what the component is, when to use it and when not to.
- Behavioral requirements that are named and carry RFC 2119 keywords, and test vectors that map to them, with passed, failed and inapplicable outcomes.
- Accessibility that covers role, label, state announcements, keyboard interaction and a target size per platform, not one value.
- States that include every state the component takes, hover and selected among them where they apply, with contrast holding in each.
- Platform specifics taken from the platform: verified https deep links, Firebase-valid event names, Apple's meaning for subsystem and category.
- Privacy that says what is collected, kept, transmitted and encrypted, even when the answer is none.
- Compliance rows linked by UUID, with `inapplicable` for a check that does not apply.
- A Change History row per version with ISO 8601 dates, and no released version edited in place.

