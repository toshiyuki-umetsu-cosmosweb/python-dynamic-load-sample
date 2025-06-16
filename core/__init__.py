""" Initial script for the core module. """
from typing import Final, Union


_GREEN: Final[str] = "\033[32m"
""" ANSI escape code for green text. """
_END: Final[str] = "\033[0m"
""" ANSI escape code to reset text formatting. """


COMMON_DATA: Final[dict[str, Union[int, float, str]]] = {}
""" Common data shared across scripts. """

print(_GREEN + "-- core module loaded. --" + _END)
