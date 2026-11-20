
Same async/await conventions as C# above. For WinUI 3 specifically, marshal UI updates back with `DispatcherQueue.TryEnqueue`.

```csharp
DispatcherQueue.TryEnqueue(() =>
{
    StatusText.Text = "Updated from background";
});
```
