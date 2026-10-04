class CookbookError(Exception):
    """Base error surfaced to the user with a clean message and non-zero exit."""


class NoCookbookRootError(CookbookError):
    """Raised when a module needs a cookbook root but resolution found none."""


class MissingDependencyError(CookbookError):
    """Raised when an optional Python dep (rich, questionary, pyyaml) is missing."""
