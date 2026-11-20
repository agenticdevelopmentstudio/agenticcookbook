
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

