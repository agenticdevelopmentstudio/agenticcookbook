
- Delegate and data-source properties are `weak` (or `unowned(unsafe)` on old APIs) so the owner does not keep its delegate alive and the delegate does not keep its owner alive.
- Define a delegate as a protocol with narrow, named callbacks. Optional methods are acceptable in Objective-C protocols; in Swift prefer a small required protocol plus default extension methods.
- A delegate callback is a notification that something happened or a request for a decision. Do not use it to move large state between objects; pass a value or use a closure for a single reply.

