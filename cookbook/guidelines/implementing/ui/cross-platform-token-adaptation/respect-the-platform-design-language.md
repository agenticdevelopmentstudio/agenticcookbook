
- Adapt to the host idiom — navigation patterns, control shapes, default density, and haptics — rather than forcing one platform's look onto another. See `agenticdevelopercookbook://guidelines/planning/ui/platform-design-languages`.
- Component-level tokens **MAY** diverge per platform (e.g., corner radius, elevation vs. shadow) while sharing the same semantic ancestor.
- Centralized design-system tooling (token build pipelines, multi-target generators) is an adopt-when-measured-need-justifies investment (per YAGNI): start with a single shared file and per-platform transforms; add heavier infrastructure only when token volume or platform count makes it pay off.

