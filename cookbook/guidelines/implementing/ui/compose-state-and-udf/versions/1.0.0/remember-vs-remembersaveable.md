
| API | Survives recomposition | Survives config change / process death | Use for |
|-----|------------------------|----------------------------------------|---------|
| `remember { ... }` | Yes | No | Transient UI state recomputable on the spot |
| `rememberSaveable { ... }` | Yes | Yes (via saved-instance `Bundle`) | UI state a user would be annoyed to lose on rotation |

- Use `rememberSaveable` for state that **SHOULD** survive rotation or process death (entered text, selected tab) when it does not belong in a `ViewModel`.
- Values stored in `rememberSaveable` **MUST** be `Bundle`-serializable or supplied with a custom `Saver`.
- `remember` **MUST NOT** be relied on across configuration changes — it is cleared when the composable leaves composition.

