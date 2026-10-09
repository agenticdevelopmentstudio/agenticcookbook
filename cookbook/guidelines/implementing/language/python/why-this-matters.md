
Most Python incidents come from a few habits: a shell string built from input, a path compared as text, an exception swallowed too broadly, and an interpreter that imports from the directory it was started in. Writing the safe form each time costs a few characters and removes whole classes of failure.

