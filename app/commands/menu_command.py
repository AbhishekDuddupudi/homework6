"""
menu_command.py: Defines the "menu" command plugin which lists all available commands.
"""
from app.commands.command_interface import CommandInterface
from app.commands.plugin_manager import PluginManager


class MenuCommand(CommandInterface):
    """
    Menu command that lists all recognized commands by the PluginManager.
    """

    @property
    def name(self) -> str:
        return "menu"

    def execute(self, args: list[str]) -> str:
        """
        The 'menu' command takes no arguments and returns a list of available commands.
        """
        if args:
            raise ValueError("The 'menu' command takes no arguments.")

        # We re-instantiate the PluginManager to get a fresh list of commands
        pm = PluginManager()
        commands = sorted(pm._commands.keys())  # protected member usage for simplicity
        return f"Available commands: {', '.join(commands)}"
