"""Creates a maze with only one solution (perfect maze).
"""

import random
from .grid import Grid, Position, get_neighbours, remove_wall

# wanneer je cell binnen stapt haal je 1 muur weg en markeer als visited,
# hierdoor onstaan er geen loops
def carve_perfect_maze(grid: Grid, entry: Position, rng: random.Random, # BEZIG
                       blocked: set[Position]) -> None:
    """Creates a perfect maze out of a fresh grid.

    Mark the 42 pattern as visited so we never enter it.
    We keep a list of cells, this is the trail. We start creating the trail at
    entry. If our current cell has any unvisited neighbours, we enter one of
    them randomly. If all neighbouring cells are already visited, we pop the
    current cell from the list and thus move back.
    We do this until every cell is visited and no trail is left behind.

    Parameters
    ----------
    grid : Grid
        list[list[dict[str, Any]]]
        A grid of cells where all the `"walls"` are closed at first. Cells can
        be marked as `"visited"` and `"walls"` can be broken open to create a
        maze.
    entry : Position
        tuple[int, int]
        The entry coordinates of the maze.
    rng : random.Random
        The random number generator created in MazeGenerator. We use it to 
        decide which unvisited neighbour we will enter next.
    blocked : set[Position]
        set[tuple[int, int]]
        Set of cells that form the 42 pattern. They shouldn't be entered when
        creating the maze.
    """
    for bx, by in blocked: # blocked is pattern_cells
        grid[by][bx]["visited"] = True # markeer alle cells in blocked set

    x, y = entry
    grid[y][x]["visited"] = True # waar we zijn is visited
    trail = [entry] # trail = list van tuples (positions)

    while trail: # ends when trail is empty = alles terug gepopt naar start
        # (terwijl alle neighbours van die route zijn gecheckt), recursie werkt
        # ook maar een grote maze zou over de recursie limiet heen gaan
        x, y = trail[-1] # gives last element in list (begint bij entry/start) == current position
        unvisited = [ # all unvisited neighbours get stored (set grows)
            (direction, position)
            for direction, position in get_neighbours(grid, x, y) # get neighbours returns list[tuple["N", (6,7)]
            if not grid[position[1]][position[0]]["visited"] # move through neighbours and check for visited
        ]

        if unvisited: # IF current has unvisited neighbour, pick one at random,
            # open wall to it, mark it visited and push (append) it (neighbour to trail)
            direction, neighbour = rng.choice(unvisited) #random.choice() returns random element from non-empty sequence
            remove_wall(grid, (x, y), direction, neighbour) # zet current position cell op False en opposite cell ook op false = geen muur
            grid[neighbour[1]][neighbour[0]]["visited"] = True # mark as visited
            trail.append(neighbour) # groei trail, walk forward (add neighbour to current)
        else: # dead end, step back (exit current), check neighbours vorige cell nog een keer (backtracking behaviour)
            trail.pop() # removes (en returns) last item in list (stack)
            # keuze: alleen terug gaan bij een dood einde zorgt voor lange kronkelige
            # gangen (voeg toe aan README), elke (unblocked) cell is precies 1x gepusht en 1x
            # gepopt == snel!
