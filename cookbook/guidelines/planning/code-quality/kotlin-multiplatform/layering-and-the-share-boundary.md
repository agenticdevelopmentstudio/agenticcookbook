
- Teams **SHOULD** share the domain and data layers (use cases, repositories, models, networking, serialization) in `commonMain`. KMP has been Stable since November 2023, so this is durable, low-risk reuse.
- The shared module **MUST NOT** depend on platform UI toolkits. Keep platform-idiomatic UI (SwiftUI, Jetpack Compose, web framework) on the consuming side unless a shared-UI decision is made deliberately.
- A shared ViewModel/presentation layer **MAY** be shared when the team accepts coupling presentation state to KMP; treat it as a deliberate scope expansion, not a default.
- Apply boundaries per [adc.principle.manage-complexity-through-boundaries](cookbook:555ad5e1-800f-4848-8c58-6f726bdcb42b): expose narrow interfaces from the shared module so platforms stay swappable.

