
Subsystem: `{{bundle_id}}` | Category: `MenuCommands`

| Event | Level | Message |
|-------|-------|---------|
| New Project initiated | info | `MenuCommands: "New Project" initiated` |
| NSOpenPanel presented | debug | `MenuCommands: NSOpenPanel presented for directory selection` |
| NSOpenPanel cancelled | debug | `MenuCommands: NSOpenPanel cancelled by user` |
| Directory selected | debug | `MenuCommands: directory selected: "{{path}}"` |
| Directory validation passed | debug | `MenuCommands: directory validation passed for "{{path}}"` |
| Directory validation failed (no .git) | warning | `MenuCommands: directory validation failed — no .git found in "{{path}}"` |
| Directory validation failed (permissions) | warning | `MenuCommands: directory validation failed — cannot access "{{path}}": {{error}}` |
| Existing package found | info | `MenuCommands: existing package found at "{{packagePath}}", opening instead of creating` |
| Package creation started | debug | `MenuCommands: creating project package at "{{packagePath}}"` |
| Package creation succeeded | info | `MenuCommands: project package created at "{{packagePath}}"` |
| Package creation failed | error | `MenuCommands: failed to create project package at "{{packagePath}}": {{error}}` |
| Document opened | info | `MenuCommands: opened document at "{{path}}"` |
| Document open failed | error | `MenuCommands: failed to open document at "{{path}}": {{error}}` |
| New Workspace initiated | info | `MenuCommands: "New Workspace" initiated` |
| NSSavePanel presented | debug | `MenuCommands: NSSavePanel presented for workspace creation` |
| NSSavePanel cancelled | debug | `MenuCommands: NSSavePanel cancelled by user` |
| Workspace creation started | debug | `MenuCommands: creating workspace package at "{{path}}"` |
| Workspace creation succeeded | info | `MenuCommands: workspace package created at "{{path}}"` |
| Workspace creation failed | error | `MenuCommands: failed to create workspace package at "{{path}}": {{error}}` |
| Error alert presented | debug | `MenuCommands: error alert presented — "{{title}}": "{{message}}"` |

