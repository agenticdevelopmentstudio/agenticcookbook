
| State | Behavior |
|-------|----------|
| NSOpenPanel displayed | User is selecting a directory for New Project. Other menu commands are blocked by the modal panel |
| NSSavePanel displayed | User is choosing a save location for New Workspace. Other menu commands are blocked by the modal panel |
| Directory validation failed | Error alert displayed with reason. User can dismiss and retry |
| Existing package found | Package at expected path is opened instead of creating a duplicate |
| Document creation in progress | Package is being created on disk. Menu command is non-reentrant (no double-creation) |
| Document open failed | Error alert displayed with failure reason. No document window opens |

