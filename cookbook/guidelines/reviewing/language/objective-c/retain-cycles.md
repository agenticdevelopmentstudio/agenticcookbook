
- A block stored on `self` that mentions `self` (directly, or through an ivar) captures a weak reference, and uses a strong local inside.
- Timers, notification observers and KVO registrations are removed in `dealloc` or an earlier teardown, and do not keep their target alive.

