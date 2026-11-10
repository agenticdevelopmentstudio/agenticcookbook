
**Decision**: Document creation flows are in `menu-commands.md`, not in this recipe.
**Rationale**: This spec covers the read/write/migration lifecycle of package documents. The "New Project" and "New Workspace" creation flows (NSOpenPanel, git validation, NSSavePanel) are specified by the Document Creation Flow ingredient (`agenticdevelopercookbook://ingredients/app/document-creation-flow`), composed by the Menu Commands recipe, since they involve menu command structure and file picker UX, not just persistence.
**Approved**: pending

**Decision**: Split the pattern into a document type, a storage format, and a SQLite helper layer.
**Rationale**: The helpers are reusable by any code that touches SQLite, the storage format varies per document kind while the document type scaffolding repeats, and each layer can change without touching the others.
**Approved**: pending

