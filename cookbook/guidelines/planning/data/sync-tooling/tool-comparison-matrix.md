
| Feature | Session Extension | cr-sqlite | Litestream | ElectricSQL | PowerSync | Turso | sqlite-sync |
|---------|:-----------------:|:---------:|:----------:|:-----------:|:---------:|:-----:|:-----------:|
| Sync direction | Manual | Bidirectional | One-way (backup) | Bidirectional | Bidirectional | Bidirectional | Bidirectional |
| Conflict resolution | Callback (custom) | CRDT automatic | N/A | CRDT (LWW) | Custom (your backend) | Multiple strategies | CRDT automatic |
| Server database | Any | Any | N/A (storage) | Postgres only | Postgres, MongoDB | Turso Cloud | SQLite Cloud, PG, Supabase |
| Offline writes | Yes | Yes | No | Yes | Yes | Yes (Beta) | Yes |
| Custom write logic | Yes | No | N/A | No | Yes | Partial | No |
| Setup complexity | Low (C API) | Low (extension) | Low (config file) | Medium | Medium | Low | Low (extension) |
| Maturity | Stable | Beta | Stable | Production | Production | Beta (offline) | Beta |

