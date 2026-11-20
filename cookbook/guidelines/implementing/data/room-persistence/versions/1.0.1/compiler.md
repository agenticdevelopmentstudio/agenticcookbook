
- You **MUST** use **KSP** (`androidx.room:room-compiler` via the KSP plugin) for the annotation processor. KAPT is legacy and roughly 2x slower; Room 3.0 removes KAPT support entirely.
- You **SHOULD** enable schema export (`room.schemaLocation`) and commit the generated JSON schema so migrations can be diffed and tested.

