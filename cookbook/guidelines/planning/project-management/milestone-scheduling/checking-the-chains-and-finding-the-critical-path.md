
*This section is informative.*

A topological sort orders the milestones so that every one comes after the milestones it depends on. A complete order exists only when the graph has no cycle, so the sort is the cycle check: Python's `graphlib.TopologicalSorter` raises `CycleError`, and its second argument is one cycle, listed with the same node first and last. Trackers differ here: Jira does not stop a cyclic link being made, and Atlassian's advice is to export the links and scan them; Microsoft Project cannot calculate dates across a loop and offers to cancel the action that would make one.

With the graph acyclic, the critical path is its longest path by duration. NetworkX's `dag_longest_path` computes it from durations on the links.

