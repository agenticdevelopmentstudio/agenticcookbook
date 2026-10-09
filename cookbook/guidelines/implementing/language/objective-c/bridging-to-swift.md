
- Design the Objective-C API so it needs no Swift-side fix-ups: declare generics on collections (`NSArray<MyListItem *> *`) so Swift sees `[MyListItem]`, and use designated nullability.
- When the Swift form should differ from the Objective-C form (a tuple instead of out-parameters, reordered or renamed arguments), mark the Objective-C declaration `NS_REFINED_FOR_SWIFT` and write the Swift-facing API in a Swift extension. The original is imported with a double underscore prefix (`__getRed(red:green:blue:alpha:)`), which keeps it out of ordinary autocompletion.
- Keep the Objective-C implementation as the single source of behavior. The refined Swift API calls it; it does not reimplement it.

