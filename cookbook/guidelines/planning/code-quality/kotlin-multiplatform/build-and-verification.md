
- The shared module **SHOULD** have its own `commonTest` suite covering domain/data logic once, plus minimal per-target tests for `actual` implementations.
- Run platform builds in CI for every target the project ships; a green Android build does not prove the iOS framework links.

