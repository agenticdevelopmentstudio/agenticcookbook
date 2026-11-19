# Research: ab-testing

Researched 2026-11-16 at base commit `2071c94`. Machine-readable record: `research.json`.

**Summary.** Both existing rules hold. A variant-by-key evaluation interface is the common shape (OpenFeature, LaunchDarkly, GrowthBook, Azure), but every standard and SDK makes the caller pass a default value and never throws; control is the abort/kill-switch state; forced variants for QA are a standard property of experimentation systems and dev tooling should be off in production. The topic is missing the implementer's core duties: deterministic hash of user+experiment ID with stable assignment through ramp-ups, exposure logged where the variant is actually seen, pre-registered metric and minimum sample size, no peeking, an SRM check on every experiment, A/A tests, ramp-up with auto-abort, data-quality guards (client telemetry loss, bots, Twyman's law), novelty effects, web flicker, Google Search rules (no cloaking, 302, canonical, end tests), Apple's rules (variants in the reviewed binary, described in review notes, no downloaded code) and store-page tests through Apple product page optimization and Google Play store listing experiments.

**Verdicts.**

- **experiment-provider-interface**: supported (`openfeature-typed-evaluation-with-default`, `openfeature-variant-field`, `azure-variant-flags`, `sdks-take-call-site-default`)
- **local-default-with-debug-override**: supported (`control-is-the-abort-state`, `azure-kill-switch-default-variant`, `forced-variants-for-qa`, `dev-override-off-in-production`)
- **deterministic-hash-assignment**: new (`hash-user-and-experiment-id`, `consistent-assignment-across-visits`, `no-correlation-between-experiments`, `optimizely-murmurhash-bucketing`, `launchdarkly-recomputes-assignment`, `growthbook-hash-and-tracking-callback`)
- **stable-assignment-when-allocation-changes**: new (`monotonic-ramp-up-keeps-assignments`, `reallocation-reshuffles-users`, `sticky-bucketing-persists-assignment`)
- **evaluation-never-fails-returns-default**: new (`evaluation-returns-default-on-error`, `sdks-take-call-site-default`)
- **log-exposure-at-point-of-use**: new (`log-exposure-when-variant-is-seen`, `launchdarkly-variation-records-exposure`, `statsig-disable-exposure-logging`, `growthbook-hash-and-tracking-callback`, `firebase-activation-event`, `assignment-without-exposure-dilutes`, `openfeature-tracking-api`)
- **pre-register-metric-and-sample-size**: new (`pre-register-hypothesis-and-metrics`, `compute-minimum-sample-size`, `underpowered-experiments-common-mistake`)
- **no-peeking**: new (`peeking-inflates-false-positives`, `stopping-or-extending-is-common-mistake`)
- **check-sample-ratio-mismatch**: new (`check-sample-ratio-mismatch`, `srm-invalidates-results`, `srm-is-common`)
- **validate-with-aa-tests**: new (`run-aa-tests`)
- **ramp-up-with-auto-abort**: new (`ramp-up-and-auto-abort`)
- **guard-data-quality**: new (`client-telemetry-loss-biases-results`, `robots-skew-results`, `twymans-law`)
- **watch-novelty-effects**: new (`novelty-and-primacy-effects`)
- **avoid-web-flicker**: new (`web-flicker`)
- **web-tests-follow-search-guidance**: new (`google-search-no-cloaking`, `google-search-302-and-canonical`, `google-search-end-tests-promptly`)
- **app-variants-ship-in-reviewed-binary**: new (`apple-review-notes-describe-changes`, `apple-no-hidden-features`, `apple-no-downloaded-code`)
- **store-page-tests-use-store-tools**: new (`apple-product-page-optimization`, `google-play-store-listing-experiments`)

**Open questions.**

- Whether the interface should return a variant name (String) or a typed value: OpenFeature returns typed values and exposes the variant name only in evaluation details; the owner decides which the rule names.
- Whether Apple App Review treats server-switched UI variants already in the binary as 'hidden features' under 2.5.19: no Apple text addresses A/B tests inside apps directly.
- Cross-device stickiness: the sources establish stickiness only for the same user identifier; no primary source establishes a general mechanism across anonymous devices.

**Limitations.**

- Windows desktop (Microsoft Store) has no fetched first-party A/B guidance; Microsoft coverage is Azure App Configuration and Microsoft ExP research.
- Several vendor quotes (Optimizely bucketing, Firebase, Play, Statsig, LaunchDarkly) came through a fetch summariser that returns quoted sentences rather than whole pages; trust scores account for this.
- Statsig's FAQ on one-sided manual exposure imbalance returned 404 and is not cited; Optimizely forced-decision pages redirected and are not cited.
- Kohavi et al.'s book 'Trustworthy Online Controlled Experiments' (2020) was not accessible; its authors' peer-reviewed papers stand in for it.
- Evan Miller's article and the Statsig blog are secondary sources, used only where corroborated.

## Best practices

- Assign variants by hashing the user identifier together with the experiment identifier and partitioning the hash range among variants, so assignment needs no stored state. (claim: `hash-user-and-experiment-id`, trust 86, multi-independent)
  > A hash function is applied to the combination of the user identifier and the experiment identifier (e.g. by concatenating them together) to obtain an integer that is uniformly distributed on a range of values. The range is then partitioned, with each variant represented by a partition.
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf); [How bucketing works (Feature Experimentation)](https://docs.optimizely.com/feature-experimentation/docs/how-bucketing-works); [Experiment traffic assignment](https://launchdarkly.com/docs/home/experimentation/traffic-assignment)
- A user must get the same variant on every visit for the length of the experiment. (claim: `consistent-assignment-across-visits`, trust 86, multi-independent)
  > Repeat assignments of a single end user must be consistent; the end user should be assigned to the same variant on each successive visit to the site.
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf); [Product page optimization](https://developer.apple.com/app-store/product-page-optimization/); [How bucketing works (Feature Experimentation)](https://docs.optimizely.com/feature-experimentation/docs/how-bucketing-works)
- Assignment in one experiment must be independent of assignment in any other concurrent experiment, which is why the experiment identifier is part of the hash input and the hash function must be sound. (claim: `no-correlation-between-experiments`, trust 72, single)
  > When multiple experiments are run, there must be no correlation between experiments. An end user's assignment to a variant in one experiment must have no effect on the probability of being assigned to a variant in any other experiment.
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf)
- Raising a treatment's percentage should add new users without moving users already assigned. (claim: `monotonic-ramp-up-keeps-assignments`, trust 82, multi-independent)
  > The algorithm may support monotonic ramp-up, meaning that the percentage of users who see a Treatment can be slowly increased without changing the assignments of users who were previously assigned to that Treatment.
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf); [Experiment traffic assignment](https://launchdarkly.com/docs/home/experimentation/traffic-assignment)
- Reducing and re-raising allocation, or changing the bucketing seed or rule configuration, can reassign users to other variants and cause a sample ratio mismatch; persist assignments if the configuration must change mid-test. (claim: `reallocation-reshuffles-users`, trust 76, multi-independent)
  > Optimizely resets the bucket ranges and users may be reassigned to different variations. This can cause a sample ratio mismatch and invalidate your experiment results.
  Sources: [How bucketing works (Feature Experimentation)](https://docs.optimizely.com/feature-experimentation/docs/how-bucketing-works); [Experiment traffic assignment](https://launchdarkly.com/docs/home/experimentation/traffic-assignment)
- Platforms offer persisted ('sticky') assignment so a user keeps a variant when targeting, allocation or login state change. (claim: `sticky-bucketing-persists-assignment`, trust 70, multi-independent)
  > Sticky bucketing ensures that users see the same experiment variant
  Sources: [GrowthBook JavaScript SDK](https://docs.growthbook.io/lib/js); [How bucketing works (Feature Experimentation)](https://docs.optimizely.com/feature-experimentation/docs/how-bucketing-works)
- Record the exposure at the moment the user first encounters the varied experience, and analyse only exposed users; assignment alone is not exposure. (claim: `log-exposure-when-variant-is-seen`, trust 84, multi-independent)
  > Event-triggered filtering is implemented by tracking the time at which each user first saw content that was affected by the experiment. This data can be collected directly (by recording an event when a user sees experimental content)
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf); [Node Core server SDK](https://docs.statsig.com/api/content/server-core/node-core); [Create Firebase Remote Config experiments with A/B Testing](https://firebase.google.com/docs/ab-testing/abtest-config)
- Control is the safe state: when a variant misbehaves the experiment is stopped and everyone gets control. (claim: `control-is-the-abort-state`, trust 84, multi-independent)
  > In case of a bug, for example, the experiment is aborted and all users should see the Control variant.
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf); [Use variant feature flags - Azure App Configuration](https://learn.microsoft.com/en-us/azure/azure-app-configuration/howto-variant-feature-flags)
- Flag/variant evaluation must never throw and must return the caller-supplied default on any failure. (claim: `evaluation-returns-default-on-error`, trust 80, single)
  > Methods, functions, or operations on the client **MUST NOT** throw exceptions, or otherwise abnormally terminate. Flag evaluation calls must always return the `default value` in the event of abnormal execution.
  Sources: [OpenFeature Specification, 1. Flag Evaluation API](https://raw.githubusercontent.com/open-feature/spec/main/specification/sections/01-flag-evaluation.md)
- Define the hypothesis and the metrics that will judge it before the experiment starts; platforms make the goal metric a creation-time choice. (claim: `pre-register-hypothesis-and-metrics`, trust 80, multi-independent)
  > The hypothesis should also include a set of metrics to measure the impact of the change introduced on the product.
  Sources: [Patterns of Trustworthy Experimentation: Pre-Experiment Stage](https://www.microsoft.com/en-us/research/?p=680556); [Create Firebase Remote Config experiments with A/B Testing](https://firebase.google.com/docs/ab-testing/abtest-config)
- Before starting, choose power and the effect to detect, estimate variance, and compute the minimum sample size and hence run time. (claim: `compute-minimum-sample-size`, trust 87, multi-independent)
  > Decide on the statistical power, the effect you would like to detect, and estimate the variability of the OEC through an A/A test. Based on this data you can compute the minimum sample size needed for the experiment and hence the running time for your web site.
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf); [A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments (KDD '17)](https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf); [Patterns of Trustworthy Experimentation: Pre-Experiment Stage](https://www.microsoft.com/en-us/research/?p=680556)
- Every experiment's analysis should test the observed split against the configured split (chi-square) and flag a sample ratio mismatch. (claim: `check-sample-ratio-mismatch`, trust 88, multi-independent)
  > If the actual ratio is different than the expected (a chi-square test can be used), it means something is wrong with the sampling process. We call this situation Sample Ratio Mismatch (SRM).
  Sources: [A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments (KDD '17)](https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf); [Diagnosing Sample Ratio Mismatch in Online Controlled Experiments: A Taxonomy and Rules of Thumb for Practitioners (KDD '19)](https://exp-platform.com/Documents/2019_KDDFabijanGupchupFuptaOmhoverVermeerDmitriev.pdf); [Diagnosing Sample Ratio Mismatch in A/B Testing](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)
- Run A/A tests to validate the split, data fidelity and false-positive rate of the experimentation system itself. (claim: `run-aa-tests`, trust 76, multi-independent)
  > Run A/A tests (see Sect. 3.1) and validate the following. 1. Are users split according to the planned percentages? 2. Is the data collected matching the system of record? 3. Are the results showing non-significant results 95% of the time?
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf); [Patterns of Trustworthy Experimentation: Pre-Experiment Stage](https://www.microsoft.com/en-us/research/?p=680556)
- Start a treatment on a small percentage, ramp it up in steps, and stop a treatment automatically if it significantly underperforms control. (claim: `ramp-up-and-auto-abort`, trust 80, multi-independent)
  > An experimentation system that analyses the experiment data in near-real-time can automatically shut-down a Treatment if it is significantly underperforming relative to the Control.
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf); [A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments (KDD '17)](https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf)

## Known solutions

- The vendor-neutral evaluation API (OpenFeature) evaluates a flag by key through typed methods, string included, and every call takes a required default value. (claim: `openfeature-typed-evaluation-with-default`, trust 85, single)
  > The `client` **MUST** provide methods for typed flag evaluation, including boolean, numeric, string, and structure, with parameters `flag key` (string, required), `default value` (boolean | number | string | structure, required), `evaluation context` (optional), and `evaluation options` (optional), which returns the flag value.
  Sources: [OpenFeature Specification, 1. Flag Evaluation API](https://raw.githubusercontent.com/open-feature/spec/main/specification/sections/01-flag-evaluation.md)
- OpenFeature's detailed evaluation reports the variant name the provider resolved, alongside the value. (claim: `openfeature-variant-field`, trust 82, single)
  > In cases of normal execution, the `evaluation details` structure's `variant` field **MUST** contain the value of the `variant` field in the `flag resolution` structure returned by the configured `provider`, if the field is set.
  Sources: [OpenFeature Specification, 1. Flag Evaluation API](https://raw.githubusercontent.com/open-feature/spec/main/specification/sections/01-flag-evaluation.md)
- OpenFeature adds an experimental tracking API to tie flag evaluations to later user actions for experimentation. (claim: `openfeature-tracking-api`, trust 65, single)
  > The `tracking API` enables the association of feature flag evaluations with subsequent actions or application states, in order to facilitate experimentation and analysis of the impact of feature flags on business objectives.
  Sources: [OpenFeature Specification, 6. Tracking](https://raw.githubusercontent.com/open-feature/spec/main/specification/sections/06-tracking.md)
- Commercial SDKs share the evaluate-by-key-with-a-fallback shape: the caller supplies the default at each call site. (claim: `sdks-take-call-site-default`, trust 80, multi-independent)
  > return a typed value with a per-call-site default
  Sources: [Experimentation (SDK features)](https://launchdarkly.com/docs/sdk/features/experimentation); [GrowthBook JavaScript SDK](https://docs.growthbook.io/lib/js); [OpenFeature Specification, 1. Flag Evaluation API](https://raw.githubusercontent.com/open-feature/spec/main/specification/sections/01-flag-evaluation.md)
- In LaunchDarkly, calling the variation method is what records the exposure; metrics come from separate track calls. (claim: `launchdarkly-variation-records-exposure`, trust 72, single)
  > Variation methods also record an exposure event so LaunchDarkly knows this context was part of the experiment.
  Sources: [Experimentation (SDK features)](https://launchdarkly.com/docs/sdk/features/experimentation)
- LaunchDarkly stores no assignment record; it recomputes the bucket from seed and context key on every evaluation. (claim: `launchdarkly-recomputes-assignment`, trust 72, single)
  > LaunchDarkly does not need to store a record of which variation each context received
  Sources: [Experiment traffic assignment](https://launchdarkly.com/docs/home/experimentation/traffic-assignment)
- GrowthBook assigns by deterministic hashing and fires a tracking callback when evaluation enrolls the user, which the app wires to its analytics. (claim: `growthbook-hash-and-tracking-callback`, trust 72, single)
  > Evaluating the feature is what enrolls a user and fires `trackingCallback`.
  Sources: [GrowthBook JavaScript SDK](https://docs.growthbook.io/lib/js)
- Statsig logs exposure on evaluation by default and lets a call disable it, so the app can log the exposure manually later. (claim: `statsig-disable-exposure-logging`, trust 70, single)
  > When set to `true`, the SDK doesn't automatically log an exposure.
  Sources: [Node Core server SDK](https://docs.statsig.com/api/content/server-core/node-core)
- Optimizely buckets with MurmurHash over user ID and experiment ID. (claim: `optimizely-murmurhash-bucketing`, trust 68, single)
  > The SDK uses the MurmurHash function to hash the user ID and experiment ID into an integer.
  Sources: [How bucketing works (Feature Experimentation)](https://docs.optimizely.com/feature-experimentation/docs/how-bucketing-works)
- Azure App Configuration models experiments as variant feature flags: named variants with optional configuration values, percentile allocation, and user/group overrides. (claim: `azure-variant-flags`, trust 80, single)
  > A variant is defined with a *Name* and an optional *Configuration Value*.
  Sources: [Use variant feature flags - Azure App Configuration](https://learn.microsoft.com/en-us/azure/azure-app-configuration/howto-variant-feature-flags)
- Experimentation systems let testers force a user or device into a chosen variant, bypassing allocation, to test each variant. (claim: `forced-variants-for-qa`, trust 82, multi-independent)
  > The algorithm may support external control, meaning that users can be manually forced into and out of variants. This property makes it easier to test the experimental site.
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf); [Use variant feature flags - Azure App Configuration](https://learn.microsoft.com/en-us/azure/azure-app-configuration/howto-variant-feature-flags); [Create Firebase Remote Config experiments with A/B Testing](https://firebase.google.com/docs/ab-testing/abtest-config)
- Developer override tooling should be disabled in production builds so internal flags and experiments are not exposed. (claim: `dev-override-off-in-production`, trust 58, single)
  > To avoid exposing all of your internal feature flags and experiments to users
  Sources: [GrowthBook JavaScript SDK](https://docs.growthbook.io/lib/js)

## Platform guidelines

- Web A/B tests must not serve Googlebot different URLs or content than humans (cloaking). (claim: `google-search-no-cloaking`, trust 90, single)
  > Don't show one set of URLs to Googlebot, and a different set to humans.
  Sources: [Minimize A/B testing impact in Google Search](https://developers.google.com/search/docs/crawling-indexing/website-testing)
- When a web test redirects to or serves alternate URLs, use 302 (temporary) redirects and rel=canonical on the alternates pointing to the original. (claim: `google-search-302-and-canonical`, trust 90, single)
  > use a 302 (temporary) redirect, not a 301 (permanent) redirect.
  Sources: [Minimize A/B testing impact in Google Search](https://developers.google.com/search/docs/crawling-indexing/website-testing)
- Run a web test only as long as needed and remove its code afterwards. (claim: `google-search-end-tests-promptly`, trust 85, single)
  > Run the experiment only as long as necessary
  Sources: [Minimize A/B testing impact in Google Search](https://developers.google.com/search/docs/crawling-indexing/website-testing)
- Apple's sanctioned A/B test surface for App Store pages is product page optimization: up to three treatments of icon, screenshots and previews, metadata approved by App Review, icons shipped in the binary, up to 90 days. (claim: `apple-product-page-optimization`, trust 85, single)
  > Before you can publish your test, any new metadata that you'd like to include in your treatments must be approved by App Review.
  Sources: [Product page optimization](https://developer.apple.com/app-store/product-page-optimization/)
- Apple requires every new feature and product change to be described specifically in the review notes and be accessible for review, which covers in-app variants. (claim: `apple-review-notes-describe-changes`, trust 74, single)
  > All new features, functionality, and product changes must be described with specificity in the Notes for Review section of App Store Connect (generic descriptions will be rejected) and accessible for review.
  Sources: [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- Apple forbids hidden, dormant or undocumented features, so variants must be visible to App Review, not concealed. (claim: `apple-no-hidden-features`, trust 72, single)
  > Don't include any hidden, dormant, or undocumented features in your app; your app's functionality should be clear to end users and App Review.
  Sources: [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- On iOS, variants must ship in the reviewed binary and be selected by configuration; downloading code that changes functionality is not allowed. (claim: `apple-no-downloaded-code`, trust 78, single)
  > nor may they download, install, or execute code which introduces or changes features or functionality of the app
  Sources: [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- Google Play offers store listing experiments for icon, feature graphic, screenshots and (localized) descriptions, with configurable confidence level and minimum detectable effect. (claim: `google-play-store-listing-experiments`, trust 80, single)
  > You can include variants of your app's icon, feature graphic, and screenshots.
  Sources: [Run A/B tests on your store listing (store listing experiments)](https://support.google.com/googleplay/android-developer/answer/6227309)
- Firebase A/B Testing counts only users who trigger the configured activation event, so the event must fire where the variant is used. (claim: `firebase-activation-event`, trust 80, single)
  > only those who trigger an activation event will be included in your experiment results.
  Sources: [Create Firebase Remote Config experiments with A/B Testing](https://firebase.google.com/docs/ab-testing/abtest-config)
- Azure variant flags define a DefaultWhenDisabled variant everyone gets when the flag is disabled (kill switch), and a DefaultWhenEnabled variant for unallocated users. (claim: `azure-kill-switch-default-variant`, trust 80, single)
  > All users now are given the **DefaultWhenDisabled** variant, regardless of which percentiles or overridden users/groups they were a part of.
  Sources: [Use variant feature flags - Azure App Configuration](https://learn.microsoft.com/en-us/azure/azure-app-configuration/howto-variant-feature-flags)

## The expert's view

- Repeatedly checking significance and stopping when it is reached inflates false positives; fix the sample size in advance or use a sequential or Bayesian design. (claim: `peeking-inflates-false-positives`, trust 85, multi-independent)
  > Repeated significance testing always increases the rate of false positives
  Sources: [How Not To Run An A/B Test](https://www.evanmiller.org/how-not-to-run-an-ab-test.html); [A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments (KDD '17)](https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf)
- Microsoft's experimenters report that stopping early or extending experiments are very common mistakes. (claim: `stopping-or-extending-is-common-mistake`, trust 72, single)
  > In our experience, stopping early or extending the experiment are both very common mistakes experiment owners make.
  Sources: [A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments (KDD '17)](https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf)
- A sample ratio mismatch usually means the results cannot be trusted until its cause is found. (claim: `srm-invalidates-results`, trust 88, multi-independent)
  > Sample Ratio Mismatch in most cases completely invalidates experiment results.
  Sources: [Diagnosing Sample Ratio Mismatch in Online Controlled Experiments: A Taxonomy and Rules of Thumb for Practitioners (KDD '19)](https://exp-platform.com/Documents/2019_KDDFabijanGupchupFuptaOmhoverVermeerDmitriev.pdf); [A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments (KDD '17)](https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf); [Diagnosing Sample Ratio Mismatch in A/B Testing](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)
- SRMs are not rare: about 6% of A/B tests at Microsoft had one. (claim: `srm-is-common`, trust 65, single)
  > about 6% of A/B tests have an SRM
  Sources: [Diagnosing Sample Ratio Mismatch in A/B Testing](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)
- Users assigned but never exposed behave like control and dilute the measured effect; tag the exposure point accurately. (claim: `assignment-without-exposure-dilutes`, trust 76, multi-independent)
  > not everyone assigned to the test group may actually be exposed to the test version
  Sources: [When allocation point and exposure point differ](https://statsig.com/blog/when-allocation-point-and-exposure-point-differ); [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf)
- Short-term effects can fade (novelty) or grow (primacy); segment the effect by day and consider longer runs before trusting a lift. (claim: `novelty-and-primacy-effects`, trust 70, single)
  > the change appeared positive in the short period but it was flat in the long term. This is a novelty effect.
  Sources: [A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments (KDD '17)](https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf)
- Client-side web tests can flash the original page before the variant renders; apply visual changes early (synchronously, via CSS). (claim: `web-flicker`, trust 62, single)
  > when the original page appears briefly before your variation.
  Sources: [Fix flashing or flickering variation content (Web Experimentation)](https://docs.optimizely.com/web-experimentation/docs/6P2o-fix-flashing-or-flickering-variation-content)
- Mobile client telemetry is lossy and a variant can change the loss rate, biasing results; measure event loss per variant. (claim: `client-telemetry-loss-biases-results`, trust 72, single)
  > An unavoidable aspect of analyzing mobile app experiments is that a substantial fraction of telemetry coming from mobile clients gets lost.
  Sources: [A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments (KDD '17)](https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf)
- Bots can skew experiment metrics enough to invalidate tests and should be filtered. (claim: `robots-skew-results`, trust 72, multi-independent)
  > Robots can introduce significant skew into estimates, enough to render assumptions invalid.
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf); [Diagnosing Sample Ratio Mismatch in A/B Testing](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)
- Surprising results, positive or negative, usually signal a bug and should be investigated before shipping. (claim: `twymans-law`, trust 66, single)
  > any unexpected metric movement, positive or negative, usually means there is an issue.
  Sources: [A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments (KDD '17)](https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf)
- Running underpowered experiments is a common mistake. (claim: `underpowered-experiments-common-mistake`, trust 82, multi-independent)
  > A common mistake is to run experiments that are underpowered.
  Sources: [Controlled Experiments on the Web: Survey and Practical Guide (Data Mining and Knowledge Discovery 18(1):140-181)](https://exp-platform.com/Documents/controlledExperimentDMKD.pdf); [A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments (KDD '17)](https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf)
