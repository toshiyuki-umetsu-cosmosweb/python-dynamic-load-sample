"""
An entry point for a command-line application that dynamically loads
"""
from __future__ import annotations
from typing import Optional, Any, Type, Literal, TypedDict, Callable
import sys
import signal
import os
import shlex
import pathlib
import types
import inspect
import importlib.machinery
import importlib.util
import traceback


class _CommandEntry(TypedDict):
    """
    Type definition for a command entry.
    """
    name: str
    description: str
    procedure: Callable[[list[str]], None]


class _Application:
    """ Application class that manages commands and runs the application. """
    def __init__(self) -> None:
        """
        Initialize the application.
        """
        self._run: bool = True
        self._commands: dict[str, _CommandEntry] = {}

    def __enter__(self) -> _Application:
        """
        Process when entering the `with` statement.

        Returns
        -------
        _Application
            _Application を返します。
        """
        return self

    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 tb: Optional[Any]) -> Literal[False]:
        """
        Process when exiting the `with` statement.

        Parameters
        ----------
        exc_type : Optional[Type[BaseException]]
            type of the exception if exiting with an exception.
        exc_value : Optional[BaseException]
            value of the exception if exiting with an exception.
        tb : Optional[Any]
            Traceback object if exiting with an exception.

        Returns
        -------
        bool
            When suppressing exceptions in the `with` block, return True.
            When notifying exceptions in the `with` block, return False.
        """
        return False

    def run(self) -> None:
        """
        Application execution routine.
        """
        self._load_commands()
        self._run = True
        signal.signal(signal.SIGINT, self._signal_handler)

        while self._run:
            try:
                command = input("> ")
                args: list[str] = shlex.split(command)
                if args:
                    self._run_command(args)
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt received")
                self._run = False
            except Exception as e:  # pylint: disable=broad-exception-caught
                traceback.print_exception(type(e), e, e.__traceback__)

    def _signal_handler(self, signum: int, frame: Optional[Any]) -> None:
        """
        Signal handler for SIGINT.

        Parameters
        ----------
        signum : int
            Signal number that was received.
        frame : Optional[Any]
            Frame object where the signal was received.
        """
        print(f"Received signal {signum}, shutting down...")
        self._run = False

    def _load_commands(self) -> None:
        """
        Load commands dynamically from the commands directory.

        Notes
        -----
        This method scans the `commands` directory for Python files
        """
        self._commands.clear()
        local_dir: str = os.path.dirname(os.path.abspath(__file__))
        print(f"Running script from: {local_dir}")

        # Load commands from the `commands` directory
        command_dir: pathlib.Path = pathlib.Path(
            os.path.join(local_dir, "commands")).resolve()
        for python_file in command_dir.glob("*.py"):
            if not python_file.is_file():
                continue

            try:
                cmd_entries: list[_CommandEntry] \
                    = self._load_command("command", python_file)
                if cmd_entries:
                    for cmd_entry in cmd_entries:
                        self._commands[cmd_entry["name"]] = cmd_entry
                else:
                    print("No valid command entry found. skip. "
                          + python_file.name)
            except ValueError as e:
                print(f"Loading command {python_file.name} failed: {e}")
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Loading command {python_file.name} failed.")
                traceback.print_exception(type(e), e, e.__traceback__)
        self._load_system_commands()

    def _load_command(self, prefix: str,
                      script_path: pathlib.Path) -> list[_CommandEntry]:
        """
        Load command.

        Parameters
        ----------
        script_path : pathlib.Path
            Path to the script file to load.

        Returns
        -------
        list[CommandEntry]
            An entry list of commands loaded from the script.
        """
        module_name: str = prefix + "." + script_path.stem
        module: types.ModuleType

        if module_name in sys.modules:
            # If the module is already loaded, remove it.
            del sys.modules[module_name]

        # Create a module spec and load the module
        spec: Optional[importlib.machinery.ModuleSpec] \
            = importlib.util.spec_from_file_location(module_name, script_path)
        if (spec is None) or (spec.loader is None):
            raise ValueError(
                f"Could not find module spec for {module_name}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        cmd_entries: list[_CommandEntry] = []

        for _, obj in vars(module).items():
            if isinstance(obj, dict) and self._is_valid_entry(obj):
                name: str = obj["name"]
                description: str = obj.get("description", "")
                proecdure: Callable[[list[str]], None] = obj["procedure"]
                cmd_entries.append(_CommandEntry(
                    name=name, description=description,
                    procedure=proecdure))

        return cmd_entries

    def _load_system_commands(self) -> None:
        """
        Load system commands.

        Notes
        -----
        This method adds default commands such as `help`, `q`, and `reload`.
        """
        # デフォルトのコマンドセットを追加
        self._commands["help"] = _CommandEntry(
            name="help",
            description="Show help message",
            procedure=self._proc_help_command)
        self._commands["q"] = _CommandEntry(
            name="q",
            description="Quit the application",
            procedure=lambda args: setattr(self, "_run", False))
        self._commands["reload"] = _CommandEntry(
            name="reload",
            description="Reload commands.",
            procedure=lambda args: self._load_commands())

    def _is_valid_entry(self, obj: dict[str, Any]) -> bool:
        """
        Checking if the given obj is a valid command entry.

        Parameters
        ----------
        obj : Any
            Obuject to check

        Returns
        -------
        bool
            If the object is a valid command entry, return True.
        """
        if not isinstance(obj, dict):
            return False

        if ("name" not in obj) or ("procedure" not in obj):
            return False

        if (not isinstance(obj["name"], str)) or (not obj["name"]):
            return False

        # Check instance of 'procedure' member
        procedure: Any = obj["procedure"]
        if not callable(procedure):
            return False

        sig: inspect.Signature = inspect.signature(procedure)
        params: tuple[inspect.Parameter, ...] = tuple(sig.parameters.values())
        if len(params) != 1:
            return False

        return True

    def _run_command(self, args: list[str]) -> None:
        """
        Execute a command.

        Parameters
        ----------
        args : list[str]
            Arguments for the command, where the first element is the command
        """
        cmd: str = args[0]
        if cmd in self._commands:
            cmd_entry: _CommandEntry = self._commands[cmd]
            cmd_entry["procedure"](args)
        else:
            print(f"Unknown command: {cmd}. "
                  "Type 'help' for available commands.")

    def _proc_help_command(self, args: list[str]) -> None:
        """
        Process the help command.
        """
        commands: list[str] = list(self._commands.keys())
        commands.sort()

        for cmd in commands:
            cmd_entry: _CommandEntry = self._commands[cmd]
            if cmd_entry["description"]:
                print(f"{cmd}: {cmd_entry['description']}")


def _main() -> None:
    """
    Execute the application.
    """
    try:
        with _Application() as app:
            app.run()
        sys.exit(0)
    except Exception as e:  # pylint: disable=broad-exception-caught
        traceback.print_exception(type(e), e, e.__traceback__)
        sys.exit(1)


if __name__ == "__main__":
    _main()
