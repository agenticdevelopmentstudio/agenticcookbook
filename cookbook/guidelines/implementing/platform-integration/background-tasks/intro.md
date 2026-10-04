
# Background tasks

Apps that sync data, process uploads, or maintain state SHOULD use platform background execution APIs rather than relying on foreground presence. Background tasks extend the app's usefulness while the user is doing other things.

- Use the platform's sanctioned background APIs — unsanctioned workarounds get killed and drain battery
- Design tasks to be resumable — background execution can be interrupted at any time
- Minimize resource usage — the OS budgets CPU and network time strictly
- Report progress and completion through notifications when appropriate

