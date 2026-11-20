
- Events and action messages travel a chain of responders. A view that does not handle an event passes it to its superview; a view controller sits in the chain between its root view and that view's superview; the window and then the application object come after.
- A gesture recognizer sees touches before its view does. If it fails to recognize them, the view gets them.
