"""
command_interface.py: Defines the standard interface (abstract base) that
all command plugins must implement.
"""
from abc import ABC, abstractmethod


class CommandInterface(ABC):
    """Abstract base class for commands in the calculator plugin system."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the command, e.g. 'add', 'subtract', etc."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, args: list[str]) -> str:
        """
        Execute the command with the given list of string arguments.
        Returns a string result or raises a ValueError / ZeroDivisionError as needed.
        """
        raise NotImplementedError
