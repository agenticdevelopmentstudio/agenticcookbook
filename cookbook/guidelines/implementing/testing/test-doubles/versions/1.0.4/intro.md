
# Test Doubles

Use [Martin Fowler's taxonomy](https://martinfowler.com/bliki/TestDouble.html):

| Double | Purpose | Example |
|--------|---------|---------|
| **Dummy** | Fill a parameter, never used | `null` or empty object |
| **Stub** | Return canned answers | `stub.getUser() → User("test")` |
| **Spy** | Record calls for later verification | `spy.wasCalled("save")` |
| **Mock** | Verify expected interactions | `mock.verify(save, times: 1)` |
| **Fake** | Working implementation, simplified | In-memory database |

**Fakes SHOULD be preferred over mocks** when possible. Fakes exercise real behavior; mocks only verify
expectations. A fake in-memory database catches more bugs than a mock that returns canned SQL results.

**You MUST NOT mock what you don't own.** Wrap external dependencies (HTTP clients, databases, SDKs)
behind your own interface. Mock your interface, not the third-party API directly. This
insulates tests from upstream API changes.

**Platform tools:**
- **Python:** `unittest.mock` (stdlib), [pytest-mock](https://github.com/pytest-dev/pytest-mock)
- **TypeScript/JS:** `jest.mock`, [vitest mocking](https://vitest.dev/guide/mocking.html)
- **Swift:** Protocol conformances (no framework needed), [swift-testing](https://github.com/apple/swift-testing)
- **.NET:** [NSubstitute](https://nsubstitute.github.io/)
- **Kotlin:** [MockK](https://mockk.io/), [Turbine](https://github.com/cashapp/turbine) for Flow testing

