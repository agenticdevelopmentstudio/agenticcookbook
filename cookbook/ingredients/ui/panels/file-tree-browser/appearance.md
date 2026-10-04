
### Row layout

```
┌──────────────────────────────────────────────┐
│  📁 Sources                              M   │
│    📄 App.swift                          A   │
│    📄 ContentView.swift                  M   │
│  📁 Tests                                    │
│  📦 MyPlugin.catnip-proj                     │
│  📄 Package.swift                            │
│  📄 README.md                                │
│  📄 .gitignore                               │
└──────────────────────────────────────────────┘
```

- **Row content**: Icon (colored per type) + file name + optional git status badge (right-aligned)
- **File name**: Single line, truncated with middle truncation if too long
- **Tooltip**: Full path of the entry
- **Icon size**: Body-scaled SF Symbol
- **List style**: `.sidebar` on Apple platforms

### Icon theming

#### Packages

| Pattern | SF Symbol | Color |
|---------|-----------|-------|
| Any recognized package directory | `shippingbox.fill` | Orange |

#### Special directories

| Pattern | SF Symbol | Color |
|---------|-----------|-------|
| `.claude` | `brain` | Accent |
| `.git` | `arrow.triangle.branch` | Accent |
| `Sources` or `src` | `folder.fill.badge.gearshape` | Accent |
| `Tests` or `test` | `folder.fill.badge.questionmark` | Accent |
| Dotfile directories (other than above) | `folder.badge.gearshape` | Accent |

#### Files by extension

| Extension(s) | SF Symbol | Color |
|--------------|-----------|-------|
| `.swift` | `swift` | Orange |
| `.json` | `curlybraces` | Yellow |
| `.md`, `.markdown` | `doc.richtext` | Blue |
| `.yaml`, `.yml`, `.toml` | `gearshape.2` | Secondary |
| `.sh`, `.bash`, `.zsh` | `terminal` | Secondary |
| `.py`, `.js`, `.ts`, `.rb` | `chevron.left.forwardslash.chevron.right` | Secondary |

#### Defaults

| Type | SF Symbol | Color |
|------|-----------|-------|
| Directory (no special match) | `folder.fill` | Accent |
| File (no extension match) | `doc` | Secondary |

