
**iOS/macOS UIKit patterns:**

- `UIViewController` subclasses — each view controller is a distinct screen or screen region. Child view controllers and their parent form a container unit.
- `UIView` / `UICollectionViewCell` / `UITableViewCell` subclasses — reusable view components; large custom views are candidates for their own scope group
- Coordinator pattern — a `Coordinator` class that owns and routes between view controllers; each coordinator defines a user flow
- `UIViewControllerRepresentable` — bridging UIKit into SwiftUI; the representable and its UIKit component belong together

**iOS/macOS SwiftUI patterns:**

- `View` + `ViewModel` pairs — a `View` struct and its `@ObservableObject` or `@Observable` view model form the canonical SwiftUI unit
- `View` + `Store` (The Composable Architecture / TCA) — `Reducer`, `State`, `Action`, and the `View` that drives them are one architectural unit
- `EnvironmentKey` + `EnvironmentValues` extension — environment-injected dependencies; the key and its consumers form a loose unit
- Preview providers — `PreviewProvider` / `#Preview` files belong with the view they preview

**Android patterns:**

- `Activity` + `Fragment` pairs — an activity and the fragments it hosts form a screen unit
- MVVM: `ViewModel` + `Fragment`/`Activity` + data binding layout — the ViewModel, its observers, and the UI that consumes it form one unit
- MVI: `ViewModel` + `UiState` sealed class + `UiEvent` — state, events, and the ViewModel that processes them
- Repository pattern — `SomeRepository` interface + implementation; the repository abstracts data access for a feature domain
- Use case / interactor pattern — `GetSomethingUseCase` — single-responsibility business logic unit; groups of related use cases form a feature scope group

**Web / React patterns:**

- React component + hook — a custom `useSomething` hook and the component(s) that use it form a unit if the hook is not shared
- Context + Provider — a `SomeContext` and its `SomeProvider` belong together; the components that consume the context are in the same scope group if the context is narrow
- Next.js: `page.tsx` + `layout.tsx` + `loading.tsx` + `error.tsx` — all route segment files for a given route are one unit
- Redux slice — `somethingSlice.ts` containing `reducer`, `actions`, and `selectors` for one domain; the slice and its `thunk` files form one scope group
- React Query — a set of `useQuery`/`useMutation` hooks for the same API resource domain belong together

**Angular patterns:**

- `NgModule` — each module is a declared scope boundary; lazy-loaded modules are natural scope groups
- Component + Template + Styles — a `.component.ts`, `.component.html`, and `.component.scss` triplet is one unit
- Service — an `@Injectable` service scoped to a module or root; the service and the components it primarily serves
- Guard + Resolver — route guards and resolvers belong with the routes they protect/resolve
- Interceptor — HTTP interceptors are cross-cutting infrastructure (see `cross-cutting-detection`)

**C# / ASP.NET patterns:**

- Controller + ViewModel — an `*Controller.cs` and its associated `*ViewModel.cs` request/response types form one unit
- Repository + Entity — a `SomeRepository.cs` and its `SomeEntity.cs` / `SomeDbContext.cs` form a persistence unit
- MediatR: `Query`/`Command` + `Handler` — the request type and its handler are one unit; group by feature domain
- Blazor: `.razor` component + `.razor.cs` code-behind — one unit

**Plugin / extension architectures:**

- Plugins that implement a declared interface — each plugin is a scope group candidate if it is self-contained
- Middleware chains — individual middleware components are scope group candidates only if they contain significant logic; trivial pass-through middleware belongs with its host pipeline
- Service / repository pairs — a service interface + repository interface + their implementations form a layered feature scope group

**Deviations from framework conventions:**

- Logic in views — business logic in `UIViewController`, React component bodies, or Blazor `.razor` files that should be in a ViewModel or service
- Fat models — domain models with persistence, validation, and business logic mixed in one class
- God services — a single service class handling many unrelated concerns
- Missing abstraction layers — direct API calls from UI components without a service or repository intermediary

