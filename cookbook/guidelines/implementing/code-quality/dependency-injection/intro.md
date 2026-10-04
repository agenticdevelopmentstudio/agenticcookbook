
# Dependency Injection

Constructor injection via `Microsoft.Extensions.DependencyInjection`. Dependencies MUST use interface types, not concrete types.

- `Transient` for lightweight stateless services
- `Scoped` for per-request services
- `Singleton` for thread-safe shared state
- A scoped service MUST NOT be injected into a singleton (captive dependency)
- Use `IOptions<T>` / `IOptionsSnapshot<T>` for configuration binding
- Keep registrations in `Add*()` extension methods for modularity

```csharp
public static IServiceCollection AddMyFeature(this IServiceCollection services)
{
    services.AddSingleton<IFeatureManager, LocalFeatureManager>();
    services.AddTransient<IOrderService, OrderService>();
    return services;
}
```

