
- Place each piece in the lowest tier whose dependencies it can live with. If it needs only the foundation, it belongs in the foundation tier, not in the feature that needed it first.
- Code written one tier too high is invisible to every sibling that will need it next. Moving it down later costs more than placing it right now.
- Do not create a new tier, framework or target to hold a feature. Adding one is a decision for the project owner.
- Ask of each piece: could a command-line tool link this without the application? If it reads an application settings singleton or an app-only type, pass that value in as a parameter, and the piece moves down.

