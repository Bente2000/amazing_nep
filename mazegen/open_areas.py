"""Functions that prevent the pacman maze from having 3x3 open areas.
"""

from .grid import Grid, Position, remove_wall, close_wall


def try_remove_wall(grid: Grid, current: Position, direction: str,
                    neighbour: Position) -> bool:
    """Remove a wall unless that creates a 3x3 open area.

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]
        Used to know which `"walls"` can be opened.
    current : Position
        tuple[int, int]
        The coordinates of the current cell.
    direction : str
        Which wall we want to break open.
    neighbour : Position
        tuple[int, int]
        The coordinates of the cell behind the wall we want to break open.

    Returns
    -------
    bool
        True if no 3x3 area is found, otherwise False.
    """
    remove_wall(grid, current, direction, neighbour)
    if find_open_3x3(grid, current):
        close_wall(grid, current, direction, neighbour)
        return False
    return True


def find_open_3x3(grid: Grid, cell: Position) -> bool:
    """Check if breaking open the current cell resulted in an open area.

    Pass all the 9 3x3 areas that the current cell is part of to
    has_open_3x3().
    Don't pass areas that contain cells that are outside the grid.
    In the first area that is checked, the current cell sits in the right lower
    corner.

    Parameters
    ----------
    grid : Grid
        list[list[dict[str,Any]]]
        Used to determine the dimensions of the grid and pass information about
        the `"walls"`.

    cell : Position
        tuple[int, int]
        The cell that has just been broken open.

    Returns
    -------
    bool
        True if an open area is found, False otherwise.
    """
    height = len(grid)
    width = len(grid[0])
    x, y = cell
    for y0 in range(y - 2, y + 1):
        for x0 in range(x - 2, x + 1):
            if x0 < 0 or y0 < 0 or x0 + 2 >= width or y0 + 2 >= height:
                continue
            if has_open_3x3(grid, x0, y0):
                return True
    return False


def has_open_3x3(grid: Grid, x0: int, y0: int) -> bool:
    """Look at the `"walls"` in a 3x3 area and determine if it's an open area.

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]
        Provides information on which `"walls"` are open or closed.
    x0 : int
        The top left x-value of the 3x3 area.
    xy : int
        The top left y-value of the 3x3 area.

    Returns
    -------
    bool
        False if all `"walls"` are open, the outer `"walls"` excluded.
        True otherwise.
    """
    for dy in range(3): # pak muurinfo 3 cellen, check alleen eerste 2
        for dx in range(3):
            walls = grid[y0 + dy][x0 + dx]["walls"]
            if dx < 2 and walls["E"]: # < 2 check want: buitenste muur mag dicht
                return False
            if dy < 2 and walls["S"]:
                return False
    return True
