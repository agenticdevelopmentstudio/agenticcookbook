
The `x:Uid` directive in XAML binds control properties to resource keys.

- `x:Uid="SaveButton"` maps to `SaveButton.Content`, `SaveButton.AutomationProperties.Name`, etc. in the `.resw` file

```xml
<!-- XAML: localized via x:Uid -->
<Button x:Uid="SaveButton" />
```
