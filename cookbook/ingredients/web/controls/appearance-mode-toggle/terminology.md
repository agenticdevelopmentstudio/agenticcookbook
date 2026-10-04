
| Term | Definition |
|------|-----------|
| Appearance mode | One of three values: `auto`, `dark`, `light` |
| System appearance | The OS-level dark/light preference reported by `prefers-color-scheme` |
| Resolved appearance | The actual dark or light appearance applied to the page — either from the system (auto) or from the forced mode |
| Site settings | The consuming site's persistence mechanism for user preferences (not specified by this recipe) |
| Forced mode | Either `dark` or `light` — an explicit override of the system appearance |
| System theme state | A cached copy of the current system appearance, kept in sync by an always-on listener |

