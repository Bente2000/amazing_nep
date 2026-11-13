"""Functions that prevent the pacman maze from having any dead ends.
"""

import random
from .grid import Grid, Position, get_neighbours
from .open_areas import try_remove_wall


def remove_dead_ends(grid: Grid, rng: random.Random,
                     blocked: set[Position]) -> None:
    """Open a random wall in every dead end.

    Parameters
    ----------
    grid : grid
        list[list[dict[str, Any]]]
        2D-array of cells with their `"walls"` and `"visited"` information.
    rng : random.Random
        Random number generator used to decide which candidate's wall to open.
        Candidates are not `blocked` and inside the `grid`.
    blocked : set[Position], set[tuple[int, int]]
        Set of `blocked` cells (the 42 pattern).
    """
    dead_ends = [ # dead_ends set van tuples (coordinaten)
        (x, y)
        for y in range(len(grid)) # len(grid) = len(y-as)
        for x in range(len(grid[0])) # len(grid[0]) = len(x-as)
        if is_dead_end(grid, (x, y), blocked) # voeg dode eindes toe aan set
    ]
    #rng.shuffle(dead_ends) # set shuffelen ## NODIG? (niet nodig voor max
    # score) (geen dead ends)

    for current in dead_ends:
        if not is_dead_end(grid, current, blocked):  # already fixed
            continue

        x, y = current
        candidates = [ # = comprehension, mss toch wel mooi
            (direction, position)
            for direction, position in get_neighbours(grid, x, y)
            if grid[y][x]["walls"][direction] and position not in blocked
        ]
        rng.shuffle(candidates) # shuffle neighbours

        for direction, neighbour in candidates: # loop want het kan fout gaan
            if try_remove_wall(grid, current, direction, neighbour):
                break # break wanneer 1 muur geopend


def is_dead_end(grid: Grid, position: Position,
                blocked: set[Position]) -> bool:
    """Check whether a cell has exactly 3 closed `"walls"`.

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]
        2D-array of cells containing their `"walls"` and `"visited"` info.
    position : Position
        tuple[int, int]
        The coordinates of the cell being investigated.
    blocked : set[Position]
        set[tuple[int, int]]
        Set of `blocked` cells (the 42 pattern).

    Returns
    -------
    bool
        True when 3 `"walls"` are closed.
        False when the cell is in 'blocked' or doesn't have 3 closed `"walls"`.
    """
    if position in blocked: # patroon telt niet mee als dood einde
        return False
    x, y = position
    closed: int = sum(grid[y][x]["walls"].values()) # alle values uit walls dict
    return closed == 3 # 3 muren zijn true = dood einde
