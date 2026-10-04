
```
╔══════════════════════════════════════════════════╗
║                                                  ║
║           ☠  HERE BE DRAGONS  ☠                  ║
║                                                  ║
║  Yolo mode auto-approves ALL permission prompts  ║
║  with zero safety checks.                        ║
║                                                  ║
║  This means Claude can:                          ║
║    • Run any shell command                       ║
║    • Edit or delete any file                     ║
║    • Push to any remote                          ║
║    • Do anything — without asking                ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

This recipe provides the same security posture as `--dangerously-skip-permissions`: **none**. It is intended for trusted local development environments where the user is actively monitoring Claude's output. It offers no protection against prompt injection, destructive commands, or unintended side effects.

**Do not use this in:**
- Shared CI/CD environments
- Production systems
- Environments with access to sensitive credentials or infrastructure
- Sessions where untrusted content (PRs, issues, external files) will be processed

