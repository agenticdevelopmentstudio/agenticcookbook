
```swift
protocol ExperimentProvider {
    /// Never throws; returns `default` on any failure.
    func variant(_ key: String, default: String) -> String
}

// At the point of use: evaluation and exposure happen where the variant is shown.
let checkout = experiments.variant("checkout-button-copy", default: "control")
analytics.logExposure(experiment: "checkout-button-copy", variant: checkout)
button.title = checkout == "buy-now" ? "Buy now" : "Checkout"
```

- **Exposure, wrong:** fetching every variant at app launch and logging exposure there counts users who never open the checkout, which dilutes the measured effect.
- **Allocation, wrong:** cutting a treatment from 50% to 10% and back to 50% without sticky bucketing reshuffles users and produces a sample ratio mismatch.
- **Web, right:** a test that serves `/landing-b` to half its visitors uses a 302 redirect from `/landing` and `<link rel="canonical" href="/landing">` on `/landing-b`.

