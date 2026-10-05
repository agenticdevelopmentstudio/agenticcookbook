
- **Quit during document save**: The app MUST wait for in-progress saves to complete before terminating child processes. This is handled by the document subsystem's save-on-close behavior.
- **Quit with no open documents and children running**: The empty URL list MUST be saved (clearing the previous restore list) and children MUST still be terminated.
- **Mode `nothing` with a relaunch that restores nothing**: No window opens and the empty URL list MUST NOT be treated as a restore failure.

