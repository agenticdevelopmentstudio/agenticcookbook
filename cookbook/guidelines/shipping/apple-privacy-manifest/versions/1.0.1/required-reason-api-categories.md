
An agent can call these unknowingly through ordinary Foundation usage. Each category has its own `NSPrivacyAccessedAPIType` string and a fixed set of allowed reason codes (`NSPrivacyAccessedAPITypeReasons`):

| Category | Common triggers an agent writes | Manifest API type |
|---|---|---|
| File timestamp | `attributesOfItem`, `contentModificationDate`, `creationDate`, `stat`, `getattrlist` | `NSPrivacyAccessedAPICategoryFileTimestamp` |
| System boot time | `systemUptime`, `mach_absolute_time` for boot-relative timing | `NSPrivacyAccessedAPICategorySystemBootTime` |
| Disk space | `volumeAvailableCapacityKey`, `statfs`, free-space checks | `NSPrivacyAccessedAPICategoryDiskSpace` |
| Active keyboard | reading the user's active keyboard list | `NSPrivacyAccessedAPICategoryActiveKeyboards` |
| User defaults | `UserDefaults` / `NSUserDefaults` access | `NSPrivacyAccessedAPICategoryUserDefaults` |

- You **MUST** declare every category your own code reaches, with at least one valid reason code per category. Invented reason codes are rejected — use only codes Apple lists for that category (see TN3183).
- You **MUST NOT** add a category you do not actually use to "be safe"; declarations are scoped to real usage.

