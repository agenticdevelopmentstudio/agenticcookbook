
| Boundary | Posture | Rationale |
|----------|---------|-----------|
| Machine-to-machine (wire, internal API) | **Strict** parse, reject + report | Tolerance here breeds undocumented coupling |
| External/3rd-party input you don't control | **Strict** parse, but graceful degradation | You cannot fix their sender; fail safe, log, alert |
| Human/UX edge (forms, CLI args, NL) | **Forgiving** — normalize then validate | Usability; humans are not protocols |
