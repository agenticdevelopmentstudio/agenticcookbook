
# Feedback Patterns

Every user action should have visible feedback. The weight of the feedback should match
the weight of the action.

- **Inline feedback** — field-level validation, character counts, progress within a component.
  Lowest weight, least disruptive.
- **Toast / Snackbar** — non-critical confirmations ("Saved", "Copied to clipboard"). Auto-dismiss
  after 3-5 seconds. No user action required. Toasts MUST NOT be used for errors.
- **Banner / Inline alert** — persistent messages that need attention but don't block work
  (connectivity warning, degraded mode). Dismissible.
- **Dialog / Alert** — destructive or irreversible actions requiring explicit confirmation
  ("Delete 12 items? This cannot be undone."). Use sparingly — dialog fatigue leads to
  click-through without reading.
- Dialogs MUST NOT be used for success messages — a toast or inline confirmation is sufficient.
- **Destructive actions** MUST require explicit confirmation with a clearly labeled action
  ("Delete", not "OK"). Default focus should be on the safe option (Cancel).

References:
- [Apple HIG: Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)
- [Material Design: Snackbar](https://m3.material.io/components/snackbar/overview)
- [NNGroup: Confirmation Dialogs](https://www.nngroup.com/articles/confirmation-dialog/)
- [NNGroup: Ten Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) (Heuristic #1: Visibility of system status)

