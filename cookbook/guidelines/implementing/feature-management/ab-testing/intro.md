
# A/B testing

Features that may need experimentation SHOULD support variant assignment via an `ExperimentProvider` interface (for example `variant(key, default) -> String`) that takes a caller-supplied default (control unless a reason is recorded) and returns it on any failure; a debug override for testers is optional in general but required in an app, as the debug panel's A/B test variant picker, and that override is kept out of release builds. Assign variants consistently and independently, by a deterministic hash of user and experiment, log the exposure where the variant is actually seen, fix the metric and sample size before starting, and do not trust a result until its sample ratio, data quality and novelty have been checked. On the web and in app stores, follow the platform's rules for tests.

