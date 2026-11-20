
- `should-use-mvvm-with-community-toolkit`: view models built on CommunityToolkit.Mvvm (`[ObservableObject]`, `[ObservableProperty]`, `[RelayCommand]`, messaging) rather than hand-written `INotifyPropertyChanged` and command classes
- `should-use-navigationview-and-frame`: page-level navigation hosted in a NavigationView with a Frame, not another navigation scheme
- `should-put-navigation-service-in-viewmodel-layer`: view models navigate through an injected navigation service interface
- `must-not-manipulate-frame-from-code-behind`: any `Frame.Navigate`, `Frame.GoBack` or other `Frame` call in a page's code-behind
- `should-scaffold-with-template-studio`: a project scaffolded with Template Studio, or a hand-built scaffold that re-creates its MVVM, navigation and theming wiring
