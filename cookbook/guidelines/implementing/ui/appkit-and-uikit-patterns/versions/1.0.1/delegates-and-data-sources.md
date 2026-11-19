
- Delegate and data-source properties MUST be `weak` (or `unowned(unsafe)` on old APIs) so the owner does not keep its delegate alive and the delegate does not keep its owner alive.
- A delegate SHOULD be a protocol with narrow, named callbacks. Optional methods are acceptable in Objective-C protocols; in Swift, code SHOULD prefer a small required protocol plus default extension methods.
- A delegate callback is a notification that something happened or a request for a decision. A delegate callback MUST NOT move large state between objects; code SHOULD pass a value or use a closure for a single reply.

