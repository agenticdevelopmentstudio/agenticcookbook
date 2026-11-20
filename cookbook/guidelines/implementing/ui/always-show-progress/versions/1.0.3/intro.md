
# Always show progress

When the UI is waiting on an async task:

- **Determinate progress** (progress bar with percentage) MUST be shown when total work is known
- **Indeterminate progress** (spinner, skeleton, shimmer) MUST be shown when it is not
- The UI MUST NOT appear frozen or unresponsive

