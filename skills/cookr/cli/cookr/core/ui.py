"""Rich console wrapper. Colored titles, sections, tables, status lines.

All user-facing output goes through here so the entire tool has consistent styling.
"""

from __future__ import annotations

from .deps import require

_rich = require("rich")
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


class UI:
    def __init__(self) -> None:
        self.console = Console()

    def title(self, text: str) -> None:
        self.console.print()
        self.console.print(Panel(Text(text, style="bold cyan"), border_style="cyan"))

    def section(self, text: str) -> None:
        self.console.print()
        self.console.print(f"[bold yellow]› {text}[/bold yellow]")

    def info(self, text: str) -> None:
        self.console.print(f"[dim]{text}[/dim]")

    def ok(self, text: str) -> None:
        self.console.print(f"[green]✓[/green] {text}")

    def warn(self, text: str) -> None:
        self.console.print(f"[yellow]![/yellow] {text}")

    def error(self, text: str) -> None:
        self.console.print(f"[red]✗[/red] {text}")

    def skip(self, text: str) -> None:
        self.console.print(f"[dim]·[/dim] [dim]{text}[/dim]")

    def table(self, columns: list[str], rows: list[list[str]], title: str | None = None) -> None:
        t = Table(title=title, show_header=True, header_style="bold")
        for c in columns:
            t.add_column(c)
        for r in rows:
            t.add_row(*r)
        self.console.print(t)

    def blank(self) -> None:
        self.console.print()
