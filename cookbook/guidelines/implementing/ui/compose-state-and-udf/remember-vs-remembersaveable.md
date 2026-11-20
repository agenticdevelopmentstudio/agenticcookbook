
| API | Survives recomposition | Survives config change / process death | Use for |
|-----|------------------------|----------------------------------------|---------|
| `remember { ... }` | Yes | No | Transient UI state recomputable on the spot |
| `rememberSaveable { ... }` | Yes | Yes (via saved-instance `Bundle`) | UI state a user would be annoyed to lose on rotation |
