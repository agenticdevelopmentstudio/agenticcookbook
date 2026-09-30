<!-- leaf: review-code-quality/code-hygiene · source: guidelines/reviewing/code-quality/code-hygiene.md -->

**Rules** (cite as `review-code-quality/code-hygiene#<slug>`):

- `replace-implementation-you-delete-one-replaces-same` MUST — When you replace an implementation, you MUST delete the one it replaces in the same change — do not leave the old and …
- `move-something-you-update-remove-reference-path` MUST — When you rename or move something, you MUST update or remove every reference; no path, import, or export may point at …
- `commented-out-code-deleted-left-tombstone-version` MUST — Commented-out code MUST be deleted, not left as a tombstone. Version control is the history.
- `after-your-change-removed` MUST — Files, functions, exports, types, assets, and config that nothing references after your change MUST be removed.
- `change-makes-unused-removed-from-manifest` SHOULD — Dependencies that your change makes unused SHOULD be removed from the manifest.
- `you-remove-only-what-change` MUST — You MUST remove only what *this* change superseded or orphaned. Pre-existing dead code unrelated to your task is out of …
- `you-not-delete-code-you-do` MUST — You MUST NOT delete code you do not understand or cannot confirm is unused — confirm with a reference search first.

# Code hygiene: remove the old thing

A change is not done until what it replaced is gone. Refactors that leave the old implementation alongside the new one, and edits that strand unreferenced code, are a recurring failure of AI-generated work ("deletion phobia"): redundancy rises and structure erodes turn over turn.

## Remove what this change supersedes

- When you replace an implementation, you MUST delete the one it replaces in the same change — do not leave the old and new versions side by side, or behind a flag that is permanently off.
- When you rename or move something, you MUST update or remove every reference; no path, import, or export may point at the thing that no longer exists.
- Commented-out code MUST be deleted, not left as a tombstone. Version control is the history.

## Leave no orphans

- Files, functions, exports, types, assets, and config that nothing references after your change MUST be removed.
- Dependencies that your change makes unused SHOULD be removed from the manifest.

## Stay within scope while cleaning

- You MUST remove only what *this* change superseded or orphaned. Pre-existing dead code unrelated to your task is out of scope: **note it** for the user (see scope-discipline) rather than deleting it.
- You MUST NOT delete code you do not understand or cannot confirm is unused — confirm with a reference search first.

## Why this matters

Orphaned and dead code misleads the next reader (human or agent), inflates context and review cost, and hides which path is live. Removing the old thing keeps the change reviewable and the codebase honest about what actually runs.
