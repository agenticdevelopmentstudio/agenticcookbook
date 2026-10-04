
# System Interactions

The operating system is not passive. It invokes callbacks, manages process lifecycle, delivers notifications, routes URLs, and terminates background work. Code that participates in OS-managed lifecycles has a fundamentally different structure than code that runs only when explicitly called. This lens identifies where the codebase touches the OS boundary — not to use system frameworks (see `system-dependencies`), but to participate in OS-managed communication, lifecycle, and integration protocols.

