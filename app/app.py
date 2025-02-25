"""
app.py: Defines the main application REPL, which delegates to the plugin manager
to find the appropriate command to run.
"""
import sys
from app.commands.plugin_manager import PluginManager


class App:
    """Main application class responsible for the REPL loop."""
    @staticmethod
    def start() -> None:
        """
        Starts the REPL (Read-Eval-Print Loop).
        Commands are discovered via the PluginManager.
        """
        print("Welcome to the Interactive Calculator. Type 'exit' to exit. Type menu to see existing commands")
        plugin_manager = PluginManager()

        while True:
            # Display REPL prompt
            user_input = input(">>> ").strip()
            if not user_input:
                # Just ignore empty lines
                continue

            # If user types 'exit', we terminate
            if user_input.lower() == "exit":
                print("Exiting the interactive calculator...")
                break

            # Parse command name and arguments
            parts = user_input.split()
            cmd_name = parts[0].lower()
            args = parts[1:]

            # Lookup command from plugin manager
            command_class = plugin_manager.get_command(cmd_name)

            if command_class is None:
                print(
                    "Unknown command. Type 'menu' to see available commands, or 'exit' to quit."
                )
                continue

            # Create an instance of the command and execute
            command_instance = command_class()
            try:
                output = command_instance.execute(args)
                if output is not None:
                    print(output)
            except ValueError as exc:
                # Command-specific usage errors or numeric conversion errors
                print(f"Error: {exc}")
            except ZeroDivisionError:
                print("Error: Cannot divide by zero.")
            except Exception as exc:  # pylint: disable=broad-except
                # Catch any other unexpected errors
                print(f"Unexpected error: {exc}", file=sys.stderr)
