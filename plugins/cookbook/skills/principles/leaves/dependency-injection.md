<!-- leaf: principles/dependency-injection · source: principles/dependency-injection.md -->

# Dependency injection

A component should receive its dependencies from the outside, not construct them internally:

- Pass services via constructor/initializer parameters or protocol properties
- Never instantiate a concrete service inside the component that uses it
- Use protocol/interface types for dependencies, not concrete types
- Avoid service locator pattern (hidden global lookup)
