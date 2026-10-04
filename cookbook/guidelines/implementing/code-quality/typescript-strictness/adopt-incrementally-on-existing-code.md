
The stricter flags surface real defects but generate large error volumes on legacy code. Per `agenticdevelopercookbook://principles/small-reversible-decisions`:

- Turn on `strict` first; land that as its own change.
- Enable one stricter flag at a time (`noUncheckedIndexedAccess`, then `exactOptionalPropertyTypes`, etc.), fixing the fallout before moving on.
- Agents **SHOULD NOT** enable every flag in a single sweep on an established codebase — small, reviewable diffs keep each step reversible.

