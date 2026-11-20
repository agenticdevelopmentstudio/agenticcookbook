
- `should-look-for-existing-solution`: every non-trivial capability built records what existing solutions were looked for, or says why not
- `must-check-existing-solutions-nearest-first`: every custom implementation records that the platform, current dependencies, own and shared codebases, and proven open source were checked in that order
- `should-check-dependencies-before-adding`: every added dependency records that current dependencies lack the capability, or says why not
- `should-search-ecosystem-for-prior-art`: every non-trivial implementation records the registry and code search done for prior art, or says why not
- `should-prefer-extending-existing-library`: no parallel implementation exists of what a used library almost does, or the build says why not
- `must-verify-candidate-package`: every added package is confirmed to exist, be actively maintained, and be genuinely used
- `should-not-install-unverified-ai-suggested-package`: every AI-suggested package added was verified first, or the build says why not
- `must-weigh-dependency-against-building`: every new dependency is weighed against building it, and none is added for trivial functionality
