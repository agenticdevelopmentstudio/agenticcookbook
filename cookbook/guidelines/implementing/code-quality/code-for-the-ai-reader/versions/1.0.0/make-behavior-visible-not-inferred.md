
- Minimize reflection, dynamic dispatch, and runtime metaprogramming that hides what code actually does. These force an agent (and a human) to simulate the runtime to predict behavior.
- Function signatures act as design documents the agent reads first — keep parameter names and return types explicit and accurate. (See the reference.)
- Explicit types and verbose, intention-revealing names are a deliberate **semantic investment**: they encode meaning the agent would otherwise have to reconstruct from context it may not have loaded. Prefer them where a language makes them optional.
- Prefer explicit control flow over implicit magic (auto-registration, monkey-patching, import-time side effects). Surprising behavior costs both audiences — see `principle-of-least-astonishment`.

