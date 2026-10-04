
1. **Shared init/deinit = same scope group.** If object A creates object B in its `init` and destroys it in its `deinit`, A owns B and they belong together.
2. **Subscription ownership defines lifecycle coupling.** If object A stores a `Cancellable` / `DisposeBag` subscription to object B's stream, A's lifecycle bounds the subscription — A and B are lifecycle-coupled.
3. **State machines are atomic.** An explicit state machine — all states, transitions, and the object that executes them — is a single unit. Do not split state machines across scope groups.
4. **Session objects define natural scope group boundaries.** A session — authentication session, network session, user session — and all objects that exist only for the duration of that session form one scope group.
5. **Weak references mark scope group edges.** A `weak` reference from A to B means B does not own A. If A's lifecycle is independent of B's, they may belong in separate scope groups communicating through a narrow interface.
6. **Disposal chain = lifecycle chain.** Follow `Dispose()` / `cancel()` / `close()` calls — each object that disposes another is part of the same lifecycle chain.

