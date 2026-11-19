
- Every write to a shared directory is preceded by an existence check.
- A same-name file that the installer did not create is skipped and reported, never replaced, truncated or deleted.
- Identical content is a no-op, and a second run reports nothing new.

