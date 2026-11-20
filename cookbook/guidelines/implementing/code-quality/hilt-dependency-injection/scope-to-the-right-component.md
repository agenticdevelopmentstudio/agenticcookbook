
| Scope | Component | Lifetime | Use for |
|-------|-----------|----------|---------|
| `@Singleton` | `SingletonComponent` | Application | App-wide singletons (DB, network client, app-scoped state) |
| `@ActivityRetainedScoped` | `ActivityRetainedComponent` | Survives config change | Shared state across recreation |
| `@ViewModelScoped` | `ViewModelComponent` | One ViewModel | Per-ViewModel collaborators |
| `@ActivityScoped` | `ActivityComponent` | One Activity | Activity-tied dependencies |
| `@FragmentScoped` | `FragmentComponent` | One Fragment | Fragment-tied dependencies |
