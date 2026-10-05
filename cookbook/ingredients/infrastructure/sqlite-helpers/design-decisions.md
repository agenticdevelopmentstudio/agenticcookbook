
**Decision**: Expose only parameterized execution; no string-interpolated SQL.
**Rationale**: Making bindings the only way to pass values removes SQL injection as a class of bug and keeps call sites uniform.
**Approved**: pending

