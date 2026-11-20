
- `should-receive-dependencies-from-outside`: a component that constructs its own dependencies
- `should-pass-services-via-initializer-or-protocol-properties`: a service reaching a component by some route other than its constructor/initializer parameters or protocol properties
- `must-not-instantiate-concrete-service-in-its-user`: a concrete service instantiated inside the component that uses it
- `should-depend-on-protocol-types`: a dependency declared with a concrete type
- `should-avoid-service-locator`: a dependency fetched through a service locator or other hidden global lookup
