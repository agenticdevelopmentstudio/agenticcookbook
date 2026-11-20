
```kotlin
// Stateless: state down, events up
@Composable
fun NameField(name: String, onNameChange: (String) -> Unit) {
    OutlinedTextField(value = name, onValueChange = onNameChange, label = { Text("Name") })
}
```

```kotlin
class ProfileViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()
}
// In the composable:
val state by viewModel.uiState.collectAsStateWithLifecycle()
```
