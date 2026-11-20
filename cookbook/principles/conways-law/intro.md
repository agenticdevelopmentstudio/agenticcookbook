
# Conway's Law

Any system tends to reproduce the communication structure of the people — or agents — that designed it. Module boundaries follow the seams along which builders coordinate, not the seams a clean design would prefer. The actionable corollary (the "inverse Conway maneuver") is to deliberately shape team and agent boundaries to match the architecture you want, then let the system grow into them.

For a multi-agent dev system this is direct: how you partition work across specialist and platform agents imprints on the generated module boundaries. **Agent assignment is therefore an architectural decision, not just a scheduling one.**
