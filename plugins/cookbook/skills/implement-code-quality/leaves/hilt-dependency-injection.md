<!-- leaf: implement-code-quality/hilt-dependency-injection · source: guidelines/implementing/code-quality/hilt-dependency-injection.md -->

**Rules** (cite as `implement-code-quality/hilt-dependency-injection#<slug>`):

- `android-apps-apps-use-hilt-ksp-annotation` SHOULD — Hilt is Google's recommended DI framework for non-trivial Android apps. Apps SHOULD use Hilt with the KSP annotation …
- `root-dependency-graph-exist-exactly-once` MUST — Annotate the Application subclass with @HiltAndroidApp. This is the root of the dependency graph and MUST exist exactly …
- `classes-you-own-declare-dependencies-via-inject` SHOULD — Classes you own SHOULD declare dependencies via an @Inject constructor. Hilt then provides them without a module.
- `unscoped-binding-assumed-create-new-instance` MUST — An unscoped binding MUST be assumed to create a new instance per injection point — that is the correct default for …
- `longer-lived-component-not-depend-shorter-lived-one` MUST — A longer-lived component MUST NOT depend on a shorter-lived one (e.g. a @Singleton holding an Activity). This is a …
- `singleton-not-applied-performance-just-case` SHOULD — @Singleton SHOULD NOT be applied for performance "just in case." Scope only stateful, expensive-to-build, or app-shared …
- `params-context-workerparameters-use-assistedinject-assisted-other` MUST — Annotate CoroutineWorker/Worker subclasses with @HiltWorker. Runtime params (Context, WorkerParameters) MUST use …

# Hilt dependency injection for Android

Hilt is Google's recommended DI framework for non-trivial Android apps. Apps **SHOULD** use Hilt with the KSP annotation processor and prefer constructor injection. `@Singleton` **SHOULD** be reserved for genuinely app-scoped state — over-scoping is the most common Hilt mistake.

## Setup

- Use **KSP** (`com.google.devtools.ksp`) for the Hilt compiler, not the legacy KAPT. KAPT is in maintenance and slower; KSP is the durable choice and supports KSP2 on Kotlin 2.x.
- Apply the `com.google.dagger.hilt.android` Gradle plugin and add `hilt-android` plus the compiler via `ksp(...)`.
- Annotate the `Application` subclass with `@HiltAndroidApp`. This is the root of the dependency graph and **MUST** exist exactly once.
- Annotate Android entry points (`Activity`, `Fragment`, `Service`) needing field injection with `@AndroidEntryPoint`.

## Prefer constructor injection

- Classes you own **SHOULD** declare dependencies via an `@Inject constructor`. Hilt then provides them without a module.
- Use a `@Module` with `@Provides` only for types you do not own (third-party, builders) or interfaces. Bind an interface to its implementation with `@Binds` in an `abstract` module — it generates less code than `@Provides`.
- Install every module into a component with `@InstallIn(...)`. Choose the **narrowest** component that fits the binding's lifetime.

## Scope to the right component

| Scope | Component | Lifetime | Use for |
|-------|-----------|----------|---------|
| `@Singleton` | `SingletonComponent` | Application | App-wide singletons (DB, network client, app-scoped state) |
| `@ActivityRetainedScoped` | `ActivityRetainedComponent` | Survives config change | Shared state across recreation |
| `@ViewModelScoped` | `ViewModelComponent` | One ViewModel | Per-ViewModel collaborators |
| `@ActivityScoped` | `ActivityComponent` | One Activity | Activity-tied dependencies |
| `@FragmentScoped` | `FragmentComponent` | One Fragment | Fragment-tied dependencies |

- An unscoped binding **MUST** be assumed to create a new instance per injection point — that is the correct default for stateless collaborators.
- A longer-lived component **MUST NOT** depend on a shorter-lived one (e.g. a `@Singleton` holding an `Activity`). This is a captive-dependency leak.
- `@Singleton` **SHOULD NOT** be applied for performance "just in case." Scope only stateful, expensive-to-build, or app-shared instances.

## Jetpack integration

- Annotate ViewModels with `@HiltViewModel` and an `@Inject constructor`. Hilt supplies the factory; inject `SavedStateHandle` for navigation/saved args. Do not construct these ViewModels manually.
- For Compose, retrieve them with `hiltViewModel()` (`androidx.hilt:hilt-navigation-compose`).
- Annotate `CoroutineWorker`/`Worker` subclasses with `@HiltWorker`. Runtime params (`Context`, `WorkerParameters`) **MUST** use `@AssistedInject` + `@Assisted`; other dependencies inject normally. Inject `HiltWorkerFactory` into the `Application` and wire it through a custom `WorkManager` `Configuration` (or the `Configuration.Provider` on the `Application`).

## Testing

- Use `hilt-android-testing` with `kspTest`/`kspAndroidTest`. Annotate tests with `@HiltAndroidTest` and drive injection with `HiltAndroidRule`.
- Replace bindings in tests with `@TestInstallIn` or `@BindValue` rather than mutating production modules.

## Anti-patterns

- Do not inject the Hilt-managed graph by passing `Context` around to build objects manually — that defeats the framework.
- Do not field-inject where constructor injection is possible; reserve field injection for framework-instantiated entry points.
- Do not create god modules. Split modules by feature and install them into the narrowest applicable component.
