
- The server **MUST NOT** treat its own tool descriptions, parameter schemas, or returned results as trusted instructions to the agent; an attacker who controls any of these is attempting tool poisoning or output injection.
- Tool results that contain external/user data **MUST** be returned as clearly delimited data, and the server **SHOULD** strip or neutralize embedded directives (e.g., "ignore previous instructions") before returning them.
- The server **SHOULD** keep tool descriptions stable and side-effect-free; surface side effects in the schema, not in prose meant to steer the model.

