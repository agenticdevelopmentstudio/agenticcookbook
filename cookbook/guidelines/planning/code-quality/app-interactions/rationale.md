
- `should-scope-component-with-its-delegate-protocol`, `may-scope-delegate-implementations-elsewhere`: A component with a clean delegate protocol is designed to be replaceable — the delegate protocol IS the interface.
- `should-identify-notification-observers`: Files that observe a posted notification are implicitly coupled even if they have no import relationship. High use of notifications across many files indicates missing formal interfaces.
- `should-flag-cross-group-singletons`: Any file that accesses a singleton is implicitly coupled to every other file that accesses the same singleton.
- `should-split-scope-groups-at-di-registration`: The DI container registration site is the architectural seam — it is where modules are wired together.
- `should-document-store-slices-per-group`: Global state (Redux, MobX, Context) makes boundaries fuzzy. If all components read from a single global store, module boundaries are implicitly bypassed.
- `should-note-notification-endpoints`: Each notification is an implicit coupling between poster and observer.
