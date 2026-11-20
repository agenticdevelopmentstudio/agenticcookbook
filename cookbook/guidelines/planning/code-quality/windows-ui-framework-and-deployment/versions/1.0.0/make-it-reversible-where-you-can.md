
- Defer the framework choice no later than the first UI module; defer the deployment choice no later than the first identity-gated feature. Both are costly to change once code depends on them ([adc.principle.small-reversible-decisions](cookbook:4554e680-aca3-4bb2-bc99-1ac381c428b2)).
- When requirements are uncertain, agents **SHOULD** prefer packaged MSIX — adding identity-gated features later is free, removing the identity assumption is not.

