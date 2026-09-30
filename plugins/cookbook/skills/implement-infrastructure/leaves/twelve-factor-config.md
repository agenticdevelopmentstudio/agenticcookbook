<!-- leaf: implement-infrastructure/twelve-factor-config · source: guidelines/implementing/infrastructure/twelve-factor-config.md -->

**Rules** (cite as `implement-infrastructure/twelve-factor-config#<slug>`):

- `endpoints-feature-toggles-read-from-environment-same` MUST — Strictly separate configuration from code. Everything that varies between deploys — credentials, service endpoints, and …
- `fixed-business-rules-live-code` SHOULD — It is NOT internal application constants that stay the same across deploys (routing tables, fixed business rules). …
- `varies-between-deploys-read-from-environment-variables` MUST — Config that varies between deploys MUST be read from environment variables (or a runtime secrets/config service), never …
- `you-build-one-immutable-artifact` MUST — You MUST build one immutable artifact and promote that same image across environments. Do NOT rebuild per environment — …
- `secrets-not-committed-version-control-litmus` MUST — Secrets MUST NOT be committed to version control. A litmus test: the repo could be made open-source at any moment …
- `config-grouped-deploy-running-instance` SHOULD — Config SHOULD be grouped by deploy (the running instance), not bucketed into named groups like config/dev, …
- `behavior-explicit-read-variable-name` MUST — Behavior MUST be explicit: read each variable by name and fail fast at startup when a required value is missing or …

# Twelve-factor configuration

Strictly separate configuration from code. Everything that varies between deploys — credentials, service endpoints, and feature toggles — **MUST** be read from the environment, and the same build artifact **MUST** run unchanged in every environment.

## What counts as config

Config is everything likely to differ between deploys (staging, production, developer machines), per the 12-Factor "config" factor.

- Resource handles to backing services (database URLs, cache hosts, queue endpoints).
- Credentials and secrets for external services.
- Per-deploy values such as the canonical hostname, region, or feature toggles.

It is **NOT** internal application constants that stay the same across deploys (routing tables, fixed business rules). Those **SHOULD** live in code.

## Core rules

- Config that varies between deploys **MUST** be read from environment variables (or a runtime secrets/config service), never hardcoded in source.
- You **MUST** build one immutable artifact and promote that same image across environments. Do **NOT** rebuild per environment — rebuilding breaks the dev/prod parity guarantee.
- Secrets **MUST NOT** be committed to version control. A litmus test: the repo could be made open-source at any moment without leaking credentials.
- Config **SHOULD** be grouped by deploy (the running instance), not bucketed into named groups like `config/dev`, `config/staging`, `config/prod` checked into the repo. Named buckets do not scale to new deploys and tempt per-environment code paths.
- Behavior **MUST** be explicit: read each variable by name and fail fast at startup when a required value is missing or malformed (see explicit-over-implicit). Do **NOT** silently fall back to a default for required secrets.

## Practical patterns

- Provide a `.env.example` (committed, no real values) listing every variable the app reads; keep the real `.env` git-ignored and out of images.
- Validate and coerce config once at boot into a typed config object; the rest of the code reads that object, not `process.env`/`os.environ` directly.
- Inject secrets at runtime from a managed secret store (cloud secret manager, orchestrator secret, or vault) rather than baking them into the artifact. Treat the choice of a heavyweight secrets platform as adopt-when-measured-need-justifies, not a default (YAGNI) — start with environment injection.

## Forecast note

The 12-Factor methodology is being revisited as a community "beyond 12-factor" update; the original `config` factor remains durable. Treat any newer factor revisions as forecasts until officially published, and pin to the current published guidance at https://12factor.net/config.

## Privacy note

Handling credentials and personal data as config has legal implications. This is engineering guidance and is **NOT** legal advice; consult counsel for regulatory obligations.
