
- When you replace an implementation, you MUST delete the one it replaces in the same change — do not leave the old and new versions side by side, or behind a flag that is permanently off.
- When you rename or move something, you MUST update or remove every reference; no path, import, or export may point at the thing that no longer exists.
- Commented-out code MUST be deleted, not left as a tombstone. Version control is the history.

