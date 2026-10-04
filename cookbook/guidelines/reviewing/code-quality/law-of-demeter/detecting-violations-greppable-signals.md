
- **Train wrecks**: a chain that walks through structure to reach a target, e.g. `a.getB().getC().doThing()`. Each `.` that traverses a *returned* object (not a fluent self-return) is a violation candidate.
- **Feature envy**: a method that pulls several fields off another object to compute something. The computation **SHOULD** likely live on that object instead.
- **Ask-then-act**: code that queries an object's state and then branches/mutates based on it. Prefer telling the object to perform the action.

A reviewer **MUST** treat a train wreck as a *refactor signal*, not an automatic defect — confirm it crosses object boundaries before flagging.

