<!-- leaf: implement-feature-management/ab-testing · source: guidelines/implementing/feature-management/ab-testing.md -->

**Rules** (cite as `implement-feature-management/ab-testing#<slug>`):

- `features-need-experimentation-support-variant-assignment-via` SHOULD — Features that may need experimentation SHOULD support variant assignment via an ExperimentProvider interface …

# A/B testing

Features that may need experimentation SHOULD support variant assignment via an `ExperimentProvider` interface (`variant(key) -> String`). Local default with debug panel override.
