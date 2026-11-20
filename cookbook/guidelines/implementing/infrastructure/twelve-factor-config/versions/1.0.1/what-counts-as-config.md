
Config is everything likely to differ between deploys (staging, production, developer machines), per the 12-Factor "config" factor.

- Resource handles to backing services (database URLs, cache hosts, queue endpoints).
- Credentials and secrets for external services.
- Per-deploy values such as the canonical hostname, region, or feature toggles.

It is **NOT** internal application constants that stay the same across deploys (routing tables, fixed business rules). Those **SHOULD** live in code.

