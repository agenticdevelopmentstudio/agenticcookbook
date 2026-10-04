
- Defer the framework choice no later than the first UI module; defer the deployment choice no later than the first identity-gated feature. Both are costly to change once code depends on them (`agenticdevelopercookbook://principles/small-reversible-decisions`).
- When requirements are uncertain, agents **SHOULD** prefer packaged MSIX — adding identity-gated features later is free, removing the identity assumption is not.

