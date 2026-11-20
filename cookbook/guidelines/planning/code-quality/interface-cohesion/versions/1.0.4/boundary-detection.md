
1. **Protocol/interface + implementors form one unit.** If a file defines a protocol and a second file is its primary concrete implementation, they belong in the same scope group unless the implementation is independently large enough to warrant separation (50+ files).
2. **Barrel files define the interface boundary.** Everything a barrel re-exports is part of the same public surface. If the barrel re-exports from five subdirectories, those subdirectories share an interface and are candidates for a single scope group — unless they are large enough to warrant separate groups that share a common API layer.
3. **Shared types follow their primary consumer, not their definition file.** A `UserProfile` struct defined in `Models/` but used only by the `Auth` module belongs in the `Auth` scope group.
4. **Fragmented interfaces are a smell.** If the same logical interface is declared across three files with no organizing barrel, note this as a cohesion anomaly — it indicates the public surface has not been intentionally designed.
5. **Internal helpers are not interface.** Private/internal/file-private symbols do not contribute to interface cohesion; they contribute to implementation cohesion analyzed by `dependency-clusters`.

