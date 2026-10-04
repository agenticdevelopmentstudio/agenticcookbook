
# Choose SwiftData vs Core Data

SwiftData and Core Data are both first-party Apple object-graph persistence frameworks backed by SQLite. SwiftData (`@Model`, Swift-native, built on top of the Core Data stack) is the modern default for new apps on recent OS versions; Core Data remains the right choice for fine-grained control, complex migrations, lower OS-version floors, or Objective-C interop. Make this a **deliberate decision**, not a reach for the newest API.

