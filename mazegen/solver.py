"""Find the shortest path by using the A* search algorithm.
"""

import heapq
from .grid import Grid, Position


DIRECTIONS = {
    "N": (0, -1),  # rows are counted top to bottom, so north is y - 1
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}
"""Directions represented as steps (in x and y).
"""


def solve(grid: Grid, entry: Position, exit_: Position) -> list[Position] | None:
    """Return the shortest path from entry to exit, or None if none exists."""
    """

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]

    entry : Position
        tuple[int, int]

    exit_ : Position
        tuple[int, int]

    Returns
    -------
    list[Position] | None
        list[tuple[int, int]] | None
        The shortest path (in coordinates) or None if no path is found.
    """
    height = len(grid)
    width = len(grid[0])

    def heuristic(position: Position) -> int:
        """Manhattan distance to the exit (expected remaining cost)."""
        """
        Parameters
        ----------
        position : Position
            tuple[int, int]

        Returns
        -------
        int
        """
        return (abs(position[0]) - abs(exit_[0])) + (abs(position[1]) -
                abs(exit_[1]))

    open_list: list[tuple[int, Position]] = [] # list[(f-waarde, (x,y)]
    heapq.heappush(open_list, (heuristic(entry), entry)) # g=0, dus h + 0 = f
    g_values: dict[Position, int] = {entry: 0}
    came_from: dict[Position, Position | None] = {entry: None}

    while open_list:
        _, current = heapq.heappop(open_list) # kleinste uit list is nu current
    # _ = priority = index (niet nodig)
        if current == exit_:
            path: list[Position] = []
            node: Position | None = current
            while node is not None:
                path.append(node)
                node = came_from[node]
            path.reverse() # came_from is path in reverse dus draai om
            return path

        x, y = current
        for direction, (dx, dy) in DIRECTIONS.items(): # items() haalt element uit dict, dus check alle 4 directions, 1 per loop
            neighbour = (x + dx, y + dy)

            if not (0 <= neighbour[0] < width and 0 <= neighbour[1] < height):
                continue # buiten grid check
            if grid[y][x]["walls"][direction]:
                continue # open/dichte muur check

            tentative_g = g_values[current] + 1 # nieuwe g waarde = altijd +1
            if neighbour not in g_values or tentative_g < g_values[neighbour]:
    # check zijn we hier al geweest? welke g waarde was het laagst?
                g_values[neighbour] = tentative_g
                came_from[neighbour] = current # houdt path bij
                f_value = tentative_g + heuristic(neighbour)
                heapq.heappush(open_list, (f_value, neighbour)) # zet f waarde in lijst met coordinaat

    return None
