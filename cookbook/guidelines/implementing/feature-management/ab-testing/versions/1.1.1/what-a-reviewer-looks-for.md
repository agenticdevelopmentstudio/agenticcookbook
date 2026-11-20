
- Experiment evaluation that bypasses the provider interface, or a call site with no default
- Provider code that can throw, or that returns anything but the default on error
- An experiment with no local default, a default other than control with no recorded reason, or a kill switch that does not return everyone to control
- An app with no A/B test variant picker in its debug panel; a debug panel override reachable in release builds; or a production override that is neither authenticated nor signed, is not documented as added attack surface, or is present where none is needed
- Random or per-session assignment that gives a user a different variant on a later visit; a hash input that omits the experiment ID, correlating experiments
- An allocation raise that moves users already assigned, or any other allocation, seed or targeting change in a running experiment that reshuffles users, without sticky assignment first
- Exposure logged at fetch, startup or assignment instead of where the variant is seen
- Experiments with no hypothesis, metric or minimum sample size recorded before launch
- Stop or extend logic driven by interim significance outside a sequential or Bayesian design
- Analysis with no SRM check, no bot filtering, or no per-variant telemetry loss check
- A result reported while a sample ratio mismatch is unexplained
- A surprising result acted on without being investigated as a possible bug
- An experimentation system never validated with A/A tests
- A treatment launched at full traffic with no recorded reason, or with no automatic shutdown or no recorded ramp steps and shutdown threshold
- Analysis that does not segment the effect by day
- Web tests that cloak, use 301 redirects, lack `rel=canonical`, or leave test code behind; client-side tests that flash the original page
- iOS variants that depend on downloaded code that introduces or changes features, are hidden from App Review or undocumented, are not described with specificity in the Notes for Review, or are not accessible for review
- Store-page tests built in-app instead of with the store's tool

