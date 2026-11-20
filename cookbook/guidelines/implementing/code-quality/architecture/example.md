
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
