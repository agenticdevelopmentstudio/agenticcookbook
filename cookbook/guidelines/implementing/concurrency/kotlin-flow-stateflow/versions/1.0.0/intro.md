
# Kotlin Flow and StateFlow: lifecycle-aware state exposure

`StateFlow` is the durable way to expose observable UI state from a ViewModel: a hot, always-has-a-value flow. The two failure modes are leaking work into the background (non-lifecycle-aware collection) and untestable code (hardcoded dispatchers). This guideline encodes the patterns that avoid both, current as of androidx.lifecycle 2.8+ (2024–2026).

