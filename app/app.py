"""
app.py: Defines the main application REPL, which delegates to the plugin manager
to find the appropriate command to run.
"""
import sys
import logging
from app.commands.plugin_manager import PluginManager

logger = logging.getLogger(__name__)


class App:
    """Main application class responsible for the REPL loop."""
    @staticmethod
    def start() -> None:
        """
        Starts the REPL (Read-Eval-Print Loop).
        Commands are discovered via the PluginManager.
        """
        logger.info("Calculator App has started. Enter commands or type 'exit' to quit.")
        print("Welcome to the Interactive Calculator. Type 'exit' to exit.")
        plugin_manager = PluginManager()

        while True:
            # Display REPL prompt
            user_input = input(">>> ").strip()
            if not user_input:
                # Just ignore empty lines
                continue

            # If user types 'exit', we terminate
            if user_input.lower() == "exit":
                logger.info("User requested exit.")
                print("Exiting the interactive calculator...")
                break

            # Parse command name and arguments
            parts = user_input.split()
            cmd_name = parts[0].lower()
            args = parts[1:]

            # Lookup command from plugin manager
            command_class = plugin_manager.get_command(cmd_name)

            if command_class is None:
                logger.warning("Unknown command encountered: %s", cmd_name)
                print(
                    "Unknown command. Type 'menu' to see available commands, or 'exit' to quit."
                )
                continue

            # Create an instance of the command and execute
            command_instance = command_class()
            try:
                output = command_instance.execute(args)
                if output is not None:
                    logger.info("Command '%s' executed successfully with args: %s", cmd_name, args)
                    print(output)
            except ValueError as exc:
                # Command-specific usage errors or numeric conversion errors
                logger.error("Command '%s' raised ValueError: %s", cmd_name, exc)
                print(f"Error: {exc}")
            except ZeroDivisionError:
                logger.error("Command '%s' caused ZeroDivisionError with args: %s", cmd_name, args)
                print("Error: Cannot divide by zero.")
            except Exception as exc:  # pylint: disable=broad-except
                # Catch any other unexpected errors
                logger.exception("Command '%s' caused an unexpected error", cmd_name)
                print(f"Unexpected error: {exc}", file=sys.stderr)
