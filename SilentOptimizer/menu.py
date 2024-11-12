from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED

def terminal_menu():
    lines = [
        "Option 1",
        "Option 2",
        "Option 3",
        "Option 4",
        "Option 5",
        "Option 6",
        "Option 7",
        "Option 8",
        "Option 9",
        "Option 10"
    ]

    table = Table(title="SilentOptimizer", title_style="bold green", box=ROUNDED)

    table.add_column("Number", justify="center", style="cyan", no_wrap=True, width=12)
    table.add_column("Tool", justify="left", style="magenta", width=12)
    
    for i, line in enumerate(lines, start=1):
        table.add_row(
            f"[{i}]",
            line,
        )

    console = Console()
    console.print(table)
