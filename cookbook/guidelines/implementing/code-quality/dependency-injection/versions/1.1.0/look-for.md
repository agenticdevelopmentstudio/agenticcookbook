
- `should-use-constructor-injection`: dependencies resolved by service locator, property injection or `new` instead of constructor parameters registered with `Microsoft.Extensions.DependencyInjection`
- `must-depend-on-interfaces`: a constructor parameter or registration typed as a concrete class
- `should-use-transient-for-stateless-services`: a lightweight stateless service registered as anything but `Transient`
- `should-use-scoped-for-per-request-services`: a per-request service registered as anything but `Scoped`
- `should-use-singleton-for-shared-state`: shared state registered as `Singleton` that is not thread-safe, or thread-safe shared state given another lifetime
- `must-not-inject-scoped-into-singleton`: a singleton whose constructor takes a scoped service
- `should-bind-configuration-with-ioptions`: configuration read directly from `IConfiguration` or hand-copied instead of bound through `IOptions<T>` / `IOptionsSnapshot<T>`
- `should-register-in-add-extension-methods`: registrations made inline in startup code rather than in `Add*()` extension methods
