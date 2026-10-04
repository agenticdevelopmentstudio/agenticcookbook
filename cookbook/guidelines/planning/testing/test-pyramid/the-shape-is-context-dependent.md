
The pyramid is a default, not dogma. Teams SHOULD choose the test distribution per
system based on where risk actually lives, not a fixed ratio. Integration-heavy systems
(thin logic over many collaborators — databases, queues, external services) MAY instead
fit the "testing trophy" shape: a larger band of integration tests, with static analysis
and type-checking as the broad base beneath them. When most of the risk is in how
components interact rather than in isolated logic, the trophy SHOULD be preferred over
the pyramid.

