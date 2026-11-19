
The classic pyramid (many unit, fewer integration, fewest E2E) is a sensible **default**,
not dogma. Some systems fit a different shape: integration-heavy services, I/O-bound code,
or thin-logic UIs often match the "testing trophy" better — more integration tests, with
static analysis and type-checking forming the broad foundational base. Teams SHOULD pick the
test distribution deliberately, per system, based on where the real risk lives, rather than
forcing a fixed ratio.

