
# Architecture

Use MVVM with [CommunityToolkit.Mvvm](https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/) — source-generated `ObservableObject`, `RelayCommand`, and messaging.

- NavigationView + Frame SHOULD be used for page-level navigation
- Navigation service abstraction in the ViewModel layer — code-behind MUST NOT manipulate Frame directly
- Use [Template Studio](https://github.com/microsoft/TemplateStudio) for project scaffolding with MVVM, navigation, and theming pre-wired

```csharp
// ViewModel with CommunityToolkit.Mvvm source generators
[ObservableObject]
public partial class MainViewModel
{
    [ObservableProperty]
    private string _title = "Home";

    [RelayCommand]
    private async Task LoadDataAsync()
    {
        var data = await _dataService.FetchAsync();
        Title = data.Name;
    }
}
```

