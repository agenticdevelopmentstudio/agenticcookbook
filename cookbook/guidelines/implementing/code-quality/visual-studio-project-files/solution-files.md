
- Manage the solution with `dotnet sln` (`add`, `list`, `remove`, `migrate`) rather than hand edits. Accepted formats are `.sln`, `.slnx` and the filtered `.slnf`; from .NET 10 `dotnet new sln` produces `.slnx`, before that `.sln`.
- Keep one solution per deployable unit and list every project in it, so a clean checkout builds.
- Nothing machine-specific (absolute paths, user folders) belongs in a project or solution file.

