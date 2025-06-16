"""
module command definition.
"""
from typing import Any, Final
import os
import sys
import types
import fnmatch


def _get_script_path(file_path: str) -> str:
    """
    Getting display script path.
    This function replace absolute path to hide sys.path.

    Parameters
    ----------
    file_path : str
        File path of script.

    Returns
    -------
    str
        Display script path.
        If the file_path is not in sys.path, return the original file_path.
    """
    for sys_path in sys.path:
        if file_path.startswith(sys_path):
            # sys.pathのパスを除去して相対パスにする。
            relative_path: str = file_path[len(sys_path):].strip(os.sep)
            return os.path.join("${sys.path}", relative_path)

    return file_path


def _filter_module(patterns: list[str]) -> list[str]:
    """
    Filter modules that match the given patterns.

    Parameters
    ----------
    patterns : list[str]
        Patterns to filter modules.

    Returns
    -------
    list[str]
        List of module names that match the patterns.
    """
    module_list: list[str] = []
    for pattern in patterns:
        results: list[str] = fnmatch.filter(sys.modules.keys(), pattern)
        for module_name in results:
            if module_name not in module_list:
                module_list.append(module_name)
    return module_list


def _module_command(args: list[str]) -> None:
    """
    Process module command.
    """
    module_names: list[str]
    if len(args) > 1:
        module_names = _filter_module(args[1:])
    else:
        module_names = list(sys.modules.keys())
        module_names.sort()

    for module_name in module_names:
        if module_name in sys.modules:
            mt: types.ModuleType = sys.modules[module_name]
            if mt is not None:
                file_path: str
                if hasattr(mt, "__file__"):
                    file_path = _get_script_path(getattr(mt, "__file__"))
                else:
                    file_path = "(built-in)"
                print(f"{module_name}: {file_path}")
            else:
                print(f"{module_name}: (Unloaded)")
        else:
            print(f"{module_name}: (NotLoaded)")


MODULE_COMMAND: Final[dict[str, Any]] = {
    "name": "module",
    "description": "List loaded modules and their file paths.",
    "procedure": _module_command
}
