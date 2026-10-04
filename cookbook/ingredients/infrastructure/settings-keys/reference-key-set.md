
The following keys are extracted from the scratching-post reference implementation and represent the minimum initial key set:

### general

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `startupBehavior` | `general.startupBehavior` | String | What to show on app launch (e.g., welcome, last project) |
| `defaultShellPath` | `general.defaultShellPath` | String | Path to the default shell executable |
| `newSessionDefault` | `general.newSessionDefault` | String | Default session type for new terminals |
| `reopenProjectsOnLaunch` | `general.reopenProjectsOnLaunch` | Bool | Whether to restore open projects on launch |
| `openProjectURLs` | `general.openProjectURLs` | [String] | List of project URLs to reopen |
| `maxScanWorkers` | `general.maxScanWorkers` | Int | Maximum concurrent file scan workers |

### ai

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `enabled` | `ai.enabled` | Bool | Whether AI features are enabled |
| `provider` | `ai.provider` | String | AI service provider identifier |
| `apiKey` | `ai.apiKey` | String | API key for the AI provider |
| `model` | `ai.model` | String | AI model name/identifier |

### profiles

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `activeProfileID` | `profiles.activeProfileID` | String (UUID) | ID of the currently active color profile |

### settings

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `sidebarWidth` | `settings.sidebarWidth` | Double | Width of the settings window sidebar in points |

