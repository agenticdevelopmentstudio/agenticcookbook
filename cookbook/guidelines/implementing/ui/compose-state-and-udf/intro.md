
# Jetpack Compose: state hoisting and unidirectional data flow

In Jetpack Compose, **state flows down and events flow up** (unidirectional data flow, UDF). Hoist state out of composables to the lowest common owner that needs it — or to a `ViewModel` for screen-level state — and keep individual composables stateless where practical. This is the most stable consensus in modern Android UI and the foundation every other Compose decision rests on.

