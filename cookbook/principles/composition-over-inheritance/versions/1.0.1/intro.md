
# Composition over inheritance

Default to composing behaviors from small, focused pieces. Use inheritance only for genuine "is-a" relationships, and even then sparingly. Prefer protocols/interfaces over base classes. When extending behavior, wrap rather than subclass.

- When tempted to subclass, ask: "Is this truly an 'is-a' relationship, or am I just reusing code?"
- Extract shared behavior into protocols or standalone functions instead of a base class
- Wrap an existing type with a new type to add behavior rather than extending the inheritance chain

