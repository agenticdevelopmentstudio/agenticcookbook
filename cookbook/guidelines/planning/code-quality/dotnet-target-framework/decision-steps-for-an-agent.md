
1. Re-read the support policy reference and confirm today's LTS/STS versions and dates.
2. App or service: set `<TargetFramework>` to the current LTS unless an explicit, documented STS need exists.
3. Library: set `<TargetFrameworks>` to the union of consumer requirements; justify each TFM in a comment.
4. Add or update `global.json` to pin the SDK feature band.
5. Record the chosen version and its end-of-support date in the PR description.

This keeps the choice a small, reversible decision (per [adc.principle.small-reversible-decisions](cookbook:4554e680-aca3-4bb2-bc99-1ac381c428b2)): a TFM bump is a single property edit plus a rebuild.

