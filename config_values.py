class ConfigError(Exception):
    "Configuration file is missing or invalid."


def parse_int(key: str, value: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise ConfigError (f"{key} must be an integer, got value"
                           f"'{value}'") from None


def parse_bool(key: str, value: str) -> bool:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    raise ConfigError(f"{key} must be True or False, got '{value}'")


def parse_coordinates(key: str, value: str) -> tuple[int, int]:
    parts = value.split(',')
    if len(parts) != 2:
        raise ConfigError(f"{key} must be in the form 'x,y', got '{value}'")
    return (parse_int(key, parts[0].strip()), parse_int(key, parts[1].strip()))
    # return catches ValueErrors in parse_int()
