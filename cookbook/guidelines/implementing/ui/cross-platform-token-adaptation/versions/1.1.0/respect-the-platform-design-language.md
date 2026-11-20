
- Adapt to the host idiom — navigation patterns, control shapes, default density, and haptics — rather than forcing one platform's look onto another. See [adc.guideline.implementing.ui.platform-design-languages](cookbook:3741ed5e-0b67-48f2-b227-36ae152c0f4b).
- Component-level tokens **MAY** diverge per platform (e.g., corner radius, elevation vs. shadow) while sharing the same semantic ancestor.
- Centralized design-system tooling (token build pipelines, multi-target generators) is an adopt-when-measured-need-justifies investment (per YAGNI): start with a single shared file and per-platform transforms; add heavier infrastructure only when token volume or platform count makes it pay off.

