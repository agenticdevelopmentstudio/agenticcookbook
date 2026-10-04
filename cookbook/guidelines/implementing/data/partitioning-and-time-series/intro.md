
# Table partitioning and time-series data

Partitioning splits one logical table into physical child partitions so the planner can prune irrelevant data and you can drop whole partitions cheaply. It adds real operational complexity, so treat it as a measured-need optimization, not a default.

