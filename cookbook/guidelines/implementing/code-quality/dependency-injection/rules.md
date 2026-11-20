
- **should-use-constructor-injection**: SHOULD use constructor injection via `Microsoft.Extensions.DependencyInjection`.
- **must-depend-on-interfaces**: Dependencies MUST use interface types, not concrete types.
- **should-use-transient-for-stateless-services**: `Transient` SHOULD be used for lightweight stateless services.
- **should-use-scoped-for-per-request-services**: `Scoped` SHOULD be used for per-request services.
- **should-use-singleton-for-shared-state**: `Singleton` SHOULD be used for thread-safe shared state.
- **must-not-inject-scoped-into-singleton**: A scoped service MUST NOT be injected into a singleton (captive dependency).
- **should-bind-configuration-with-ioptions**: SHOULD use `IOptions<T>` / `IOptionsSnapshot<T>` for configuration binding.
- **should-register-in-add-extension-methods**: SHOULD keep registrations in `Add*()` extension methods for modularity.
