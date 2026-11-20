
- `should-receive-dependencies-from-outside`: each component receives its dependencies from outside, or the work says why not
- `should-pass-services-via-initializer-or-protocol-properties`: services are passed via constructor/initializer parameters or protocol properties, or the work says why not
- `must-not-instantiate-concrete-service-in-its-user`: no component instantiates a concrete service it uses
- `should-depend-on-protocol-types`: dependencies are typed as protocols/interfaces, or the work says why not
- `should-avoid-service-locator`: no dependency is obtained through a service locator, or the work says why not
