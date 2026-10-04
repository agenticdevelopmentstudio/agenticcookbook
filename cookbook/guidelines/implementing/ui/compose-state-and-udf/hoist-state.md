
State hoisting moves state up to a caller, making a composable stateless. A hoisted state-holder pattern replaces a state value with a `value` parameter (flows down) and an `onValueChange` lambda (flows up).

- A reusable composable **SHOULD** be stateless: it takes its state via parameters and emits changes via callback lambdas. This advances `separation-of-concerns` — rendering is decoupled from state ownership.
- State **MUST** be hoisted to the **lowest common ancestor** that reads or writes it — no higher. Hoisting too high causes unnecessary recomposition and couples unrelated subtrees; hoisting too low blocks sharing.
- Screen-level / business state (data loaded from repositories, navigation results, form submission status) **SHOULD** live in a `ViewModel`, not in composition, so it survives configuration changes and process-death restoration.
- Pure UI element state (scroll position, expanded/collapsed, focus, text-field cursor) **MAY** stay in composition via `remember` when no other component needs it.

```kotlin
// Stateless: state down, events up
@Composable
fun NameField(name: String, onNameChange: (String) -> Unit) {
    OutlinedTextField(value = name, onValueChange = onNameChange, label = { Text("Name") })
}
```

