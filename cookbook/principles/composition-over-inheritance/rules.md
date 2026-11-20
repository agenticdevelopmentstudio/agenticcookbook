
- **should-compose-from-small-focused-pieces**: SHOULD default to composing behaviors from small, focused pieces.
- **should-use-inheritance-only-for-genuine-is-a**: SHOULD use inheritance only for genuine "is-a" relationships, and even then sparingly; when tempted to subclass, SHOULD ask: "Is this truly an 'is-a' relationship, or am I just reusing code?"
- **should-prefer-protocols-over-base-classes**: SHOULD prefer protocols/interfaces over base classes, extracting shared behavior into protocols or standalone functions instead of a base class.
- **should-wrap-rather-than-subclass**: When extending behavior, SHOULD wrap rather than subclass: wrap an existing type with a new type to add behavior rather than extending the inheritance chain.
