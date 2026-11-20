
# Kotlin Multiplatform

Kotlin Multiplatform (KMP) shares non-UI logic — domain, data, networking — across Android, iOS, desktop, and web from a single `commonMain` source set, using `expect`/`actual` for the few platform-specific seams. The default share boundary is business logic; UI is a per-platform decision, not an automatic share.

