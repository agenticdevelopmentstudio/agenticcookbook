
- **should-receive-dependencies-from-outside**: A component SHOULD receive its dependencies from the outside, not construct them internally.
- **should-pass-services-via-initializer-or-protocol-properties**: SHOULD pass services via constructor/initializer parameters or protocol properties.
- **must-not-instantiate-concrete-service-in-its-user**: MUST NOT instantiate a concrete service inside the component that uses it.
- **should-depend-on-protocol-types**: SHOULD use protocol/interface types for dependencies, not concrete types.
- **should-avoid-service-locator**: SHOULD avoid the service locator pattern (hidden global lookup).
