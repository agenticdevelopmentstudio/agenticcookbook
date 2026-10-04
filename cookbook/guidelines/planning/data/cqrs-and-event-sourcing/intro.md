
# CQRS and event sourcing

CQRS (Command Query Responsibility Segregation) splits the write model (commands that mutate state) from the read model (queries that return data), letting each evolve and scale separately. Event sourcing stores state as an append-only log of immutable events; current state is derived by replaying or projecting those events into read models. They are independent patterns that are often, but not necessarily, combined.

