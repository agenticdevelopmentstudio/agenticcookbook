
- When you replace an implementation, you MUST delete the one it replaces in the same change. Do not leave old and new side by side, and do not park the old one behind a flag that is permanently off.
- Do the deletion as you go, not as a cleanup pass you plan to do later. A planned cleanup that never happens is the usual way dead paths survive.
- Delete the old tests with the old code, and move any behavior they pinned that still matters onto the new path.

