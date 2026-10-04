
- Trunk-based development assumes strong automated checks and a fast CI feedback loop; without them, frequent merges to a shared trunk amplify breakage. Establish green-trunk gating first.
- Heavily regulated contexts may require a release branch for a tagged, audited build. That is a release artifact cut *from* trunk, not a long-lived integration branch — trunk remains the single integration point.

