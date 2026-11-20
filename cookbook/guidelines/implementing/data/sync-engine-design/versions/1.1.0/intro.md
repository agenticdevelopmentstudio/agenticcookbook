
# Sync Engine Design

The sync engine is the client-side component that orchestrates all synchronization: collecting dirty records, sending them to the server, receiving server changes, applying them locally, and managing retry and scheduling. A well-designed engine is entity-agnostic — adding a new synced entity type requires minimal new code.

