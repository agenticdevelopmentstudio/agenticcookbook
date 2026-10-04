
A centralized logging infrastructure pattern that defines a single enum or struct (e.g., `enum Log`) with static `Logger` instances per category, all sharing one subsystem. Provides clean call-site syntax such as `Log.project.info("message")`. This is the implementation pattern for Rule 9 (instrumented logging). Every feature area gets its own named category so that log output can be filtered by subsystem + category in Console.app, Logcat, or browser dev tools.

