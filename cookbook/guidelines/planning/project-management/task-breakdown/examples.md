
*This section is informative.*

A task too large and too vague to act on:

```text
Internet integration                       (estimate: 3 weeks)
```

The same work broken down. Each task is small, names a visible action and carries a done test:

```text
Title:     Add the "Sign in with GitHub" button to the login page
Action:    Render the button and wire it to the OAuth start endpoint
Done when: - The button appears on /login for signed-out users
           - Clicking it redirects to github.com/login/oauth/authorize
           - The existing email sign-in still passes its tests
Expect:    about half a day
Milestone: Beta sign-up
```

A layer split, and a vertical split of the same story:

```text
By layer (avoid):   "Build the export UI"  /  "Add the export table"  /  "Write the export API"
Vertical slices:    "Export one report as CSV"  /  "Export a filtered report"  /  "Schedule a weekly export"
```

A blocked task:

```text
Blocked by:  #412 Rotate the staging OAuth secret
Note:        Waiting on the new client secret from the identity team; sign-in fails without it.
Blocked:     2026-11-20 -> 2026-11-22
```

