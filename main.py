# Copyright (C) 2026 Kamil Yarkaev kamilarkaev@gmail.com
# License: GPL-3.0+


from functions import main_menu, greeting
from rich.console import Console

console = Console()
if __name__ == "__main__":
    try: 
        greeting()
        main_menu()

    except KeyboardInterrupt:
        console.print("\n\n[bold #fabd2f]CLI-Mate was interrupted. Bye, Mate![/]")