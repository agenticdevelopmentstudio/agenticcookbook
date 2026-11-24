
*This section is informative.*

A cycle check over the exported milestone links, followed by the critical path:

```python
from graphlib import TopologicalSorter, CycleError
import networkx as nx

# milestone -> the milestones it depends on
depends_on = {
    "api-freeze": {"start"},
    "docs-ready": {"api-freeze"},
    "beta": {"api-freeze"},
    "launch": {"beta", "docs-ready"},
}

try:
    order = list(TopologicalSorter(depends_on).static_order())
except CycleError as err:
    raise SystemExit(f"cycle in milestone chain: {' -> '.join(err.args[1])}")

# durations, in working days, of the work on each link
days = {("start", "api-freeze"): 15, ("api-freeze", "docs-ready"): 5,
        ("api-freeze", "beta"): 10, ("beta", "launch"): 5, ("docs-ready", "launch"): 3}
g = nx.DiGraph()
for (a, b), d in days.items():
    g.add_edge(a, b, days=d)
print(nx.dag_longest_path(g, weight="days"))   # ['start', 'api-freeze', 'beta', 'launch']
```

Had `start` also depended on `launch`, the sort would have stopped with `cycle in milestone chain: start -> launch -> beta -> api-freeze -> start` (the order the error lists varies).

A status update for one milestone:

```text
Status date:  2026-11-20
Milestone:    Beta
Status:       At risk
Baseline:     2026-12-01    Forecast: 2026-12-05 (+4 days)
Risk:         R-14 Load tests may fail on the new storage tier; mitigation in progress
Change:       Forecast moved 4 days after the API freeze slipped; launch still holds inside its contingency
```

A milestone given as work, and the same plan done as events with the work between them:

```text
As work (avoid):   "Build the export service"  (milestone, 3 weeks)
As events:         start -> [build export service, 15 days] -> Export service live (milestone)
```

