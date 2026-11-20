
Use STRIDE to drive question 2 systematically. Apply each category to elements touching a trust boundary:

| Category | Threat | Property violated |
|----------|--------|-------------------|
| **S**poofing | Impersonating a user or component | Authentication |
| **T**ampering | Unauthorized modification of data/code | Integrity |
| **R**epudiation | Denying an action without traceable proof | Non-repudiation |
| **I**nformation disclosure | Exposing data to the wrong party | Confidentiality |
| **D**enial of service | Degrading or removing availability | Availability |
| **E**levation of privilege | Gaining capabilities beyond grant | Authorization |

- The team **MUST** consider every STRIDE category for each flow crossing a trust boundary, even if the conclusion is "not applicable."
- Each identified threat **SHOULD** map to a concrete control documented in the relevant feature plan, and the control's guideline (e.g. authentication, privacy) **SHOULD** be linked from the model.

