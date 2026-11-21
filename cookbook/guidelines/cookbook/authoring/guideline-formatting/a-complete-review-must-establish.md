
- Every required frontmatter field is present, `domain` is absent, `type` is `guideline`, and every `triggers` name is in the trigger guide.
- The H1 matches the `title` exactly, it is the only H1, and no heading level is skipped.
- The summary statement sits directly under the H1 and stands on its own.
- Every part but the intro and the history has a role, and the `rules`, `review-focus`, `review-bar` and `build-bar` roles are each present.
- Every bullet in a `rules` part is a uniquely named rule with an RFC 2119 keyword, one requirement, a checkable statement and the circumstances it applies in.
- Every rule ends with one citation, every cited id is a claim in `research/research.json`, and every cited claim is named by a verdict.
- No rule is stronger than the weakest claim it cites.
- Examples, notes and rationale are informative and state no requirement of their own.
- The build bar has exactly one line per named rule and no other line naming anything.
- Rule names are unchanged from the previous version, or the change is a new version.
- The topic has one folder and links out rather than repeating what other docs say.
- The file ends with a change history table with Version, Date, Author and Summary columns and a row for every version.

