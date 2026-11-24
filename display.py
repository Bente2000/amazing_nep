from mazegen import MazeGenerator
from mazegen.grid import Position
from output import write_output

RESET = "\033[0m"
"""str : Colour code that resets the terminal to the default colour.
"""

WALL_COLOURS = [
    "\033[97m",  # bright white
    "\033[31m",  # red
    "\033[32m",  # green
    "\033[33m",  # yellow
    "\033[34m",  # blue
    "\033[95m",  # bright magenta
    "\033[96m",  # bright cyan
]
"""list[str] : Colour codes for bright white, red, green, yellow, blue,
               bright magenta and bright cyan, respectively.
"""

ENTRY_COLOUR = "\033[7;92m"
"""str : Bright green.
"""

EXIT_COLOUR = "\033[7;91m"
"""str : Bright red.
"""

PATH_COLOUR = "\033[94m"
"""str : Bright blue.
"""

PATTERN_COLOUR = "\033[7;95m"  # magenta background
"""str : Magenta background.
"""



def _cell_content(maze: MazeGenerator, x: int, y: int,
                  path_cells: set[Position]) -> str:
    """Return the 3-character content of a cell, coloured."""
    if (x, y) == maze.entry:
        return f"{ENTRY_COLOUR} S {RESET}"
    if (x, y) == maze.exit_:
        return f"{EXIT_COLOUR} E {RESET}"
    if (x, y) in maze.pattern_cells:
        return f"{PATTERN_COLOUR}✿🌸{RESET}"
    if (x, y) in path_cells:
        return f"{PATH_COLOUR}｡🫧{RESET}"
    return "   "


#def render_ascii(maze: MazeGenerator,
#                 path: list[Position] | None = None,
#                 wall_colour: str = WALL_COLOURS[0]) -> str:
#    """Return the maze as a coloured ASCII string."""
#    path_cells = set(path) if path else set()
#
#    def wall(text: str) -> str:
#        return f"{wall_colour}{text}{RESET}"
#
#    lines = []
#
#    # Top border: north walls of the first row
#    top = wall("+")
#    for _ in range(maze.width):
#        top += wall("---") + wall("+")
#    lines.append(top)
#
#    for y in range(maze.height):
#        middle = wall("|") # west muur van maze
#        bottom = wall("+") # west muur van maze
#
#        for x in range(maze.width):
#            cell = maze.grid[y][x]
#            content = _cell_content(maze, x, y, path_cells) # voor speciale
#            # tekens / kleuren (pattern, entry, exit, path)
#
#            # East wall right of the cell
#            middle += content + (wall("|") if cell["walls"]["E"] else " ")
#            # South wall below the cell
#            bottom += ((wall("---") if cell["walls"]["S"] else "   ")
#                        + wall("+"))
#        lines.append(middle) # append per row, middle = grote string
#        lines.append(bottom) # append per row, bottom = grote string
#        # 2 lines per cel
#
#    return "\n".join(lines) #maze = lange string gevuld met strings en kleurcodes

def render_ascii(maze: MazeGenerator,                # andere versie
                 path: list[Position] | None = None,
                 wall_colour: str = WALL_COLOURS[0]) -> str:
    """Return the maze as a coloured ASCII string."""
    path_cells = set(path) if path else set()

    def wall(text: str) -> str:
        return f"{wall_colour}{text}{RESET}"

    lines = []

    # Top border: north walls of the first row
    top = wall(":)")
    for _ in range(maze.width - 1):
        top += wall("~~~~")# + wall("-")
    top += wall("~:)")# + wall("-")
    lines.append(top)

    for y in range(maze.height):
        middle = wall(":") # west muur van maze
        if y == maze.height - 1:
            bottom = wall(":)") # west muur van maze
        else:
            bottom = wall(":") # west muur van maze

        for x in range(maze.width - 1):
            cell = maze.grid[y][x]
            content = _cell_content(maze, x, y, path_cells) # voor speciale
            # tekens / kleuren (pattern, entry, exit, path)
            middle += content + (wall("|") if cell["walls"]["E"] else " ")
            if y == maze.height - 1:
                bottom += wall("~~~~")
            else:
                if cell["walls"]["S"]:
                    bottom += wall("===O")
                elif cell["walls"]["E"]:
                    bottom += wall("   O")
                else:
                    bottom += wall("    ")
        x += 1
        cell = maze.grid[y][x]
        content = _cell_content(maze, x, y, path_cells)
        middle += content + wall(")")
        if y == maze.height - 1:
            bottom += wall("~:)")
        elif cell["walls"]["S"]:
            bottom += wall("===)")
        elif cell["walls"]["E"]:
            bottom += wall("   )")
        lines.append(middle) # append per row, middle = grote string
        lines.append(bottom) # append per row, bottom = grote string
        # 2 lines per cel

    return "\n".join(lines) #maze = lange string gevuld met strings en kleurcodes


def run_menu(maze: MazeGenerator, output_file: str, path: list[Position] | None) -> None:
    """Show the maze and handle user choices until the user quits."""
    show_path = False
    colour_index = 0
    #path = maze.solve()
    valid_choice = True

    while True: # until error or exit
        if valid_choice:
            print(render_ascii(maze, path if show_path else None,
                               WALL_COLOURS[colour_index]))
            print("\nA-Maze-ing: You have generated a maze.\n")
            print("1: Show/hide shortest path")
            print("2: Change wall colours")
            print("3: Generate a new maze")
            print("4: Quit")

        try:
            choice = input("\nChoose an option (1 ,2 ,3 or 4): ").strip()
        except (KeyboardInterrupt): # voor ^D
            print("\n")
            return
        except (EOFError): # voor ^C
            print("\n")
            return
        if choice == "1":
            show_path = not show_path
            valid_choice = True
        elif choice == "2":
            colour_index = (colour_index + 1) % len(WALL_COLOURS)#roteer ipv ++
            valid_choice = True
        elif choice == "3":
            maze.generate()
            path = maze.solve()
            write_output(maze.grid, maze.entry, maze.exit_, output_file, path)
            valid_choice = True
        elif choice == "4":
            return
        else:
            print("Invalid choice, please enter a number from 1 to 4.")
            valid_choice = False
