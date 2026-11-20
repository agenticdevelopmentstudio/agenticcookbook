
- `should-look-for-existing-solution`: non-trivial functionality built with no sign that an existing solution was looked for
- `must-check-existing-solutions-nearest-first`: custom code duplicating what the platform, standard library, a current dependency, a sibling or shared module, or a proven open-source library already provides
- `should-check-dependencies-before-adding`: a new dependency added for a capability a current dependency already has
- `should-search-ecosystem-for-prior-art`: non-trivial functionality implemented with no search of the package registry or code search for prior art
- `should-prefer-extending-existing-library`: a parallel implementation of what a used library almost does, where extending it or contributing upstream was possible
- `must-verify-candidate-package`: new packages whose existence, maintenance and real use were not confirmed
- `should-not-install-unverified-ai-suggested-package`: AI-suggested package names installed unverified, including typosquat-like names
- `must-weigh-dependency-against-building`: a dependency taken on for trivial functionality a little copying would cover
