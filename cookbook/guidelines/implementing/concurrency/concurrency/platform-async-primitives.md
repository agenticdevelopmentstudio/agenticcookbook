
The platform concurrency (async) primitives for background work:

- **Apple**: Swift Concurrency (`async`/`await`, `Task`, actors)
- **Android**: Kotlin Coroutines (`viewModelScope`, `Dispatchers.IO`)
- **Web**: `Promise`/`async`, Web Workers
- **Python**: `asyncio`, threading for I/O
- **Windows/.NET**: `async`/`await`, `Task.Run` for CPU-bound work, `DispatcherQueue` for UI updates
