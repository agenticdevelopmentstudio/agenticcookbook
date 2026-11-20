
- Actions that belong to the frontmost object use a `nil` target and are implemented on a responder in the chain. Actions that belong to one object name that object.
- No action reaches its handler through a global or a stored back-reference when the chain would deliver it.
- A `nextResponder` override has a stated reason.

