from mazegen import MazeGenerator
from mazegen.grid import Position
from output import write_output

RESET = "\033[0m"
WALL_COLOURS = [
    "\033[37m",  # white
    "\033[31m",  # red
    "\033[32m",  # green
    "\033[33m",  # yellow
    "\033[34m",  # blue
    "\033[35m",  # magenta
    "\033[36m",  # cyan
]
ENTRY_COLOUR = "\033[92m"
EXIT_COLOUR = "\033[91m"
PATH_COLOUR = "\033[93m"
PATTERN_COLOUR = "\033[45m"  # magenta background colour, so it stands out


def _cell_content(maze: MazeGenerator, x: int, y: int,
                  path_cells: set[Position]) -> str:
    """Return the 3-character content of a cell, coloured."""
    if (x, y) == maze.entry:
        return f"{ENTRY_COLOUR} S {RESET}"
    if (x, y) == maze.exit:
        return f"{EXIT_COLOUR} E {RESET}"
    if (x, y) in maze.pattern_cells:
        return f"{PATTERN_COLOUR}   {RESET}"
    if (x, y) in path_cells:
        return f"{PATH_COLOUR} * {RESET}"
    return "   "


def render_ascii(maze: MazeGenerator,
                 path: list[Position] | None = None,
                 wall_colour: str = WALL_COLOURS[0]) -> str:
    """Return the maze as a coloured ASCII string."""
    path_cells = set(path) if path else set()

    def wall(text: str) -> str:
        return f"{wall_colour}{text}{RESET}"

    lines = []

    # Top border: north walls of the first row
    top = wall("+")
    for x in range(maze.width):
        closed = maze.grid[0][x]["walls"]["N"]
        top += (wall("---") if closed else "   ") + wall("+")
    lines.append(top)

    for y in range(maze.height):
        middle = wall("|")
        bottom = wall("+")

        for x in range(maze.width):
            cell = maze.grid[y][x]
            #cell = maze.get_cell(x, y)
            content = _cell_content(maze, x, y, path_cells)

            # East wall right of the cell
            middle += content + (wall("|") if cell["walls"]["E"] else " ")
            # South wall below the cell
            bottom += ((wall("---") if cell["walls"]["S"] else "   ")
                        + wall("+"))

        lines.append(middle)
        lines.append(bottom)

    return "\n".join(lines)


def run_menu(maze: MazeGenerator, output_file: str) -> None:
    """Show the maze and handle user choices until the user quits."""
    show_path = False
    colour_index = 0
    path = maze.solve()

    while True: # until error or exit
        print(render_ascii(maze, path if show_path else None,
                           WALL_COLOURS[colour_index]))
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")

        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if choice == "1":
            maze.generate()
            maze.solve()
            write_output(maze.grid, maze.entry, maze.exit, output_file, path)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            colour_index = (colour_index + 1) % len(WALL_COLOURS)#roteer ipv ++
        elif choice == "4":
            return
        else:
            print("Invalid choice, please enter a number from 1 to 4.")
