"""Import third-party deps with a clean install hint on failure."""

from .errors import MissingDependencyError

_HINT = (
    "Missing Python dependency '{name}'. Install with:\n"
    "    python3 -m pip install --user {name}\n"
    "(./install installs rich, questionary, pyyaml automatically.)"
)


def require(name: str):
    try:
        return __import__(name)
    except ImportError as e:
        raise MissingDependencyError(_HINT.format(name=name)) from e
