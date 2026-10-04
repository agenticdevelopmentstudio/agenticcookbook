
- Teams **SHOULD** model trust boundaries before building a feature, while the design is still cheap to change.
- Teams **SHOULD** revisit the model whenever the architecture changes — a new external dependency, a new data store, a new trust boundary, or a change in who can reach a flow.
- Keep each session lightweight: a focused diagram and a short threat list per feature beats an exhaustive enterprise-wide model done once. The Manifesto explicitly values "a culture of finding and fixing design issues" over checkbox compliance.
- Threat models **SHOULD** live in version control alongside the design they describe so they evolve with the code and stay reviewable in PRs.

