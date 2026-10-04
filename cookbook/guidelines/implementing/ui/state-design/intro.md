
# State Design

Every view that loads data or can be empty MUST handle all four states explicitly. A blank
screen with no explanation MUST NOT be shown.

**The four states:**

1. **Loading** — show progress (see agenticdevelopercookbook://guidelines/implementing/ui/always-show-progress). Use skeleton screens for content-heavy
   views, spinners for actions. Never block the entire screen for a partial load.
2. **Empty** — explain what belongs here, why it's empty, and provide a single clear action to
   populate it. Use an icon or illustration, a brief message, and a CTA button.
3. **Error** — identify the problem, explain why if possible, and offer a recovery action (retry,
   go back, contact support). Raw error codes or stack traces MUST NOT be shown. Don't blame the user.
4. **Loaded** — the normal content state.

Design empty and error states with the same care as the loaded state — they are often the
user's first impression.

References:
- [Apple HIG: Empty States](https://developer.apple.com/design/human-interface-guidelines/empty-states)
- [NNGroup: Empty State Design](https://www.nngroup.com/articles/empty-state-interface-design/)
- [NNGroup: Error Message Guidelines](https://www.nngroup.com/articles/error-message-guidelines/)
- [Material Design: Empty States (M2 reference)](https://material.io/design/communication/empty-states.html)

