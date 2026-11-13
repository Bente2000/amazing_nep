"""Functions that have to do with the grid.
"""

from typing import Any

Position = tuple[int, int]
Cell = dict[str, Any] # str =walls en visited, any = diactionary vs boolean (niet hetzelfde type)
Grid = list[list[Cell]]

OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}
"""dict[str] : The keys are the four directions, the values their opposites.
"""


def create_grid(width: int, height: int) -> Grid:
    """Create a grid of cells.

    In every cell the `"walls"` are represented by the four directions,
    set to True (meaning they are closed `"walls"`).
    Every cell is also set to unvisited (`"visited"` = False).

    Parameters
    ----------
    width : int
        The width of the grid.
    height : int
        The height of the grid.

    Returns
    -------
    Grid
        list[list[dict[str, Any]]]
        A whole grid (2D-array) made of cells, holding information about
        themselves (dict with two keys: `"walls"` and `"visited"`, their values,
        respectively: "{"N" :True, etc.}" and False).
    """
    return [ # row for row = grid[y][x], y is primaire lijst
        [
            {
                "walls": {"N": True, "E": True, "S": True, "W": True},
                "visited": False,
            }
            for _ in range(width)
        ]
        for _ in range(height)
    ]


def get_neighbours(grid: Grid, x: int, y: int) -> list[tuple[str, Position]]:
    """Create a list of the neighbours of the current cell.

    Neighbours are represented by direction in relation to the current cell,
    they also have their coordinates stored.

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]
        The whole grid of cells.
    x : int
        The x-value of the current cell.
    y : int
        The y-value of the current cell.

    Returns
    -------
    neighbours : list[tuple[str, Position]]
        List of neighbours (tuples): direction (str), coordinates (Position).
    """
    height = len(grid)
    width = len(grid[0])
    neighbours: list[tuple[str, Position]] = []

    if y > 0:
        neighbours.append(("N", (x, y - 1)))
    if x < width - 1:
        neighbours.append(("E", (x + 1, y)))
    if y < height - 1:
        neighbours.append(("S", (x, y + 1)))
    if x > 0:
        neighbours.append(("W", (x - 1, y)))

    return neighbours


def remove_wall(grid: Grid, current: Position, direction: str,
                neighbour: Position) -> None:
    """Open the wall between two neighbours (from both sides).

    Open both `"walls"` by opening from opposite direction in neighbour.

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]
        The whole grid of cells.
    current : Position
        tuple[int, int]
        (x, y) of the current cell.
    direction : str
        Direction of the wall we want to remove.
    neighbour : Position
        tuple[int, int]
        (x, y) of the cell neighbouring the wall we want to remove.
    """
    x1, y1 = current
    x2, y2 = neighbour
    grid[y1][x1]["walls"][direction] = False
    grid[y2][x2]["walls"][OPPOSITE[direction]] = False


def close_wall(grid: Grid, current: Position, direction: str,
               neighbour: Position) -> None:
    """Close the wall between two neighbours (from both cells).

    Close both `"walls"` by closing from opposite `direction` in `neighbour`.

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]
        The whole grid of cells.
    current : Position
        tuple[int, int]
        (x, y) of the `current` cell.
    direction : str
        `direction` of the wall we want to close.
    neighbour : Position, tuple[int, int]
        (x, y) of the cell neighbouring the wall we want to close.
    """
    x1, y1 = current
    x2, y2 = neighbour
    grid[y1][x1]["walls"][direction] = True
    grid[y2][x2]["walls"][OPPOSITE[direction]] = True
