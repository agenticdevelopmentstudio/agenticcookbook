
Linting MUST run as part of the automated verification process:
- **During development** — as part of the build or pre-commit hook
- **In CI** — linting failures MUST block the build alongside test failures
- **After code generation** — AI-generated code MUST pass linting before being accepted

