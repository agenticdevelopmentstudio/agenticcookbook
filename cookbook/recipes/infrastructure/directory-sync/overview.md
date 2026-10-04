
A lifecycle pattern for synchronizing an in-memory file tree with the filesystem. The coordinator drives four sequential phases: cache load (instant display) followed by full sync (accurate rebuild) followed by watch (live updates) followed by surgical update (efficient patching). This ensures the UI displays a file tree immediately on launch while converging to an accurate, live-updated representation as quickly as possible.

