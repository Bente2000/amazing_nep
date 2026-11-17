"""Build a configuration file that can be passed to the maze.
"""

from dataclasses import dataclass
from config_values import ConfigError, parse_int, parse_bool, parse_coordinates

# dataclass decorator uses __init__ and sets __repr__ to print class nicely
@dataclass(frozen=True) # frozen dataclasses don't have their values changed
class Config:
    """Used to store the mandatory keys found in the config file.

    Attributes
    ----------
    width : int
        Width of the maze.
    height : int
        Height of the maze.
    entry : tuple[int, int]
        Entry coordinates of the maze.
    _exit : tuple[int, int]
        Exit coordinates of the maze.
    output_file : str
        Stores the shortest found path in hexadecimals.
    perfect : bool
        When True there is one solution, when False there is multiple (pacman style).
    seed : int | None
        The seed of the maze or when None, a random maze will be generated.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit_: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None # int | None is the type hint,
    # = None is the default value for the None type (seed=None not needed now)


# initialize tuple for checking if keys are present
MANDATORY_KEYS: tuple[str, ...] = ("WIDTH", "HEIGHT", "ENTRY", "EXIT",
                                   "OUTPUT_FILE", "PERFECT")
"""The keys needed for the maze.
"""


def build_config(config_path: str) -> Config:
    """Read config.txt and build config class if the file contains the right types.

    Parameters
    ----------
    config_path : str
        The path to the config file

    Returns
    -------
    Config
        All the values needed for generating a maze.

    Raises
    ------
    ConfigError
        If a mandatory key is missing.
    """
    raw: dict[str, str] = read_config(config_path) # raw is a dict
    missing: list[str] = [key for key in MANDATORY_KEYS if key not in raw]
    if missing:
        raise ConfigError(f"missing mandatory key(s): {', '.join(missing)}")

    width = parse_int("WIDTH", raw["WIDTH"]) # takes str (respresenting key) and value belonging to key in raw[]
    height = parse_int("HEIGHT", raw["HEIGHT"])
    entry = parse_coordinates("ENTRY", raw["ENTRY"])
    exit_= parse_coordinates("EXIT", raw["EXIT"])
    seed: int | None = parse_int("SEED", raw["SEED"]) if "SEED" in raw else None # create seed variable

    return Config(
            width=width,
            height=height,
            entry=entry,
            exit_=exit_,
            output_file=raw["OUTPUT_FILE"],
            perfect=parse_bool("PERFECT", raw["PERFECT"]),
            seed=seed)
    # return Config class


def read_config(config_path: str) -> dict[str, str]: # returns raw file as dict
    """

    Parameters
    ----------
    config_path : str
        The path to the config file.

    Returns
    -------
    dict[str, str]
        The config file parsed to a dictionary with the right syntax and elements.

    Raises
    ------
    ConfigError
        If a key, value or seperator is missing.
        If duplicate key is found.
        If the config file can't be found or read.
    """
    maze_data: dict[str, str] = {} # initialize empty dict
    try: #read key=value pairs from file to dict, ignore blank and # lines
        with open(config_path, encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if not line or line.startswith('#'):
                    continue
                key, seperator, value = line.partition('=')
                key = key.strip().upper()
                value = value.strip()
                if not seperator or not key or not value:
                    raise ConfigError(f"line {line_number}: expected KEY=VALUE"
                                      f", got '{line}")
                if key in maze_data:
                    raise ConfigError(f"line {line_number}: duplicate '{key}'")
                maze_data[key] = value # loop through file to add to dict
    except FileNotFoundError: #only ConfigError is shown bc 'from None'
        raise ConfigError(f"file not found: '{config_path}'") from None
    except UnicodeDecodeError: #file content not in utf-8 (binary or not ascii)
        raise ConfigError(f"'{config_path}' isn't a valid test file") from None
    except OSError as e: # includes PermissionError, IsADirectoryError
        raise ConfigError(f"can't read '{config_path}': {e}") from None # e shows error message by OSError specifying error
    return maze_data
