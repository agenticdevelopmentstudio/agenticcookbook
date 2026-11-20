
### Traceability

- **must-trace-requirements-to-source**: Every behavioral requirement in the recipe MUST be traceable to a specific, observable behavior in the source code. Traceability means a reviewer can point to the code path, API response, or test case that demonstrates the behavior.
- **must-not-invent-requirements**: Requirements MUST NOT be invented to fill perceived gaps. If the source code does not implement a behavior, the recipe MUST NOT require it.
- **should-note-indirect-evidence-source**: Where traceability is indirect (e.g., behavior is inferred from a test rather than inspected in production code), the recipe SHOULD note the evidence source in a comment or Design Decisions entry.
- **must-mark-partially-observable-requirements**: Requirements that are partially observable — where some aspect of the behavior cannot be confirmed from the code alone — MUST be marked `NEEDS REVIEW` with an explanation of what cannot be confirmed and why.

### Accurate Representation of Gaps

- **must-not-fabricate-unimplemented-concerns**: If the source code does not implement support for a concern (e.g., accessibility, internationalization, offline handling), the recipe MUST NOT fabricate requirements for that concern.
- **must-mark-unimplemented-sections**: Unimplemented sections MUST be marked with `NEEDS REVIEW: Not implemented in source. Behavior undefined.` This signals to consumers that the recipe is incomplete in a specific way, rather than silently omitting the concern.
- **must-not-mark-implemented-behavior-needs-review**: A recipe MUST NOT mark a section `NEEDS REVIEW` when the behavior is actually implemented and observable. `NEEDS REVIEW` is reserved for genuine gaps in the source, not for sections the author found tedious to analyze.

### Honest Representation of Quirks and Workarounds

- **must-document-workarounds-and-quirks**: If the source code contains a known workaround, a platform-specific hack, or behavior that deviates from what a naive reader would expect, the recipe MUST document it. These deviations MUST appear in a Design Decisions section or as inline notes on the affected requirements.
- **must-not-smooth-over-quirks**: The recipe MUST NOT smooth over quirks by describing the idealized behavior and omitting the actual behavior.
- **must-document-unusual-handling**: If the source code handles a case in an unusual or non-obvious way (e.g., a retry loop that silently drops errors after three attempts), the recipe MUST document that behavior as a requirement or a noted deviation, not omit it.
- **should-note-behavior-affecting-technical-debt**: Technical debt in the source SHOULD be noted in Design Decisions when it affects behavioral correctness.
- **must-not-treat-behavior-affecting-debt-as-optional**: Authors MUST NOT treat documentation of technical debt as optional when the debt affects how implementations must behave.

### Error Handling Accuracy

- **must-document-actual-error-handling**: If the source code silently swallows exceptions, ignores error return codes, or fails to communicate errors to the caller or user, the recipe MUST accurately document this — not describe the error handling the code should have had.
- **must-not-claim-unattempted-error-handling**: A recipe MUST NOT claim `MUST display an error message on failure` when the source code makes no such attempt; such a claim is a source fidelity failure regardless of whether the behavior is desirable.

### No Idealization

- **must-describe-code-as-it-is**: The recipe MUST describe the code as it is, not as the author believes it should be.
- **must-separate-aspirational-behavior**: Aspirational behavior belongs in a separate "Recommended Improvements" section if included at all, and MUST be clearly distinguished from normative requirements.
- **must-not-derive-requirements-from-an-ideal**: Requirements MUST NOT be derived from what "a well-implemented component would do" rather than what the code actually does; such requirements are a source fidelity violation.

