
- Do not reach for a CSS-in-JS runtime or a JS animation library when an interoperable native CSS feature covers the need.
- Do not escalate specificity or use `!important` to win the cascade — reach for `@layer` instead.
- Do not gate a feature solely on `caniuse` percentages without checking Baseline tier and whether your traffic includes pre-cutoff versions.

