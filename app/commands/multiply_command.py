"""
multiply_command.py: Defines the "multiply" command plugin.
"""
from app.commands.command_interface import CommandInterface


class MultiplyCommand(CommandInterface):
    """
    Command to multiply two numbers.
    Usage: multiply x y
    """

    @property
    def name(self) -> str:
        return "multiply"

    def execute(self, args: list[str]) -> str:
        """
        Expects exactly two numeric arguments.
        Returns a string: "x * y = result"
        Raises ValueError if number of args is incorrect or if conversion fails.
        """
        if len(args) != 2:
            raise ValueError("Invalid number of arguments for multiply command. Usage: multiply <num1> <num2>.")

        try:
            x = float(args[0])
            y = float(args[1])
        except ValueError:
            raise ValueError("Invalid numeric input for multiply command.")

        result = x * y
        return f"{x} * {y} = {result}"
