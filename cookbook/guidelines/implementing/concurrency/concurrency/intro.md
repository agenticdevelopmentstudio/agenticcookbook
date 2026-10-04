
# No blocking the main thread

All lengthy work must run on background threads/tasks using platform async primitives:

- **Apple**: Swift Concurrency (`async`/`await`, `Task`, actors)
- **Android**: Kotlin Coroutines (`viewModelScope`, `Dispatchers.IO`)
- **Web**: `Promise`/`async`, Web Workers
- **Python**: `asyncio`, threading for I/O
- **Windows/.NET**: `async`/`await`, `Task.Run` for CPU-bound work, `DispatcherQueue` for UI updates

The main/UI thread MUST NOT be blocked.

---

# Concurrency

All lengthy work MUST run on background threads/tasks using platform async primitives. The main/UI thread MUST NOT be blocked. Progress SHOULD be shown (determinate or indeterminate) when the UI is waiting on an async task.

