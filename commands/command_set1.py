""" Sample command set """
from typing import Any, Final

print(__file__ + " executed.")

# This command is loaded.
COMMAND_XXX: Final[dict[str, Any]] = {
    "name": "xxx",
    "description": "This is a sample command.",
    "procedure": lambda args: print(f"Executing xxx command with args: {args}")
}

# Bellow entries are not loaded due to type mismatches.
COMMAND_YYY: Final[dict[str, Any]] = {
    "name": "yyy",
    "description": "This is a sample command.",
    "procedure": lambda a, c, args: print("Executing yyy command.")
}

# This command is loaded.
COMMAND_ZZZ: Final[dict[str, Any]] = {
    "name": "zzz",
    "description": "This is a sample command.",
    "procedure": lambda args: print(f"Executing zzz command with args: {args}")
}
