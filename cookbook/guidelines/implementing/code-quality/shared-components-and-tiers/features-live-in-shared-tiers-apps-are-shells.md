
- A feature's models, service protocol, client, storage, logic and views go into the repo's existing shared tiers. Any application (a GUI, a daemon, a command-line tool) then assembles the feature from them.
- What legitimately stays in an application: the entry point, config files, and aggregation code, meaning menu assembly, dependency wiring, and thin adapters that bind a shared protocol to that application's data or transport.
- Split a feature by what each piece needs. Models and pure logic go to the foundation, persistence to the storage tier, views to the UI tier, transport clients to the IPC tier, and only the glue stays in the app.
- If a feature exists only in app code, no other app can use it, and the next app will rebuild it.

