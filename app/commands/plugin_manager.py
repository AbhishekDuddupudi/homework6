"""
plugin_manager.py: Auto-discovers command classes from the 'commands' folder
using pkgutil, and provides a lookup method to retrieve them by name.
"""
import pkgutil
import inspect
import importlib
import os
from app.commands.command_interface import CommandInterface


class PluginManager:
    """
    Scans the 'app/commands' package for classes that implement CommandInterface.
    Maintains a dict of command_name -> CommandClass.
    """

    def __init__(self):
        self._commands = {}
        self._discover_commands()

    def _discover_commands(self) -> None:
        """
        Auto-discovers all modules under 'app.commands' and finds
        classes implementing CommandInterface.
        """
        package_name = "app.commands"
        package_path = os.path.dirname(__file__)

        for finder, name, ispkg in pkgutil.iter_modules([package_path]):
            # Skip __init__.py or sub-packages
            if ispkg or name in ("__init__", "command_interface", "plugin_manager"):
                continue

            full_module_name = f"{package_name}.{name}"
            module = importlib.import_module(full_module_name)

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    issubclass(obj, CommandInterface)
                    and obj is not CommandInterface
                ):
                    # Register command by its 'name' property
                    cmd_instance = obj()
                    self._commands[cmd_instance.name] = obj

    def get_command(self, command_name: str):
        """
        Returns the command class for a given command name (str).
        If none is found, returns None.
        """
        return self._commands.get(command_name)
