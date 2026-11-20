
**Delegation patterns:**

- Swift: `weak var delegate: SomeDelegate?` properties; protocol declarations named `*Delegate`, `*DataSource`; `delegate?.someMethod()` call sites
- Objective-C: `@protocol` declarations; `id<Protocol>` typed delegate properties
- Kotlin: interface-based delegation; `by` keyword delegation
- C#: `event` declarations; delegate types; `EventHandler<T>` patterns
- TypeScript: callback props in React (`onPress`, `onChange`, `onSubmit`); callback-typed interface fields

**Observer and notification patterns:**

- iOS: `NotificationCenter.default.addObserver()` / `post(name:)` — note the notification name, sender, and observer registration site. Each notification is an implicit coupling between poster and observer.
- Android: `LocalBroadcastManager`, `EventBus`, `LiveData.observe()`, `Flow.collect()`, `BroadcastReceiver`
- C#: `IObservable<T>` / `IObserver<T>`; Reactive Extensions (`Rx.NET`); `WeakReference` event subscriptions
- Web: `addEventListener` / `dispatchEvent`; custom `EventEmitter`; `window.postMessage`; `BroadcastChannel`
- Reactive frameworks: `Combine` (Swift), `RxSwift`, `RxKotlin`, `RxJS` — publisher/subscriber chains; note where publishers are created vs where subscribers attach

**Shared state and singletons:**

- Global or class-level `static var shared` / `static let shared` — singleton access points
- `UserDefaults` / `SharedPreferences` / `localStorage` reads and writes — shared mutable state accessed by key string
- Global state containers: Redux store, MobX observables, Zustand store, Vuex store, `@EnvironmentObject` (SwiftUI), `Context` (React)
- Thread-local or actor-isolated state — note the isolation boundary

**Dependency injection:**

- Constructor injection — dependencies passed as initializer arguments; clean coupling, easy to test
- Property injection — `var service: SomeService?` set after construction; looser coupling but less explicit
- DI containers: Swinject, Hilt, Dagger, Spring, Koin, inversify — note registration vs resolution sites
- `@Environment` / `@EnvironmentObject` (SwiftUI), `@Inject` / `@Provides` (Hilt/Dagger), `@Injectable` (Angular)

**Navigation and routing:**

- Coordinator pattern — a coordinator object owns navigation decisions and routes between screens
- Router pattern — centralized routing table; routes referenced by name or enum case
- Direct `present()`, `push()`, `navigate()`, `startActivity()` calls from within a view — tight coupling between view and navigation
- Deep link handlers — URL-to-screen mapping centralized in a router or scattered across app delegates
- Navigation state in global store (React Navigation, SwiftUI `NavigationPath`) — navigation is shared state

**Callback chains:**

- Completion handler chains — `func doThing(completion: @escaping (Result) -> Void)` — note depth; chains of 3+ levels suggest refactoring to async/await
- Promise chains — `.then().then().catch()` — note where error handling breaks the chain
- `async/await` call chains — cleaner but still represent control flow coupling

**Event buses:**

- Named event systems: custom `EventBus`, `MessageBus`, `PubSub` implementations
- Cross-component event dispatching where event consumer is not statically known at definition time

