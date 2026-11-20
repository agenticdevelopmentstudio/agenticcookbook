
| Boundary | Posture | Rationale |
|----------|---------|-----------|
| Machine-to-machine (wire, internal API) | **Strict** parse, reject + report | Tolerance here breeds undocumented coupling |
| External/3rd-party input you don't control | **Strict** parse, but graceful degradation | You cannot fix their sender; fail safe, log, alert |
| Human/UX edge (forms, CLI args, NL) | **Forgiving** — normalize then validate | Usability; humans are not protocols |

Do **NOT** read this guideline as "be hostile and strict everywhere." Hostile strictness at the human edge harms usability; the synthesis is: **strict internally, forgiving at the human edge, with active maintenance closing the loop**.

