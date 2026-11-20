
| Platform | Generated form | Example |
|----------|----------------|---------|
| swift | Swift constants | `Color`, `CGFloat` static lets in an enum/extension |
| kotlin | Compose values | `Color`, `Dp`, `TextStyle` in an `object` |
| typescript / web | CSS custom properties + TS consts | `--color-accent`, exported token map |
| csharp | WinUI `ResourceDictionary` | `<Color x:Key="...">`, `<x:Double x:Key="...">` |

- Each output **SHOULD** be code-generated, committed (or published as an artifact), and clearly marked "do not edit by hand" with a generated-file header.
- Naming **MUST** be derived deterministically from token paths so the same token resolves to a predictable symbol on every platform.
- Semantic/alias tokens (`color.surface.primary`) **SHOULD** be exposed to product code; raw/primitive tokens (`palette.blue.500`) **SHOULD NOT** be referenced directly in features (per explicit-over-implicit).

