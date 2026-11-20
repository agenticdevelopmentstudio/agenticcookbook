
Route types, one `object` and one `data class`:

```kotlin
@Serializable object Home
@Serializable data class Profile(val userId: String)
```

The graph built with the type-safe builders, navigating by passing a route instance:

```kotlin
NavHost(navController, startDestination = Home) {
    composable<Home> { HomeScreen(onOpenProfile = { navController.navigate(Profile(it)) }) }
    composable<Profile> { backStackEntry ->
        val profile: Profile = backStackEntry.toRoute()
        ProfileScreen(profile.userId)
    }
}
```
