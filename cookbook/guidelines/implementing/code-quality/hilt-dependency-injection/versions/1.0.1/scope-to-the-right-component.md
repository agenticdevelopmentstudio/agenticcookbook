
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

