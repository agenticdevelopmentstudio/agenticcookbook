
For every logical change:

1. **Make the change** — implement one coherent unit of work
2. **Build** — run the platform build command (`xcodebuild`, `./gradlew build`, `npm run build`, `dotnet build`, `cargo build`)
3. **Verify** — the build MUST pass and existing tests MUST still pass before committing
4. **Commit** — commit the passing change with a descriptive message
5. **Repeat** — move to the next logical change

Multiple uncommitted changes MUST NOT be stacked. If a change breaks the build, fix it before moving on — do not add more changes on top of a broken state. This prevents compound debugging sessions where multiple interacting changes all break at once.

