
- The solution SHOULD be managed with `dotnet sln` (`add`, `list`, `remove`, `migrate`) rather than hand edits. Accepted formats are `.sln`, `.slnx` and the filtered `.slnf`; from .NET 10 `dotnet new sln` produces `.slnx`, before that `.sln`.
- There SHOULD be one solution per deployable unit, and it MUST list every project, so a clean checkout builds.
- A project or solution file MUST NOT contain anything machine-specific (absolute paths, user folders).

