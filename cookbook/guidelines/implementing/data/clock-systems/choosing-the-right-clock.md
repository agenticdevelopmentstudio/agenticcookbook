
| Scenario | Recommended Clock |
|----------|------------------|
| Server assigns all timestamps | Physical clock (server-side) |
| Client-server sync with server authority | Server-assigned monotonic versions |
| Multi-device, causal ordering needed | Hybrid Logical Clocks (HLC) |
| Small fixed replica set (database cluster) | Vector clocks |
| Simple causal ordering, low overhead | Lamport timestamps |
| Peer-to-peer, no central server | HLC or CRDTs (which embed their own ordering) |

