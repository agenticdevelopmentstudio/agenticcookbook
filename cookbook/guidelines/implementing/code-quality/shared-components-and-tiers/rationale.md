
- `should-place-in-lowest-tier`: Code written one tier too high is invisible to every sibling that will need it next. Moving it down later costs more than placing it right now.
- `must-not-import-from-higher-tier`, `should-invert-upward-dependencies`, `should-extract-shared-part-of-cycle`: This is separation of concerns applied to layers. It limits what a change can break, and lets each tier be understood by itself.
- `should-put-feature-pieces-in-shared-tiers`, `should-split-feature-by-need`: If a feature exists only in app code, no other app can use it, and the next app will rebuild it.
