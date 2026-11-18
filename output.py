"""Write a maze and it's shortest solution to the output file.
"""
from mazegen.grid import Grid, Position

# Bit value of each wall: a closed wall sets its bit to 1
WALL_BITS = {"N": 1, "E": 2, "S": 4, "W": 8}
"""Every value, when set to True, represents a closed wall in that direction.

Example
-------

"""

# Step between two neighbouring cells -> direction letter
DIRECTION = {
    (0, -1): "N",
    (1, 0): "E",
    (0, 1): "S",
    (-1, 0): "W",
}
"""The key is the step (in x and y) towards the direction given as value.

    dict[tuple, str]
"""

def write_output(grid: Grid, entry: Position, exit_: Position, filename: str, 
                 path: list[tuple[int, int]] | None) -> None:
    """Write the maze, entry, exit and shortest path to the file.

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]
        Convert the grid to hexadecimals using the `"walls"` data.
    entry : Position
        tuple[int, int]
        The coordinates of the entry of the maze.
    exit_ : Position
        tuple[int, int]
        The coordinates of the exit of the maze.
    filename : str
        The name of the output file.
    path : list[tuple[int, int]] | None
        Convert the path from coordinates to directions.

    Raises
    ------
    OSError
        If the ouput file can't be written to.
    """

    lines = []
    for row in grid:
        lines.append("".join( # "" want geen character plaatsen tussen lines
            cell_to_hex(cell["walls"]) for cell in row # pak info over muren
        )) # groei maze row for row, join hele row en append in list

    lines.append(f"\n{entry[0]},{entry[1]}")
    lines.append(f"{exit_[0]},{exit_[1]}")
    lines.append(path_as_directions(path) if path else "")

    with open(filename, "w") as file:
        file.write("\n".join(lines) + "\n")


def cell_to_hex(walls: dict[str, bool]) -> str:
    """Encode the walls of one cell as a single hexadecimal digit."""

    """

    Parameters
    ----------
    walls : dict[str, bool]
        Use the direction key to get the value for each wall and use them as
        `WALL_BITS`.
    Returns
    -------
    str
        The values for the directions in `WALL_BITS` converted to hexadecimals.
    """
    value = 0
    for direction, bit in WALL_BITS.items(): # "N":1, "E":2, "S":4, "W":8
        if walls[direction]: # if walls["N"] == True, False, True, True
            value |= bit # |= (merge bits) bv: 0100 |= 1000, value = 1100 = 12
    return format(value, "x") # convert naar lowercase hexadecimal = b


def path_as_directions(path: list[tuple[int, int]]) -> str:
    """Convert a list of coordinates into a string like 'ESSEN'."""
    direction_letters = ""
    if not path:
        return ""

    came_before = path[0]            # the cell we were on one step ago
    for current in path[1:]:         # every cell except the first
        step = (current[0] - came_before[0], current[1] - came_before[1])
        direction_letters += DIRECTION[step]
        came_before = current        # move forward: this cell is now "before"
    return direction_letters
