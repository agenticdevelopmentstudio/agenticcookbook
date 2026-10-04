
- **DO NOT** open a branch and let it diverge from trunk for a week, then attempt a large merge.
- **DO NOT** use a `develop` branch as a staging trunk that periodically merges into `main`; this is GitFlow, not trunk-based development, and reintroduces batched integration.
- **DO NOT** hold finished-but-unreleased code on a branch — merge it disabled behind a flag.
- **DO NOT** disable or bypass required checks to land a merge faster.

