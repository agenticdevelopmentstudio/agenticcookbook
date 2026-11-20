
- **Vague requirement.** `SHOULD handle errors appropriately.` — "Appropriately" is undefined. The reviewer cannot test it; the developer cannot implement against it. A conformant version: `MUST display an inline error message adjacent to the triggering control when a validation error occurs.`
- **Implementation-specific language.** `MUST use UIAlertController to display the error.` — This prescribes iOS SDK usage, eliminating valid alternatives and making the requirement platform-locked. A conformant version: `MUST display the error in a modal dialog that blocks interaction until dismissed.`
- **Untestable statement.** `MUST provide a good user experience.` — No test can verify "good." This belongs in a design rationale section, not requirements.
- **Relative threshold with no anchor.** `MUST have adequate touch target size.` — "Adequate" is unmeasurable. A conformant version: `MUST have a touch target of at least 44×44pt on iOS and 48×48dp on Android.`
- **Missing RFC keyword.** `The button changes to a loading state after the user taps it.` — This reads as a description, not a requirement. A developer reading it cannot know if deviation is acceptable. It MUST include MUST or SHOULD.
- **Compound requirement.** `MUST display the error message and log it to the analytics service and disable the submit button.` — This bundles three independently testable behaviors. Each MUST be a separate requirement.
- **Keyword used with wrong semantics.** `MUST try to validate input before submission.` — "Must try" implies effort, not outcome. If validation is required, the requirement MUST describe the required outcome, not the attempt.

