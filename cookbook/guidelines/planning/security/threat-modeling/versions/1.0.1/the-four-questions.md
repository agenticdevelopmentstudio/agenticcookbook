
Anchor every modeling session on the four questions from the Threat Modeling Manifesto (threatmodelingmanifesto.org):

1. **What are we building?** — Diagram the system as a data-flow diagram (DFD): processes, data stores, external entities, and the flows between them. Mark **trust boundaries** where data crosses a privilege or ownership change (network edge, process boundary, tenant boundary, untrusted input).
2. **What can go wrong?** — Enumerate threats against each element and flow that crosses a trust boundary.
3. **What are we going to do about it?** — Decide a response per threat: mitigate, eliminate, transfer, or knowingly accept.
4. **Did we do a good enough job?** — Validate the model against the built system and the decisions made.

- Teams **MUST** answer all four questions; producing a DFD without enumerating threats and responses is not threat modeling.
- Each enumerated threat **MUST** record an explicit response; "accept" is valid but **MUST** be documented with a rationale and owner.

