
- Annotate ViewModels with `@HiltViewModel` and an `@Inject constructor`. Hilt supplies the factory; inject `SavedStateHandle` for navigation/saved args. Do not construct these ViewModels manually.
- For Compose, retrieve them with `hiltViewModel()` (`androidx.hilt:hilt-navigation-compose`).
- Annotate `CoroutineWorker`/`Worker` subclasses with `@HiltWorker`. Runtime params (`Context`, `WorkerParameters`) **MUST** use `@AssistedInject` + `@Assisted`; other dependencies inject normally. Inject `HiltWorkerFactory` into the `Application` and wire it through a custom `WorkManager` `Configuration` (or the `Configuration.Provider` on the `Application`).

