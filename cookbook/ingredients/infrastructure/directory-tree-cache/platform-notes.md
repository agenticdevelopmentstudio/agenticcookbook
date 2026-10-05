
- **SwiftUI (macOS)**: For atomic cache writes, write to a `.tmp` file in the same directory then use `FileManager.moveItem(at:to:)`, which is atomic on APFS/HFS+. Load and save on a background `DispatchQueue`.
- **SwiftUI (iOS / visionOS)**: Cache loading and saving work identically via `FileManager`.
- **Compose / React/Web**: Not applicable — this ingredient targets Apple platforms and TypeScript services; a web or Android implementation would use the platform's atomic-rename primitive in the same way.

