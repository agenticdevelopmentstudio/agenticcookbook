
- `should-receive-dependencies-from-outside`: whether each component receives its dependencies from outside
- `should-pass-services-via-initializer-or-protocol-properties`: whether services are passed via constructor/initializer parameters or protocol properties
- `must-not-instantiate-concrete-service-in-its-user`: whether any component instantiates a concrete service it uses
- `should-depend-on-protocol-types`: whether dependencies are typed as protocols/interfaces rather than concrete types
- `should-avoid-service-locator`: whether any dependency is obtained through a service locator
