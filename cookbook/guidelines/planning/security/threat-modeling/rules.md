
- **should-anchor-sessions-on-the-four-questions**: You SHOULD anchor every modeling session on the four questions from the Threat Modeling Manifesto (threatmodelingmanifesto.org).
  1. **What are we building?** — Diagram the system as a data-flow diagram (DFD): processes, data stores, external entities, and the flows between them. Mark **trust boundaries** where data crosses a privilege or ownership change (network edge, process boundary, tenant boundary, untrusted input).
  2. **What can go wrong?** — Enumerate threats against each element and flow that crosses a trust boundary.
  3. **What are we going to do about it?** — Decide a response per threat: mitigate, eliminate, transfer, or knowingly accept.
  4. **Did we do a good enough job?** — Validate the model against the built system and the decisions made.
- **must-answer-all-four-questions**: Teams **MUST** answer all four questions; producing a DFD without enumerating threats and responses is not threat modeling.
- **must-record-a-response-per-threat**: Each enumerated threat **MUST** record an explicit response; "accept" is valid but **MUST** be documented with a rationale and owner.
- **should-use-stride-for-question-two**: You SHOULD use STRIDE to drive question 2 systematically, applying each category to elements touching a trust boundary.
- **must-consider-every-stride-category-at-trust-boundaries**: The team **MUST** consider every STRIDE category for each flow crossing a trust boundary, even if the conclusion is "not applicable."
- **should-map-each-threat-to-a-linked-control**: Each identified threat **SHOULD** map to a concrete control documented in the relevant feature plan, and the control's guideline (e.g. authentication, privacy) **SHOULD** be linked from the model.
- **should-model-trust-boundaries-before-building**: Teams **SHOULD** model trust boundaries before building a feature, while the design is still cheap to change.
- **should-revisit-the-model-on-architecture-change**: Teams **SHOULD** revisit the model whenever the architecture changes — a new external dependency, a new data store, a new trust boundary, or a change in who can reach a flow.
- **should-keep-each-session-lightweight**: You SHOULD keep each session lightweight: a focused diagram and a short threat list per feature beats an exhaustive enterprise-wide model done once.
- **should-keep-threat-models-in-version-control**: Threat models **SHOULD** live in version control alongside the design they describe so they evolve with the code and stay reviewable in PRs.
