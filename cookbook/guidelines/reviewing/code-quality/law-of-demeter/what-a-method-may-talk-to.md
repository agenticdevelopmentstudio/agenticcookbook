
A method **SHOULD** only send messages to:

- `this` / `self`
- its own parameters
- objects it creates directly
- its own direct fields/properties
- (in some formulations) globals/singletons it holds — treat these with suspicion regardless

