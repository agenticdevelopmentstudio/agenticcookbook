
| Option | Type | Default | Description |
|---|---|---|---|
| `layoutVariant` | enum (`sidebar`, `tabBar`) | `sidebar` | Sidebar for 4+ categories; tab bar for fewer than 5 categories or when platform convention prefers tabs |
| `sidebarWidth` | range (pt) | 150–220 | Fixed or narrow resizable sidebar width |
| `showCategoryIcons` | Bool | `false` | Whether icons appear beside category names; MUST be approved by the user |
| `initialCategory` | category id | first category | Category selected when the browser appears |
| `persistenceBackend` | interface | platform default | Storage backend behind the persistence abstraction (`UserDefaults`, SQLite, registry, `localStorage`) |

