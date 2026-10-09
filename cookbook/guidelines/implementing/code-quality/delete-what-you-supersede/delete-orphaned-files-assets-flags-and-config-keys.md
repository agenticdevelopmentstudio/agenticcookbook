
- After the change, anything that nothing references MUST go: files, functions, exports, types, images and other assets, feature flags, config keys, environment variables, migrations of paths that no longer exist.
- A flag whose rollout is finished, or whose old branch you just removed, is an orphan. Remove the flag and the branch it guarded.
- Dependencies your change made unused SHOULD come out of the manifest in the same change.
- Confirm with a reference search before deleting. You MUST NOT delete what you cannot show is unused, and you MUST NOT widen the cleanup to unrelated dead code; note that for the user instead.

