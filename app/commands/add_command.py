"""
add_command.py: Defines the "add" command plugin.
"""
from app.commands.command_interface import CommandInterface


class AddCommand(CommandInterface):
    """
    Command to add two numbers.
    Usage: add x y
    """

    @property
    def name(self) -> str:
        return "add"

    def execute(self, args: list[str]) -> str:
        """
        Expects exactly two numeric arguments.
        Returns a string of the format: "x + y = result"
        Raises ValueError if number of args is incorrect or if conversion fails.
        """
        if len(args) != 2:
            raise ValueError("Invalid number of arguments for add command. Usage: add <num1> <num2>.")

        try:
            x = float(args[0])
            y = float(args[1])
        except ValueError:
            raise ValueError("Invalid numeric input for add command.")

        result = x + y
        # Output a nicely formatted string
        return f"{x} + {y} = {result}"
