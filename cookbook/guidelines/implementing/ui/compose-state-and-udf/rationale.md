
- `should-pass-narrowest-parameters`, `should-prefer-stable-parameter-types`: The Compose compiler enables **strong skipping** by default in current releases (Kotlin 2.x + the Compose compiler Gradle plugin), which skips composables even with some unstable parameters — but minimizing scope and preferring stable types remains the durable practice.
