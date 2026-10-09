
- Every file lives inside a directory that names its purpose and belongs to a declared tier. Do not leave source files strewn at the top level of a repo or package.
- Keep a directory cohesive: what is inside changes together and is reached through a small public surface. Details that other code should not touch stay inside it.
- Group by concept, not by file type, so a reader finds a feature in one place.
- When a path belongs to no declared tier, move the file into one. Do not add a tier just to hold it.

