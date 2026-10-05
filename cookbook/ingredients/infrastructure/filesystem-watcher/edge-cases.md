
- **Rapid filesystem changes**: The 0.5s debounce (debounce-latency) coalesces rapid changes into a single event. If changes arrive faster than the consumer processes them, the consumer SHOULD batch them rather than queue unbounded updates.
- **Network/remote drives**: FSEvents may not work reliably on network-mounted volumes. The watcher SHOULD fall back to periodic polling or disable watch mode for non-local filesystems. Implementors SHOULD detect volume type and adapt.
- **Directory deleted while watching**: The watcher MUST handle the root directory being deleted or unmounted. It SHOULD stop the FSEvents stream and report the removal so the consumer can publish an empty tree.

