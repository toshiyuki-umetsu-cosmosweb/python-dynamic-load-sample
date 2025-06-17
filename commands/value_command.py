"""
Loading test.
This file is used to confirm the behavior to import module which is specified
in this file.
"""
from typing import Any, Final, Union
import json
import core


def _value_get_commmand(args: list[str]) -> None:
    """ Process value get command. """
    if len(args) == 3:
        key: str = args[2]
        if key in core.COMMON_DATA:
            value: Union[int, float, str] = core.COMMON_DATA[key]
            print(json.dumps(value))
        else:
            raise ValueError(f"'{key}' not found.")
    elif len(args) == 2:
        for key, value in core.COMMON_DATA.items():
            print(f"{key}={json.dumps(value)}")
    else:
        raise ValueError("Invalid arguments for 'value get' command. ")


def _value_set_command(args: list[str]) -> None:
    """ Process value set command. """
    if len(args) != 4:
        raise ValueError("Invalid arguments for 'value set' command. ")

    key: str = args[2]
    value: Any = json.loads(args[3])
    if not isinstance(value, (int, float, str)):
        raise ValueError("Value must be an int, float, or str.")
    core.COMMON_DATA[key] = value


def _value_command(args: list[str]) -> None:
    """
    Process value command.
    This command is used to set or get a value.
    """
    if len(args) < 2:
        print("Usage:")
        print("  value get - Get all values.")
        print("  value get <key> - Get the value for the specified key.")
        print("  value set <key> <value> - "
              "Set the value for the specified key.")
        return

    if args[1] == "get":
        _value_get_commmand(args)
    elif args[1] == "set":
        _value_set_command(args)


VALUE_COMMAND: Final[dict[str, Any]] = {
    "name": "value",
    "description": "Set/Get a value.",
    "procedure": _value_command
}
