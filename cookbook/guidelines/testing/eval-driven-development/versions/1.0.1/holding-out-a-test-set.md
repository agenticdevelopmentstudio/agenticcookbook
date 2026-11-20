
- **MUST** keep a held-out test set that is not used while iterating on prompts, rubrics, or the judge — otherwise you are tuning to the eval and overstating quality.
- **SHOULD** treat the gold set used for judge calibration and the held-out behavior test set as distinct; do not let one leak into the other.
- **SHOULD** version eval datasets alongside the code so a result is reproducible against a known dataset revision.

