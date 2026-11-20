
### When to Use a Script

- File scaffolding (creating directories, copying templates, writing boilerplate)
- Git operations (commits, branch creation, status checks)
- Build and lint commands (compile, format, type-check)
- File manipulation (search-and-replace, moving files, generating indexes)
- Environment setup (installing dependencies, checking prerequisites)
- Metrics collection (counting lines, measuring file sizes, generating reports)

### When the Model Is Still Needed

- Decisions that require judgment or context (what to name something, which approach to take)
- Content generation (writing code, documentation, review comments)
- Analysis that requires understanding (identifying gaps, evaluating tradeoffs)
- Adapting to unexpected situations (error diagnosis, recovery strategies)

### How to Apply

- **In skills**: The skill invokes the script via Bash, then uses the model for the steps that need judgment.
- **In hooks**: Hooks are already shell commands — they're the natural home for deterministic automation.
- **In agents**: An agent that runs `wc -l` is faster than one that reads a file and counts lines.

