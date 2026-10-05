
| State | Behavior |
|-------|----------|
| Idle | No scan in progress |
| Full sync in progress | Top-level directories are being scanned in parallel on a background queue |
| Surgical update in progress | Children of affected directories are being reloaded on a background queue |
| Complete | A new tree or a set of replacement children has been produced for the caller to apply |

