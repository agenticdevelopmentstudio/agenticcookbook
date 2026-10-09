
- A lower tier MUST NOT import from a higher one. The foundation knows nothing about the features built on it.
- When a lower tier needs something from above, invert the dependency: define a protocol or callback in the lower tier and let the higher tier supply it.
- A cycle between tiers means the shared part belongs in a tier below both. Extract it rather than allowing the cycle.
- This is separation of concerns applied to layers. It limits what a change can break, and lets each tier be understood by itself.

