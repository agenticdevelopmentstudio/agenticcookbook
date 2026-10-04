---
id: 2b7a1e5f-80b0-4837-ab7e-5b6151450d4a
title: "Dependency Injection"
domain: agenticdevelopercookbook://guidelines/reviewing/code-quality/dependency-injection
type: guideline
version: 1.0.3
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Use constructor injection via Microsoft.Extensions.DependencyInjection, depend on interface types rather than concrete types, and never inject a scoped service into a singleton."
platforms: []
languages:
  - csharp
tags:
  - csharp
  - dependency-injection
  - language
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - new-module
  - code-review
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.3 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
