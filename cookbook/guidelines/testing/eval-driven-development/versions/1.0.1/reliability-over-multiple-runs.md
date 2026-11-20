
A single passing run proves nothing about probabilistic behavior.

- **MUST** report results across multiple runs of the same input, not one pass.
- **SHOULD** distinguish "succeeds at least once" from "succeeds every time" — these are different product guarantees. Anthropic's eval guidance frames these as `pass@k` (success in at least one of k attempts) and `pass^k` (all k trials succeed); pick the metric that matches your reliability requirement.
- **SHOULD** track the consistency metric over time so regressions in flakiness are visible, not just regressions in best-case quality.

