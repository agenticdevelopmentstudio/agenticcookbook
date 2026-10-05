
**Decision**: Write to a temporary SQLite file, read it back as bytes, and hand the bytes to a `FileWrapper`.
**Rationale**: SQLite wants a file path, while `ReferenceFileDocument` wants a `FileWrapper`. Going through a temporary file lets SQLite do what it does best while the document system performs the atomic directory replacement, so an interrupted write never corrupts the existing package.
**Approved**: pending

