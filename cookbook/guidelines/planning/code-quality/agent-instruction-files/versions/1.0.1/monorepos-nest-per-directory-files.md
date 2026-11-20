
- For multi-package repos you **SHOULD** place a scoped instruction file inside each package. Agents read the **nearest** file up the directory tree, so the closest one takes precedence over the root file.
- The root file **SHOULD** hold repo-wide guidance; nested files **SHOULD** hold only what differs for that package, to avoid duplication.

