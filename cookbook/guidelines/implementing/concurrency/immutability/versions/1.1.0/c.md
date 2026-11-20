
```csharp
// Immutable DTO
public record OrderSummary(string OrderId, decimal Total, DateTime CreatedAt);

// Modified copy
var updated = order with { Total = 99.99m };

// Readonly value type
public readonly record struct Point(double X, double Y);
```
