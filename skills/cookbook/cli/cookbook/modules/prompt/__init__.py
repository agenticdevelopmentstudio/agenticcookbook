"""`cookbook prompt` — assemble an expert prompt and print it.

See prompt_cli for the implementation; this file just re-exports the
module-protocol attrs (NAME, HELP, register, run) so `cliapp.discover`
picks them up.
"""

from .prompt_cli import NAME, HELP, register, run

__all__ = ["NAME", "HELP", "register", "run"]
