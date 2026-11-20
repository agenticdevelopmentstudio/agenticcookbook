
These examples show one provider shape. Whether the provider interface keeps `isEnabled(key) -> Bool` or takes a call-site default and typed values is an open question for the owner; here the in-code defaults live in one table inside the local implementation.

### Swift: a UserDefaults-backed default

```swift
protocol FeatureFlagProvider {
    func isEnabled(_ key: String) -> Bool
}

final class UserDefaultsFlagProvider: FeatureFlagProvider {
    private let defaults: UserDefaults

    // inCodeDefaults: off = today's behaviour. Nonsensitive values only.
    init(defaults: UserDefaults = .standard, inCodeDefaults: [String: Bool]) {
        self.defaults = defaults
        defaults.register(defaults: inCodeDefaults)
    }

    func isEnabled(_ key: String) -> Bool {
        defaults.bool(forKey: key)   // never throws; falls back to the registered default
    }
}
```

### Kotlin: the decision injected at construction

```kotlin
// The emailer knows nothing about flags; the composition root decides.
class InvoiceEmailer(private val includeOrderCancellation: Boolean) {
    fun build(invoice: Invoice): Email =
        if (includeOrderCancellation) withCancellationLink(invoice) else plain(invoice)
}

val emailer = InvoiceEmailer(
    includeOrderCancellation = flags.isEnabled("{{app_prefix}}.order-cancellation-email"),
)
```

### TypeScript: a localStorage-backed default that never throws

```typescript
export interface FeatureFlagProvider {
  isEnabled(key: string): boolean;
}

export class LocalStorageFlagProvider implements FeatureFlagProvider {
  constructor(private readonly inCodeDefaults: Record<string, boolean>) {}

  isEnabled(key: string): boolean {
    const fallback = this.inCodeDefaults[key] ?? false;
    let raw: string | null;
    try {
      raw = window.localStorage.getItem(key); // throws SecurityError when storage is blocked
    } catch {
      return fallback;
    }
    if (raw === "true") return true;   // localStorage holds strings only
    if (raw === "false") return false;
    return fallback;
  }
}
```

### C#: Microsoft.FeatureManagement with appsettings.json

```json
{
  "FeatureManagement": {
    "NewCheckout": false
  }
}
```

```csharp
builder.Services.AddFeatureManagement();

[FeatureGate("NewCheckout")]
public class NewCheckoutController : Controller { /* ... */ }

// The service knows nothing about flags; it receives the payment strategy.
public class CheckoutService(IPayment payment)
{
    public Task<Receipt> PayAsync(Cart cart) => payment.PayAsync(cart);
}

// Composition: the flag is read here, once per request, and the chosen strategy passed in.
app.MapPost("/checkout", async (Cart cart, IFeatureManager features,
                                NewPayment newPayment, LegacyPayment legacyPayment) =>
{
    IPayment payment = await features.IsEnabledAsync("NewCheckout") ? newPayment : legacyPayment;
    return await new CheckoutService(payment).PayAsync(cart);
});
```

### Tests: both states

```typescript
for (const on of [true, false]) {
  test(`checkout completes with new-checkout ${on ? "on" : "off"}`, () => {
    // checkout receives the decision, not the provider
    expect(checkout(on, cart).status).toBe("paid");
  });
}
```

