
A model-based grader **MUST NOT** be allowed to gate (block a merge, fail a build, accept a release) until it has been calibrated against a human-labeled gold set.

- **MUST** assemble a human-labeled gold set, run the judge over it, and measure agreement (e.g., divergence rate or correlation) before trusting the judge.
- **MUST** re-calibrate when the judge prompt, the judge model, or the rubric changes.
- **SHOULD** instruct the judge to return "Unknown" or abstain when it lacks evidence, rather than guessing.
- **SHOULD** periodically read raw transcripts and grades; a passing aggregate score can hide a judge that is rejecting valid answers or rubber-stamping bad ones.

