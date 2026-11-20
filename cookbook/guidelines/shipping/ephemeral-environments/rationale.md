
- `must-recreate-state-from-iac`, `should-keep-environments-cheap-and-short-lived`, `must-remove-every-namespaced-resource`: These environments are throwaway by design (per *design-for-deletion*). These rules prevent drift into long-lived "pets".
