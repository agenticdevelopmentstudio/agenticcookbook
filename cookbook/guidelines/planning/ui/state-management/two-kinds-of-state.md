
| Property | Server state | Client state |
|----------|--------------|--------------|
| Owner | A remote system you don't control | This client session |
| Lifecycle | Can go stale, change behind your back | Changes only when the user/app changes it |
| Sync | Asynchronous, may fail, may be slow | Synchronous, always available |
| Examples | User profile, product list, search results | Open modal, selected tab, theme toggle, unsaved form input |
| Needs | Caching, dedup, refetch, invalidation | Read/write, occasionally shared across components |

