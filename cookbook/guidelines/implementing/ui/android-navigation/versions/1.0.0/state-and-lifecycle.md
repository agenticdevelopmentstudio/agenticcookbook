
- Surviving process death **MUST** be handled: route types are saved automatically because they are serializable; additional UI state goes in `SavedStateHandle` or `rememberSaveable`.
- Back-stack-scoped state **SHOULD** use `viewModel()` scoped to the `NavBackStackEntry` so a ViewModel is cleared when its destination leaves the stack.
- Use a single `startDestination`; avoid clearing and rebuilding the entire graph to navigate — prefer `popUpTo`/`launchSingleTop` (Nav2) or list operations (Nav3).

