
- **Room 2.8.4** is the current stable line. Stable Kotlin Multiplatform (KMP) support arrived in **2.7.0** (Android + iOS + JVM desktop). State KMP support as "2.7.0+" — do not back-port the claim to older versions.
- **Room 3.0.0-alpha01** (released 2026-03-11) is a major, breaking, KMP-first line that adds JS/WASM targets, generates only Kotlin, drops KAPT (KSP-only), and disallows blocking DAO functions. **Room 3.0 is ALPHA — treat its API and the `androidx.room3:room3-*` artifact rename as a FORECAST, not a shipped default. Do not migrate production code to it yet.**
- Pin the Room version explicitly in the version catalog; do not float to `+`.

