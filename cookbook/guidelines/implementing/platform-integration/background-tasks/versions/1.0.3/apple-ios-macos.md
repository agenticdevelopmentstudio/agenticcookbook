
Use `BGAppRefreshTask` and `BGProcessingTask` via the BackgroundTasks framework for deferred work. Use `URLSession` background transfers for uploads and downloads that survive app suspension. On macOS, longer-running background work is less restricted but should still use `ProcessInfo.performActivity` to prevent App Nap. Use `NSBackgroundActivityScheduler` for periodic maintenance tasks on macOS.

