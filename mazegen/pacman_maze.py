"""Create a pacman maze out of a perfect maze.
"""
import random
from .grid import Grid, Position
from .dead_ends import remove_dead_ends
from .loops import ensure_min_loops


def make_pacman_maze(grid: Grid, rng: random.Random,
                     blocked: set[Position]) -> None:
    """Make sure the maze has no dead ends anymore and has at least 2 loops.

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]
        2D-array of cells containing their `"walls"` and `visited` information.
    rng : random.Random
        Random number generator created in MazeGenerator, we pass it over to
        make sure the seed is correct.
    blocked : set[Position]
        set[tuple[int, int]]
        Set of `blocked` cells (the 42 pattern).
    """
    remove_dead_ends(grid, rng, blocked)
    ensure_min_loops(grid, rng, blocked)
