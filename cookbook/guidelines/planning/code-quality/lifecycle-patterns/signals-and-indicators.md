
**Construction and initialization:**

- Custom `init` / constructor with dependency parameters — the set of parameters reveals what the object owns vs borrows
- Factory methods — `SomeClass.make()`, `SomeClass.create(with:)`, static constructors — note what the factory assembles
- Builder patterns — `SomeBuilder().withX().withY().build()` — the builder collects all initialization dependencies; the built object's lifecycle starts at `build()`
- Two-phase initialization — `init()` followed by explicit `setup()` / `configure()` / `start()` — note what state exists between phases
- `@objc func awakeFromNib()` / `viewDidLoad()` — lifecycle initialization in the view layer tied to the host view controller's own lifecycle

**Teardown and cleanup:**

- `deinit` (Swift), `finalize()` (Java), destructor `~ClassName()` (C++), `Dispose()` / `IDisposable` (C#), `close()` / `Closeable` (Java/Kotlin) — note what resources are released
- `onDestroy()`, `onStop()`, `viewWillDisappear()`, `componentWillUnmount()` — framework-managed teardown hooks; note what cleanup is performed
- Explicit `cancel()`, `invalidate()`, `stop()`, `shutdown()` calls — active teardown beyond simple deallocation
- `defer` blocks (Swift/Go) — resource cleanup guaranteed at scope exit
- `using` (C#), `try-with-resources` (Java), `with` statement (Python) — automatic resource management scope

**Retain and memory management:**

- `weak` / `unowned` references in Swift — indicates shared ownership or prevents cycles; the `weak` end does not participate in the lifecycle of the `strong` end
- `WeakReference<T>` in Kotlin/Java/C# — same semantics
- Reference counting in C++ (`shared_ptr` / `weak_ptr`) — ownership semantics explicit in type
- `@autoreleasepool` blocks — scope-limited memory management
- Capture lists in closures — `[weak self]` vs `[unowned self]` vs strong capture — strong capture extends lifetime

**Connection and session management:**

- Database connection pools — `ConnectionPool`, `DBQueue` (GRDB), `Core Data` persistent container — connections acquired and returned
- Network session objects — `URLSession`, `OkHttpClient`, `HttpClient` — note whether sessions are per-request or long-lived
- WebSocket connections — establish, maintain, reconnect, close — a distinct lifecycle unit
- Bluetooth peripheral connections — `CBCentralManager` connect/disconnect cycle
- Authentication sessions — login → token refresh → logout; the token's validity window IS the session lifecycle

**State machines:**

- Explicit state enums with associated values — `enum State { case idle, loading, loaded(Data), error(Error) }` — the state machine is a lifecycle in data
- State transition methods — `func transitionTo(_ state: State)` — note valid transitions
- Reactive state sequences — `@Published var state: State` (Combine), `StateFlow` (Kotlin), `BehaviorSubject` (RxSwift/RxKotlin) — the stream IS the state machine

**Resource ownership and disposal:**

- Subscription storage — `var cancellables = Set<AnyCancellable>()` (Combine), `disposeBag: DisposeBag` (RxSwift), `compositeDisposable` (RxJava) — the object that holds the storage bag owns the subscription lifecycle
- Timer lifecycle — `Timer.scheduledTimer()` must be invalidated; note where invalidation happens relative to the owning object's teardown
- `NotificationCenter` observer registration — note whether removal is explicit (`removeObserver`) or managed by token disposal

**Pooling and reuse:**

- Object pools — `ReusablePool`, cell reuse in `UITableView`/`RecyclerView` — objects are not destroyed but returned; their lifecycle is the pool's lifecycle, not the consumer's
- View recycling — `prepareForReuse()` — an intermediate lifecycle event between allocation and consumer use

