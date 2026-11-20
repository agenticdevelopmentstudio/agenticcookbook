
# Hilt dependency injection for Android

Hilt is Google's recommended DI framework for non-trivial Android apps. Apps **SHOULD** use Hilt with the KSP annotation processor and prefer constructor injection. `@Singleton` **SHOULD** be reserved for genuinely app-scoped state — over-scoping is the most common Hilt mistake.

