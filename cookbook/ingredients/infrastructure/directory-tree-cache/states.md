
| State | Behavior |
|-------|----------|
| No cache | Loader returns an empty state; the caller begins a full sync immediately |
| Cache loaded | Entries are reconstructed into a tree and handed to the caller for display |
| Cache corrupt or unreadable | Treated exactly like no cache; a warning is logged |
| Saving | A background write to a temporary file is in progress |
| Saved | The temporary file has been atomically renamed over the cache file |

