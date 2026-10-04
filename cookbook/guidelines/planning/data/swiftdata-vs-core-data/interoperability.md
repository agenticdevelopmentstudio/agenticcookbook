
- The two **can coexist in one app** over the same store, enabling incremental adoption.
- Teams **MAY** introduce SwiftData for new models in a Core Data app, or expose a Core Data stack to SwiftData, rather than performing a big-bang rewrite.
- When interoperating, the underlying schema **MUST** stay compatible across both layers; validate with migration tests before shipping.

