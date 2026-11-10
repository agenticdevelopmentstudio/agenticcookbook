
**Decision**: Compose the project window from a dedicated split-layout ingredient plus the existing panel, header, status-bar, frame-persistence, and logging ingredients instead of one monolithic window spec.
**Rationale**: Each panel keeps a single owner (design-for-deletion); the window recipe states only how they wire together, so a panel can be replaced without touching the layout.
**Approved**: pending

