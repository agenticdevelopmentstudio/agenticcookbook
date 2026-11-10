
- Deriving the key from a timestamp or auto-increment — low entropy invites collisions.
- Treating a `409`/`422` from key handling as a transient error and retrying blindly (see [adc.guideline.implementing.networking.retry-and-resilience](cookbook:cef41f52-bfc6-4ff0-bb67-eb52521c7391)).
- Caching only the status code and not the body, so a replay returns an incomplete response.

