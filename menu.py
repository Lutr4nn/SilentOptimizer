from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED

def terminal_menu():
    all_lines = [f"Option {i}" for i in range(1, 11)]

    table = Table(title="SilentOptimizer", title_style="bold green", box=ROUNDED)

    table.add_column("Number", justify="center", style="cyan", no_wrap=True, width=12)
    table.add_column("Description", justify="left", style="magenta", width=12)
    
    for i, line in enumerate(all_lines, start=1):
        table.add_row(
            f"[{i}]", line,
        )

    console = Console()
    console.print(table)
