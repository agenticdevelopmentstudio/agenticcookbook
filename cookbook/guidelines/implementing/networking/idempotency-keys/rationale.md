
- `must-reject-a-reused-key-with-new-parameters`: Failing fast here surfaces a client bug instead of double-charging.
- `should-finalize-after-commit`: Recording the key before the operation succeeds risks replaying a response for work that never happened.
