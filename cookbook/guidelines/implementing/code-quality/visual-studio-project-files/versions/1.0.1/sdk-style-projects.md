
- Every project MUST use an SDK-style `.csproj` whose root element is `<Project Sdk="Microsoft.NET.Sdk">` (or the SDK that matches the project type). The SDK imports its props and targets implicitly.
- A project MUST NOT list source files. The SDK includes `Compile`, `EmbeddedResource` and `None` items by glob and leaves out `bin` and `obj`. Listing a default item again fails with error NETSDK1022. An item MUST be added only to include something the glob misses, and `Remove` MUST be used to exclude.
- Code MUST NOT hand-edit the old-style project format. Convert it.
- Implicit global usings (from .NET 6) are an SDK feature; a project SHOULD turn them on or off explicitly with a property rather than relying on a template.

