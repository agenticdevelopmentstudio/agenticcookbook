
# Progressive Web App installability

This guideline applies only when an **installable** web app is in scope. An installable app SHOULD ship a Web App Manifest and a service worker with an explicit caching strategy, and MUST account for iOS/Safari limitations. If installability is not a requirement, do not add a service worker for its own sake (YAGNI).

