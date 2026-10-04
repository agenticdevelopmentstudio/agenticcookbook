
1. Re-read the support policy reference and confirm today's LTS/STS versions and dates.
2. App or service: set `<TargetFramework>` to the current LTS unless an explicit, documented STS need exists.
3. Library: set `<TargetFrameworks>` to the union of consumer requirements; justify each TFM in a comment.
4. Add or update `global.json` to pin the SDK feature band.
5. Record the chosen version and its end-of-support date in the PR description.

This keeps the choice a small, reversible decision (per `agenticdevelopercookbook://principles/small-reversible-decisions`): a TFM bump is a single property edit plus a rebuild.

