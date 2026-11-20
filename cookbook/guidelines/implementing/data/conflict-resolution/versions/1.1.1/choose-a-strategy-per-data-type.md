
No single strategy fits all data. Apply the simplest strategy that is correct for each entity type:

| Strategy | When to Use |
|----------|-------------|
| Last-Write-Wins (LWW) | Settings, preferences, low-contention single-user records |
| Server-wins | Admin-pushed config, read-only replication |
| Client-wins | Personal notes, drafts owned by one user |
| Field-level merge | Task trackers, CRMs — concurrent users edit different fields |
| CRDTs | Collaborative editing, peer-to-peer, extended offline periods |
| Operational Transformation | Collaborative text with a central server |
| Conflict queue | Medical, legal, financial — silent loss is unacceptable |

