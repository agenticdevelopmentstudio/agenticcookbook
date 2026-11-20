
- `should-model-recoverable-outcomes-as-values`: recoverable outcomes are returned as values, or the work says why not
- `should-reserve-exceptions-for-unrecoverable`: exceptions and panics signal only bugs and unrecoverable states, or the work says why not
- `should-put-the-failure-in-the-signature`: every function that can fail says so in its return type, or the work says why not
- `should-keep-boundary-policy-consistent-per-layer`: each layer keeps one boundary policy, or the work says why not
- `must-not-swallow-failures`: every failure is propagated or handled explicitly; none is swallowed
