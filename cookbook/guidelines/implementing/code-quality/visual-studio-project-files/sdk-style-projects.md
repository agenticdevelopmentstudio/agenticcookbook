
- Every project uses an SDK-style `.csproj` whose root element is `<Project Sdk="Microsoft.NET.Sdk">` (or the SDK that matches the project type). The SDK imports its props and targets implicitly.
- Do not list source files. The SDK includes `Compile`, `EmbeddedResource` and `None` items by glob and leaves out `bin` and `obj`. Listing a default item again fails with error NETSDK1022. Add an item only to include something the glob misses, and use `Remove` to exclude.
- Do not hand-edit the old-style project format. Convert it.
- Implicit global usings (from .NET 6) are an SDK feature; turn them on or off explicitly with a property rather than relying on a template.

