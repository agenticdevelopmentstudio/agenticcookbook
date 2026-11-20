
- `should-use-constructor-injection`: every dependency is injected through the constructor via `Microsoft.Extensions.DependencyInjection`, or the code says why not
- `must-depend-on-interfaces`: every injected dependency is typed as an interface, not a concrete type
- `should-use-transient-for-stateless-services`: every lightweight stateless service is `Transient`, or the code says why not
- `should-use-scoped-for-per-request-services`: every per-request service is `Scoped`, or the code says why not
- `should-use-singleton-for-shared-state`: every thread-safe shared state service is `Singleton`, or the code says why not
- `must-not-inject-scoped-into-singleton`: no singleton receives a scoped service
- `should-bind-configuration-with-ioptions`: configuration is bound with `IOptions<T>` / `IOptionsSnapshot<T>`, or the code says why not
- `should-register-in-add-extension-methods`: registrations live in `Add*()` extension methods, or the code says why not
