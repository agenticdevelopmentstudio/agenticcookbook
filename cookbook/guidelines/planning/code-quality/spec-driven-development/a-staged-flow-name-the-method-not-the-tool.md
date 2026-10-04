
A common shape is **Spec -> Plan -> Tasks -> Implement -> Verify**: the spec captures requirements, the plan captures the technical approach, tasks break it into ordered units, then implementation executes against the spec.

- Adopt the *methodology*; do **NOT** hard-code a specific tool, command set, or vendor flow into your process. Spec-driven tooling (e.g. plan modes, spec-kit-style scaffolds) churns fast — names and commands change between releases. The durable practice is "write the spec first, separate planning from execution, verify at the end."
- For larger features, the agent **MAY** interview the human first to surface edge cases and tradeoffs, then write the spec, then start a fresh session to implement against it with clean context.

