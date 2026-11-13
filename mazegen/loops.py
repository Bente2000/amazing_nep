"""Functions that make sure that the pacman maze has enough loops.
"""

import random
from .grid import Grid, Position
from .open_areas import try_remove_wall


def ensure_min_loops(grid: Grid, rng: random.Random,
                     blocked: set[Position]) -> None:
    """Make sure there are at least 2 loops.

    Parameters
    ----------
    grid : grid
        list[list[dict[str, Any]]]
        2D-array of cells with their `"walls"` and `"visited"` information.
    rng : random.Random
        Pass over a generator with the correct seed.
    blocked : set[Position], set[tuple[int, int]]
        Set of `blocked` cells (the 42 pattern).
    """
    loops = count_loops(grid, blocked)

    for current, direction, neighbour in list_closed_walls(
            grid, rng, blocked):
        if loops >= 2:
            return
        if try_remove_wall(grid, current, direction, neighbour):
            loops += 1  # each extra passage adds exactly one loop


def count_loops(grid: Grid, blocked: set[Position]) -> int:
    """Count the amount of loops in the maze.

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]
        Used to check which `"walls"` are open.
    blocked : set[Position]
        set[tuple[int, nt]]
        Set of 'blocked' cells (the 42 pattern).

    Returns
    -------
    int
        The total amount of loops.
    """
    height = len(grid)
    width = len(grid[0])
    cells = 0
    passages = 0

    for y in range(height):
        for x in range(width):
            if (x, y) in blocked:
                continue
            cells += 1
            walls = grid[y][x]["walls"]
            if not walls["E"] and x + 1 < width:
                passages += 1
            if not walls["S"] and y + 1 < height:
                passages += 1

    return passages - (cells - 1)


def list_closed_walls(grid: Grid, rng: random.Random,
                      blocked: set[Position]
                      ) -> list[tuple[Position, str, Position]]:
    """List which `"walls"` are closed (except the 42 pattern).

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]
        Used to check which `"walls"` are closed.
    rng : random.Random
        Random number generator used to shuffle the closed `"walls"` so that if
        an extra loop is created, it is not always the first wall in the list
        that would be opened.
    blocked : set[Position]
        set[tuple[int, int]]
        The 42 pattern, it doesn't count for the list.

    Returns
    -------
    list[tuple[Position, str, Position]]
        list[tuple[[int, int], str, [int, int]]]
        All the `"walls"` in the grid that are closed.
    """
    height = len(grid)
    width = len(grid[0])
    closed_walls: list[tuple[Position, str, Position]] = []
    for y in range(height):
        for x in range(width):
            for direction, (dx, dy) in (("E", (1, 0)), ("S", (0, 1))):
                neighbour = (x + dx, y + dy)
                if neighbour[0] >= width or neighbour[1] >= height:
                    continue
                if (x, y) in blocked or neighbour in blocked:
                    continue
                if grid[y][x]["walls"][direction]: # direction is S en E
                    closed_walls.append(((x, y), direction, neighbour))

    rng.shuffle(closed_walls)
    return closed_walls
