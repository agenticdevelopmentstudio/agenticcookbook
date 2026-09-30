<!-- leaf: plan-security/threat-modeling · source: guidelines/planning/security/threat-modeling.md -->

**Rules** (cite as `plan-security/threat-modeling#<slug>`):

- `teams-answer-four-questions-producing` MUST — Teams MUST answer all four questions; producing a DFD without enumerating threats and responses is not threat modeling.
- `enumerated-threat-record-explicit-response-accept` MUST — Each enumerated threat MUST record an explicit response; "accept" is valid but MUST be documented with a rationale and …
- `team-consider-stride-category-flow` MUST — The team MUST consider every STRIDE category for each flow crossing a trust boundary, even if the conclusion is "not …
- `identified-threat-map-concrete-control-documented` SHOULD — Each identified threat SHOULD map to a concrete control documented in the relevant feature plan, and the control's …
- `teams-model-trust-boundaries-before` SHOULD — Teams SHOULD model trust boundaries before building a feature, while the design is still cheap to change.
- `teams-revisit-model-whenever-architecture` SHOULD — Teams SHOULD revisit the model whenever the architecture changes — a new external dependency, a new data store, a new …
- `threat-models-live-version-control-alongside` SHOULD — Threat models SHOULD live in version control alongside the design they describe so they evolve with the code and stay …

# Threat modeling

Threat modeling is a design activity that ties point controls (auth, TLS, input validation) to a documented reason. It answers *why* a control exists before code is written, and is most useful when run as a lightweight, recurring habit rather than a one-time gate.

## The four questions

Anchor every modeling session on the four questions from the Threat Modeling Manifesto (threatmodelingmanifesto.org):

1. **What are we building?** — Diagram the system as a data-flow diagram (DFD): processes, data stores, external entities, and the flows between them. Mark **trust boundaries** where data crosses a privilege or ownership change (network edge, process boundary, tenant boundary, untrusted input).
2. **What can go wrong?** — Enumerate threats against each element and flow that crosses a trust boundary.
3. **What are we going to do about it?** — Decide a response per threat: mitigate, eliminate, transfer, or knowingly accept.
4. **Did we do a good enough job?** — Validate the model against the built system and the decisions made.

- Teams **MUST** answer all four questions; producing a DFD without enumerating threats and responses is not threat modeling.
- Each enumerated threat **MUST** record an explicit response; "accept" is valid but **MUST** be documented with a rationale and owner.

## STRIDE enumeration

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

## Make it continuous (shift-left)

- Teams **SHOULD** model trust boundaries before building a feature, while the design is still cheap to change.
- Teams **SHOULD** revisit the model whenever the architecture changes — a new external dependency, a new data store, a new trust boundary, or a change in who can reach a flow.
- Keep each session lightweight: a focused diagram and a short threat list per feature beats an exhaustive enterprise-wide model done once. The Manifesto explicitly values "a culture of finding and fixing design issues" over checkbox compliance.
- Threat models **SHOULD** live in version control alongside the design they describe so they evolve with the code and stay reviewable in PRs.

## Anti-patterns

- **One-time gate**: a single pre-launch review that is never revisited. Architecture drifts and the model goes stale.
- **Controls without threats**: adding TLS or input validation because a checklist says so, with no recorded threat they address. The control cannot be reasoned about or removed safely.
- **Boundary blindness**: enumerating threats on internal flows while ignoring the actual trust boundary (the network edge, the untrusted client, the multi-tenant split).
- **Tool worship**: assuming a diagramming or scanning tool *is* the threat model. The four questions and recorded decisions are the artifact; tools only assist.
