<!-- leaf: implement-ui/android-navigation · source: guidelines/implementing/ui/android-navigation.md -->

**Rules** (cite as `implement-ui/android-navigation#<slug>`):

- `app-use-single-activity-architecture` MUST — The app MUST use a single-activity architecture: one Activity hosts the Compose UI; screens are composables, not …
- `navigation-state-navhostcontroller-created-once-top-ui` SHOULD — Navigation state (the NavHostController) SHOULD be created once at the top of the UI tree via rememberNavController() …
- `screen-composables-not-read-mutate-back-stack` MUST — Screen composables MUST NOT read or mutate the back stack directly; they emit navigation events upward. This follows …
- `routes-serializable-kotlin-types-raw` MUST — Routes MUST be @Serializable Kotlin types, not raw strings: an object for argument-free destinations, a data class for …
- `arguments-passed-through-route-type` MUST — Arguments MUST be passed through the route type and read with toRoute(); do NOT concatenate path strings or hand-parse …
- `viewmodels-receive-route-arguments-via` SHOULD — ViewModels SHOULD receive route arguments via SavedStateHandle.toRoute<Route>() rather than being handed a …
- `deep-links-declared-per-destination-deeplinks` SHOULD — Deep links SHOULD be declared per destination (deepLinks = listOf(navDeepLink<Profile>(...))) so the same type-safe …
- `surviving-process-death-handled-route-types-saved` MUST — Surviving process death MUST be handled: route types are saved automatically because they are serializable; additional …
- `stack-scoped-state-use-viewmodel-scoped-navbackstackentry` SHOULD — Back-stack-scoped state SHOULD use viewModel() scoped to the NavBackStackEntry so a ViewModel is cleared when its …

# Android navigation in Compose

Drive navigation in a Jetpack Compose app with a single activity, a type-safe navigation graph, and navigation state hoisted out of composables. Define destinations as `@Serializable` route types so argument errors fail at compile time, not at runtime.

## Architecture

- The app **MUST** use a single-activity architecture: one `Activity` hosts the Compose UI; screens are composables, not separate activities.
- Navigation state (the `NavHostController`) **SHOULD** be created once at the top of the UI tree via `rememberNavController()` and passed down, or wrapped in narrow callbacks (`onNavigateToProfile: (id) -> Unit`) so leaf composables stay navigation-agnostic and testable.
- Screen composables **MUST NOT** read or mutate the back stack directly; they emit navigation events upward. This follows unidirectional data flow — see `agenticdevelopercookbook://guidelines/implementing/ui/compose-state-and-udf`.

## Default: type-safe Navigation Compose (Nav2)

Use the stable type-safe APIs in `androidx.navigation:navigation-compose` (type-safe routes are stable as of 2.8.0; pin a current `2.9.x` build and apply the `kotlinx-serialization` Gradle plugin).

- Routes **MUST** be `@Serializable` Kotlin types, not raw strings: an `object` for argument-free destinations, a `data class` for destinations with arguments.

  ```kotlin
  @Serializable object Home
  @Serializable data class Profile(val userId: String)
  ```

- Build the graph with the type-safe builders and navigate by passing a route instance:

  ```kotlin
  NavHost(navController, startDestination = Home) {
      composable<Home> { HomeScreen(onOpenProfile = { navController.navigate(Profile(it)) }) }
      composable<Profile> { backStackEntry ->
          val profile: Profile = backStackEntry.toRoute()
          ProfileScreen(profile.userId)
      }
  }
  ```

- Arguments **MUST** be passed through the route type and read with `toRoute()`; do **NOT** concatenate path strings or hand-parse `NavBackStackEntry.arguments`.
- ViewModels **SHOULD** receive route arguments via `SavedStateHandle.toRoute<Route>()` rather than being handed a `NavController`.
- Deep links **SHOULD** be declared per destination (`deepLinks = listOf(navDeepLink<Profile>(...))`) so the same type-safe route drives both in-app and external entry.

## Navigation 3 (Nav3) — newer option, adopt deliberately

`androidx.navigation3` reached 1.0 stable on 2025-11-19. Pin a current `1.x` release before relying on it; APIs and supporting libraries (e.g. `material3-adaptive-navigation3`) are still maturing, so treat specific surface details as evolving (FORECAST) and re-check the release notes.

- Nav3 models the back stack as a plain observable `List` of keys (a `SnapshotStateList`) that you mutate directly (`backStack.add(key)` / `removeLastOrNull()`); `NavDisplay` renders the top entries. This makes the back stack first-class app state.
- Choose Nav3 as a **deliberate decision** when you need full control over the back stack, multi-pane/adaptive layouts, or custom transitions — not as a blanket mandate. Navigation Compose (Nav2) remains supported and is a correct default for most apps.
- Do **NOT** mix Nav2 `NavHost` and Nav3 `NavDisplay` for the same flow; pick one model per navigation graph and migrate a flow at a time.

## State and lifecycle

- Surviving process death **MUST** be handled: route types are saved automatically because they are serializable; additional UI state goes in `SavedStateHandle` or `rememberSaveable`.
- Back-stack-scoped state **SHOULD** use `viewModel()` scoped to the `NavBackStackEntry` so a ViewModel is cleared when its destination leaves the stack.
- Use a single `startDestination`; avoid clearing and rebuilding the entire graph to navigate — prefer `popUpTo`/`launchSingleTop` (Nav2) or list operations (Nav3).
