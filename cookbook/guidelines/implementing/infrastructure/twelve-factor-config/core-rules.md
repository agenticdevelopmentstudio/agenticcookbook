
- Config that varies between deploys **MUST** be read from environment variables (or a runtime secrets/config service), never hardcoded in source.
- You **MUST** build one immutable artifact and promote that same image across environments. Do **NOT** rebuild per environment — rebuilding breaks the dev/prod parity guarantee.
- Secrets **MUST NOT** be committed to version control. A litmus test: the repo could be made open-source at any moment without leaking credentials.
- Config **SHOULD** be grouped by deploy (the running instance), not bucketed into named groups like `config/dev`, `config/staging`, `config/prod` checked into the repo. Named buckets do not scale to new deploys and tempt per-environment code paths.
- Behavior **MUST** be explicit: read each variable by name and fail fast at startup when a required value is missing or malformed (see explicit-over-implicit). Do **NOT** silently fall back to a default for required secrets.

