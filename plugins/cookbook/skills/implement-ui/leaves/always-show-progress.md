<!-- leaf: implement-ui/always-show-progress · source: guidelines/implementing/ui/always-show-progress.md -->

**Rules** (cite as `implement-ui/always-show-progress#<slug>`):

- `determinate-progress` MUST (progress bar with percentage) — MUST be shown when total work is known
- `indeterminate-progress` MUST (spinner, skeleton, shimmer) — MUST be shown when it is not
- `ui-not-appear-frozen-unresponsive` MUST — The UI MUST NOT appear frozen or unresponsive

# Always show progress

When the UI is waiting on an async task:

- **Determinate progress** (progress bar with percentage) MUST be shown when total work is known
- **Indeterminate progress** (spinner, skeleton, shimmer) MUST be shown when it is not
- The UI MUST NOT appear frozen or unresponsive
