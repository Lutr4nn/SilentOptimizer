from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED
from tools import *


def terminal_menu():
    lines = [
        "CPU Bouncer",
        "Disk Space",
        "Disk Cleaner",
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
        table.add_row(f"[{i}]", line)

    console = Console()
    console.print(table)
    
    try:
        choice = int(input("Choose a tool number: "))
        if 1 <= choice <= 10:
            if choice == 1:
                tool.cpu_bouncer()
            elif choice == 2:
                tool.disk_space()
                print('If you want to clean the disk, you can use the Disk Clenaer tool.')
            elif choice == 3:
                tool.disk_cleaner()
            elif choice == 4:
                Tools.option_4()
            elif choice == 5:
                Tools.option_5()
            elif choice == 6:
                Tools.option_6()
            elif choice == 7:
                Tools.option_7()
            elif choice == 8:
                Tools.option_8()
            elif choice == 9:
                Tools.option_9()
            elif choice == 10:
                Tools.option_10()
            else:
                print(f"Option {choice} is running.")
        else:
            print("Invalid choice. You must choose a number between 1 and 10.")
    except ValueError:
        print("Only numbers are allowed.")
