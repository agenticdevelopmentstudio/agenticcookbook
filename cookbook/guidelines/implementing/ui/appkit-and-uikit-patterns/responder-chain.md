
- Events and action messages travel a chain of responders. A view that does not handle an event passes it to its superview; a view controller sits in the chain between its root view and that view's superview; the window and then the application object come after.
- A control whose target is `nil` sends its action up the chain until an object implements the method. Use that for commands that belong to whoever is frontmost (copy, delete, undo), and set an explicit target for commands that belong to one object.
- Implement an action on the object that owns the behavior, usually the view controller, not on a distant object reached through a stored reference.
- To insert an object into the chain, override `nextResponder` and return it. Do this sparingly; the default chain is what users and the system expect.
- A gesture recognizer sees touches before its view does. If it fails to recognize them, the view gets them.

