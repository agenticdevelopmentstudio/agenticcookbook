
- `should-construct-what-each-test-needs`: a test that uses data built for other tests rather than constructing its own
- `should-avoid-large-shared-fixture-files`: a large fixture file shared across tests
- `should-use-builders-or-factories-for-complex-objects`: a complex object spelled out in full in a test instead of a builder or factory call naming only the fields it cares about
- `should-use-property-based-generators-for-coverage`: input coverage attempted with hand-listed cases where a Hypothesis strategy or fast-check arbitrary would serve
- `should-use-inline-literals-for-simple-cases`: a simple case routed through a builder or fixture instead of an inline literal
- `must-keep-specific-data-visible-in-the-test`: a test whose specific data lives in a magic fixture out of view

