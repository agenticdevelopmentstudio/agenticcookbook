<!-- leaf: implement-code-quality/architecture · source: guidelines/implementing/code-quality/architecture.md -->

**Rules** (cite as `implement-code-quality/architecture#<slug>`):

- `navigationview-frame-used-page-level-navigation` SHOULD — NavigationView + Frame SHOULD be used for page-level navigation
- `layer-code-behind-not-manipulate-frame-directly` MUST — Navigation service abstraction in the ViewModel layer — code-behind MUST NOT manipulate Frame directly

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
