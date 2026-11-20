
| Double | Purpose | Example |
|--------|---------|---------|
| **Dummy** | Fill a parameter, never used | `null` or empty object |
| **Stub** | Return canned answers | `stub.getUser() → User("test")` |
| **Spy** | Record calls for later verification | `spy.wasCalled("save")` |
| **Mock** | Verify expected interactions | `mock.verify(save, times: 1)` |
| **Fake** | Working implementation, simplified | In-memory database |

