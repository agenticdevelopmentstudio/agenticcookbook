
- `should-convert-cold-upstream-with-statein`: `stateIn` gives the production pipeline lifecycle control tied to subscription.
- `should-start-while-subscribed-5000`: The 5-second stop timeout keeps the upstream alive across configuration changes and short app-switches while still tearing it down when the UI is truly gone.
- `must-collect-lifecycle-aware`: Collecting a `StateFlow` does NOT auto-stop when the UI goes to the background — unlike `LiveData.observe()`.
- `should-inject-dispatchers`: Hardcoded dispatchers cannot be swapped for a test dispatcher, making suspend logic flaky or untestable.
