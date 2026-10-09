
- Name methods so a call site reads as a phrase, with a label for every argument after the first. Follow the conventions of the framework you extend rather than inventing new vocabulary.
- Prefix every public class, protocol, enum and constant with a project prefix, because Objective-C has no namespaces.
- Mark designated initializers (`NS_DESIGNATED_INITIALIZER`) and forbid inherited ones that cannot work (`NS_UNAVAILABLE`), so a half-initialized object cannot be built.
- Report recoverable failure with a `BOOL` or object return plus an `NSError **` out-parameter, not with exceptions. Exceptions are for programmer errors.

