
# Separate server state from client state

Application state is not one thing. **Server state** (remote, asynchronous, cacheable, can go stale without your code touching it) and **client state** (UI toggles, modals, form drafts) have different lifecycles and MUST be managed by different mechanisms. Conflating them — typically by copying fetched data into a global client store — is the most common state-management mistake in web UIs.

This guideline covers *data* state ownership. For PRESENTATION states (loading / empty / error / content rendering), see the UI state-design guideline.

