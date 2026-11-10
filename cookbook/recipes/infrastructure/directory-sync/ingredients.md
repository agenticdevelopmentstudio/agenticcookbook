
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Directory tree cache | [adc.ingredient.infrastructure.directory-tree-cache](cookbook:7c689b1f-37db-4422-a129-270c697d5875) | Phase 1: loads the JSON cache for instant display and writes it atomically after every change | Yes | Cache directory (a dedicated `cache-{entryID}` directory per workspace entry) |
| Directory tree scanner | [adc.ingredient.infrastructure.directory-tree-scanner](cookbook:13715ef0-3351-4477-8fa6-24541c65697a) | Phase 2 and Phase 4: full rebuild and surgical reload of affected directories | Yes | `maxScanWorkers` (default 3, clamped to 1-8) |
| Filesystem watcher | [adc.ingredient.infrastructure.filesystem-watcher](cookbook:7e284016-0ceb-4c5e-b3d2-52d9366685cb) | Phase 3: file-level change notifications, debounced and filtered | Yes | Debounce latency (0.5 seconds), excluded path prefixes (default `.git` and package directories) |
| Directory watch coordinator | [adc.ingredient.infrastructure.directory-watch-coordinator](cookbook:01dc6100-4aa9-4b7b-9385-e056260b57b3) | Owns the lifecycle, publishes the tree and `isSyncing`, applies updates on the main thread; the workspace manager pools one per entry | Yes | Entry ID for workspace use |

