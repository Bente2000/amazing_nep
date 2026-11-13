"""Check whether the values in the config file are of the right type.
"""

class ConfigError(Exception):
    """Error class that is used to label config errors as such.

    Parameters
    ----------
    Exception         ## meer info
        
    """
    "Configuration file is missing or invalid."


def parse_int(key: str, value: str) -> int:
    """Check whether the given value can be converted to an integer.

    Parameters
    ----------
    key : str
        The key belonging to the value.
    value : str
        The value to convert.

    Returns
    -------
    int
        The value converted to an integer.

    Raises
    ------
    ConfigError
        If a wrong type is passed.
    """
    try:
        return int(value)
    except ValueError:
        raise ConfigError (f"{key} must be an integer, got value"
                           f"'{value}'") from None


def parse_bool(key: str, value: str) -> bool:
    """Check whether a given value is a bool.

    Parameters
    ----------
    key : str
        The key belonging to the given value (always "Perfect").
    value : str
        The value that is being checked.

    Returns
    -------
    bool
        True if value is "True", False if value is "False".

    Raises
    ------
    ConfigError
        If the given value is not a bool.
    """
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    raise ConfigError(f"{key} must be True or False, got '{value}'")


def parse_coordinates(key: str, value: str) -> tuple[int, int]:
    """Check whether a given value can be converted to tuple of two integers.

    Parameters
    ----------
    key : str
        The key belonging to the value being checked.
    value : str
        The value being checked.

    Returns
    -------
    tuple[int, int]
        The value converted to coordinates.

    Raises
    ------
    ConfigError
        If the given value can't be converted to coordinates.
    """
    parts = value.split(',')
    if len(parts) != 2:
        raise ConfigError(f"{key} must be in the form 'x,y', got '{value}'")
    return (parse_int(key, parts[0].strip()), parse_int(key, parts[1].strip()))
    # return catches ValueErrors in parse_int()
