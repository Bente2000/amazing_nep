"""Create the 42 pattern.
"""

from .grid import Position

PATTERN_42 = (
    "X.X.XXX",
    "X.X...X",
    "XXX.XXX",
    "..X.X..",
    "..X.XXX",
)
"""tuple[str, ...] : The pattern formed by 5 strings of 7 characters.
"""


def create_42(width: int, height: int, entry: Position,
                          exit_: Position) -> set[Position]:
    """Create the 42 pattern if it fits inside the maze.

    Parameters
    ----------
    width : int
        The width of the maze.
    height : int
        The height of the maze.
    entry : Position
        tuple[int, int]
        The entry (x, y) of the maze.
    exit_ : Position
        tuple[int, int]
        The exit (x, y) of the maze.

    Returns
    -------
    X_cells : set[Position]
        set[tuple[int, int]]
        The cells forming the pattern or an empty set if the maze is too small.
    """
    pat_h = len(PATTERN_42) # telt elementen (= gelijk aan y = 5)
    pat_w = len(PATTERN_42[0]) # telt lengte eerste element (=x=7)
    # centre it so the maze centre lands in the gap between 4 and 2
    start_x = width // 2 - pat_w // 2
    start_y = height // 2 - pat_h // 2

    # keep a margin of 1 cell so nothing gets isolated at the border
    if (start_x < 1 or start_y < 1
            or start_x + pat_w > width - 1
            or start_y + pat_h > height - 1):
        print("Error: maze too small for the '42' pattern, skipping it.")
        return set()

    X_cells = {
        (start_x + count_X, start_y + count_row)
        for count_row, row in enumerate(PATTERN_42)
        for count_X, char in enumerate(row)
        if char == "X"
    } # cells is een set van tuples (coordinaten)

    if entry in X_cells or exit_ in X_cells:
        print("Error: entry or exit is inside the '42', skipping it.")
        return set()

    return X_cells
