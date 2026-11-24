
- Each MUST rule is kept, with no exception: `each-selection-justified-by-diff`, `every-changed-path-accounted-for`, `fail-closed-is-stated`, `reasoning-cites-diff-contents`.
- Each SHOULD rule is kept or its departure is stated: `fail-closed-when-unsure`, `unknown-reach-selects-everything`, `shared-inputs-select-everything`, `select-by-dependency-graph-not-paths-alone`, `diff-against-a-known-good-base`, `select-from-every-changed-file`, `always-select-new-changed-and-failing-tests`, `run-the-full-suite-periodically`, `validate-selection-against-full-runs`, `retrain-a-learned-selector`, `record-why-each-test-was-selected`, `log-each-fallback`, `measure-selection-recall-and-savings`, `path-skipped-required-checks-resolve`.
- Each MAY rule is noted where it was used: `decide-change-by-content`, `batch-affected-runs`, `map-a-separate-postsubmit-group`.

