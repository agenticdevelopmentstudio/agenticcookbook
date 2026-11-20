
- `should-model-recoverable-outcomes-as-values`: an expected, recoverable outcome (not-found, validation-failed, conflict) signalled by a throw instead of a returned value
- `should-reserve-exceptions-for-unrecoverable`: an exception or panic for a condition the caller could recover from
- `should-put-the-failure-in-the-signature`: a function that can fail whose return type does not say so
- `should-keep-boundary-policy-consistent-per-layer`: two failure-representation policies mixed within one layer
- `must-not-swallow-failures`: log-and-continue, a silent `null`, or a default that masks a failure
