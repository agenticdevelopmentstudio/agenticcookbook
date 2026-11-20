
- `should-use-constructor-injection`: each new service receives its dependencies as constructor parameters resolved by `Microsoft.Extensions.DependencyInjection`, or the code says why not
- `must-depend-on-interfaces`: each new constructor parameter and registration uses an interface type
- `should-use-transient-for-stateless-services`: each new lightweight stateless service is registered `Transient`, or the code says why not
- `should-use-scoped-for-per-request-services`: each new per-request service is registered `Scoped`, or the code says why not
- `should-use-singleton-for-shared-state`: each new thread-safe shared state service is registered `Singleton`, or the code says why not
- `must-not-inject-scoped-into-singleton`: no singleton the build registers depends on a scoped service (scope validation on, or the graph checked)
- `should-bind-configuration-with-ioptions`: each new configuration section is bound through `IOptions<T>` / `IOptionsSnapshot<T>`, or the code says why not
- `should-register-in-add-extension-methods`: each new registration is in an `Add*()` extension method, or the code says why not
