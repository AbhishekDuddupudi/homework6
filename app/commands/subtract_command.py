"""
subtract_command.py: Defines the "subtract" command plugin.
"""
from app.commands.command_interface import CommandInterface


class SubtractCommand(CommandInterface):
    """
    Command to subtract two numbers.
    Usage: subtract x y
    """

    @property
    def name(self) -> str:
        return "subtract"

    def execute(self, args: list[str]) -> str:
        """
        Expects exactly two numeric arguments.
        Returns a string: "x - y = result"
        Raises ValueError if number of args is incorrect or if conversion fails.
        """
        if len(args) != 2:
            raise ValueError("Invalid number of arguments for subtract command. Usage: subtract <num1> <num2>.")

        try:
            x = float(args[0])
            y = float(args[1])
        except ValueError:
            raise ValueError("Invalid numeric input for subtract command.")

        result = x - y
        return f"{x} - {y} = {result}"
