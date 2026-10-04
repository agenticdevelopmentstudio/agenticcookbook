
# Law of Demeter and Tell, Don't Ask

The Law of Demeter (a "principle of least knowledge") says a method **SHOULD** talk only to its immediate collaborators, not to objects it reaches through them. The related "Tell, Don't Ask" heuristic says you **SHOULD** tell an object to do something rather than ask for its internals and act on them yourself. Both reduce coupling, but both have well-known exceptions — apply them as SHOULD-level review signals, not absolute rules.

