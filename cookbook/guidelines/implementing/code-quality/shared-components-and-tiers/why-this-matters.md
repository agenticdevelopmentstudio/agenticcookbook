
A component written one tier too high is invisible to its siblings, so each rebuilds its own. Placing code in the lowest tier that can hold it, and keeping dependencies pointing down, means features compose from shared parts and a change stays inside its boundary.

