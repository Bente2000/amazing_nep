"""A reusable maze generator.
"""

import random
from typing import Any
from .grid import Cell, Grid, create_grid
from .pacman_maze import make_pacman_maze
from .pattern_42 import create_42
from .perfect_maze import carve_perfect_maze
from .solver import solve

Position = tuple[int, int]

class MazeGenerator:

    def __init__(self, width: int, height: int, entry: Position,
                 exit_: Position, perfect: bool = False, # false = default
                 seed: int | None = None) -> None:
        self._check_types(width, height, entry, exit_, perfect, seed) # juiste waardes meegekregen?
        self._check_values(width, height, entry, exit_, perfect)
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.perfect = perfect
        self.seed = seed
        self.random = random.Random(seed) # instance of Random class from random 
        self.pattern_cells: set[Position] = set() # lege set voor tuples
        self.grid: Grid = create_grid(width, height) # start met verse grid om
        #crashes te voorkomen wanneer self.grid wordt gebruikt zonder eerst generate() te callen

    @staticmethod # hoeft self niet te gebruiken, dus eigenlijk een plain method
    #hier geplaatst vanwege organisatie
    def _check_types(width: Any, height: Any, entry: Any, exit_: Any, 
                     perfect: Any, seed: Any) -> None:
        if not isinstance(width, int):
            raise ValueError("Width must be an integer")
        if not isinstance(height, int):
            raise ValueError("Height must be an integer")
        if not isinstance(entry, tuple) or len(entry) != 2:
            raise ValueError("Entry must be tuple of two integers: (x,y)")
        if not isinstance(entry[0], int) or not isinstance(entry[1], int):
            raise ValueError("Entry must be tuple of two integers: (x,y)")
        if not isinstance(exit_, tuple) or len(exit_) != 2:
            raise ValueError("Exit must be tuple of two integers: (x,y)")
        if not isinstance(exit_[0], int) or not isinstance(exit_[1], int):
            raise ValueError("Exit must be tuple of two integers: (x,y)")
        if not isinstance(perfect, bool):
            raise ValueError("Perfect must be set to True or False")
        if seed is not None and not isinstance(seed, int):
            raise ValueError("Seed must be an integer or None")

    @staticmethod
    def _check_values(width: int, height: int, entry: Position,
                      exit_: Position, perfect: bool) -> None:
        if width < 1 or height < 1:
            raise ValueError("Maze dimentions must be positive")
        if not perfect and (min(width, height) < 2 or width * height < 6):
            raise ValueError("Maze must fit at least two loops in pac-man mode"
                             " (non-perfect maze)")
        for name, (x,y) in (("Entry", entry), ("Exit", exit_)):
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(f"{name} is outside of the maze")
        if entry == exit_:
            raise ValueError("Entry and exit must be different from each other")


    def generate(self) -> Grid:
        """Generate a new maze and return the grid."""
        self.grid = create_grid(self.width, self.height) # nodig voor regenerate, maak verse grid
        self.pattern_cells = create_42(
            self.width, self.height, self.entry, self.exit_)

        carve_perfect_maze(
            self.grid, self.entry, self.random, self.pattern_cells)

        if not self.perfect:
            make_pacman_maze(self.grid, self.random, self.pattern_cells)

        return self.grid

    def solve(self) -> list[Position] | None:
        """Find the shortest path from entry to exit."""
        return solve(self.grid, self.entry, self.exit_)
