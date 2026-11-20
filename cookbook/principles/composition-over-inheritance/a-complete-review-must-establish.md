
- `should-compose-from-small-focused-pieces`: whether new behavior is composed from small, focused pieces by default
- `should-use-inheritance-only-for-genuine-is-a`: whether each subclass stands for a genuine "is-a" relationship, and inheritance is used sparingly
- `should-prefer-protocols-over-base-classes`: whether shared behavior lives in protocols/interfaces or standalone functions rather than a base class
- `should-wrap-rather-than-subclass`: whether added behavior wraps the existing type rather than extending its inheritance chain
- `must-not-nest-inheritance-more-than-one-level`: No inheritance hierarchies more than 1 level deep except for genuine is-a relationships;
- `should-wrap-rather-than-subclass`: no subclassing to extend behavior where wrapping is possible
