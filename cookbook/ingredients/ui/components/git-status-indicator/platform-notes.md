
- **SwiftUI**: Status enum with `color: Color` and `displayCharacter: String` computed properties. Use `Text(status.displayCharacter).font(.caption2.monospaced().bold()).foregroundStyle(status.color)`. Git provider runs `Process()` with `git status --porcelain=v1 -uall --ignore-submodules` on a background queue.
- **Compose**: Sealed class with `color: Color` and `char: String` properties. `Text(status.char, color = status.color, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold, fontSize = 10.sp)`.
- **React/Web**: TypeScript enum or union type. `<span style={{ fontFamily: 'monospace', fontWeight: 'bold', color: status.color }}>{status.char}</span>`. Git status via backend API or `simple-git` library in Electron.

