"""
divide_command.py: Defines the "divide" command plugin.
"""
from app.commands.command_interface import CommandInterface


class DivideCommand(CommandInterface):
    """
    Command to divide two numbers.
    Usage: divide x y
    """

    @property
    def name(self) -> str:
        return "divide"

    def execute(self, args: list[str]) -> str:
        """
        Expects exactly two numeric arguments.
        Returns a string: "x / y = result"
        Raises ValueError if usage is incorrect or if numeric conversion fails,
        ZeroDivisionError if y == 0.
        """
        if len(args) != 2:
            raise ValueError("Invalid number of arguments for divide command. Usage: divide <num1> <num2>.")

        try:
            x = float(args[0])
            y = float(args[1])
        except ValueError:
            raise ValueError("Invalid numeric input for divide command.")

        if y == 0:
            raise ZeroDivisionError("Attempted to divide by zero.")

        result = x / y
        return f"{x} / {y} = {result}"
