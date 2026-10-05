
**Decision**: Open an existing project package instead of creating a duplicate when one exists at the expected path.
**Rationale**: One project directory maps to one package; creating duplicates would split project state.
**Approved**: pending

**Decision**: Require a `.git` directory for New Project.
**Rationale**: A Git repository is the unit a project package wraps; failing early with a clear alert avoids creating a package around a non-repository.
**Approved**: pending

