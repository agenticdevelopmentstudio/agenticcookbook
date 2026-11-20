
# Manage complexity through boundaries

Well-defined boundaries between subsystems let each side evolve independently. Define ports (interfaces) that describe what the application needs. Use adapters to translate between external technologies and your ports. Test the core application without databases, UIs, or networks.

- Define each external dependency as a protocol the app owns, not a concrete type the vendor owns
- Keep adapter implementations thin — translate and delegate, never add business logic
- If two modules need to share a type, extract it into a shared contract rather than coupling the modules directly
- Verify boundaries by confirming core logic compiles and tests pass with no framework imports
- Extend at the boundary, don't break the contract: once a boundary is stable and widely depended on, add capability through new implementations behind the port rather than changing the port's existing shape — the durable kernel of the open/closed principle. Apply it only to boundaries that have actually stabilized; do not pre-generalize one you are still discovering (see yagni, steel-thread-first).

