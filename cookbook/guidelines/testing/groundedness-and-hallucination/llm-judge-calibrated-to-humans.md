
- An LLM judge **MAY** score groundedness by seeing only the answer + retrieved chunks and labeling each claim. Keep the judge blind to any gold answer so it scores support, not agreement.
- You **MUST** calibrate the judge against a human-labeled gold set and report agreement (e.g., Cohen's kappa) before trusting its scores. An uncalibrated judge can saturate near 1.0 and hide real failures.
- Frameworks such as RAGAS, DeepEval, and TruLens implement these metrics; their absolute scores diverge on the same data (forecast: still true in 2026), so pin one framework + version and track trends rather than comparing raw cross-tool numbers.

