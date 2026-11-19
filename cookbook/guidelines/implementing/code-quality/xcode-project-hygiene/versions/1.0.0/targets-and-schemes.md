
- Schemes MUST be shared (stored in the project's shared data, not in a user's private data) and checked in, so command-line builds and CI use the same schemes as the IDE.
- One scheme per thing a person builds, runs or tests. Delete schemes that no longer build.
- Name targets and schemes after what they produce. Do not leave `Untitled`, a copied target's `copy` suffix or a stale product name.
- Keep test targets separate from app targets, and set each target's deployment target explicitly in the xcconfig, not by default.

