<!-- leaf: test-general/design-time-data · source: guidelines/testing/design-time-data.md -->

**Rules** (cite as `test-general/design-time-data#<slug>`):

- `views-use-datacontext-designinstance-so` SHOULD — Views SHOULD use d:DataContext and d:DesignInstance so the designer renders realistic content, not empty surfaces

# Design-Time Data

Design-time data enables visual preview testing in the XAML designer without running the application — the Windows equivalent of SwiftUI `#Preview` and Compose `@Preview`.

## What to verify

- Views SHOULD use `d:DataContext` and `d:DesignInstance` so the designer renders realistic content, not empty surfaces
- Verify all significant view states are previewable: default, empty, error, loading, populated
- Use XAML Hot Reload for rapid visual iteration during testing
