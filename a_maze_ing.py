import sys
from mazegen import MazeGenerator
from config import build_config
from config_values import ConfigError
from display import run_menu
from output import write_output

#if __name__ == "__main__": # if a_maze_ing.py is imported instead of run,
#    # you're able to import the main (def main()) as well,
#    # so you're able to make a test file and import the program incl. main()


def main() -> int: # volgorde path check checken
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} config.txt", file=sys.stderr)
        return 1

    try:
        config = build_config(sys.argv[1])
    except ConfigError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    try:
        maze = MazeGenerator(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit_=config.exit_, # pas exit aan
            perfect=config.perfect,
            #seed=config.seed
        )
    except ValueError as e:  # raised by the validation in __init__
        print(f"Error: {e}", file=sys.stderr)
        return 1


    # VERSIE 3: write_output() uit maze class gehaald

    grid = maze.generate()
    path = maze.solve()
    try:
        #write_output(maze, config.output_file, path)
        write_output(grid, config.entry, config.exit_, config.output_file, path)
        run_menu(maze, config.output_file)
    except OSError as e:
        print(f"Error: cannot write ouput file: {e}", file=sys.stderr)
        return 1
    print("Maze generated.")

    return 0
#    try:                             # VERSIE 2: elke maze geprint, maar cirkel
#        maze.generate_solve("output_maze.txt")  # write_output() nu in class, niet oke!!
#        run_menu(maze, config.output_file)
#    except OSError as e:
#        print(f"Error: cannot write ouput file: {e}", file=sys.stderr)
#        return 1
#    
#    return 0

#    maze.generate()               # VERSIE 1:  alleen eerste maze geprint
#    path = maze.solve()
#    #if path is None:
#    #    print("No path found.")
#    #else:
#    #    print("Path:", path)
#    #    print(f"Path length: {len(path) - 1} steps")
#    try:
#        write_output(maze, config.output_file, path)
#    except OSError as e:
#        print(f"Error: cannot write ouput file: {e}", file=sys.stderr)
#        return 1
    #print("Maze generated.")
    #print(f"Entry: {maze.entry}")
    #print(f"Exit:  {maze.exit}")

    #path = maze.solve()
    #if path is None:
    #    print("No path found.")
    #else:
    #    print("Path:", path)
    #    print(f"Path length: {len(path) - 1} steps")
   # return 0


if __name__ == "__main__":
    sys.exit(main())
