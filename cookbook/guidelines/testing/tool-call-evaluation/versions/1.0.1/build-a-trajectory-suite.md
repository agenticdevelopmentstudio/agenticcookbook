
- Each test case **MUST** pin an input and the expected tool-call trajectory (tool names plus expected arguments). Treat this suite as a fixed, versioned regression set.
- Argument checks **SHOULD** allow semantic equivalence where exact match is too strict (e.g., equivalent date formats), but **MUST** stay strict on identifiers, units, and destructive parameters.
- Score against the trajectory, not just the final output — an agent can reach a correct answer through an unsafe or wasteful path.

