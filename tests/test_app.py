import pytest
from app import App
from unittest.mock import patch
from app.commands.command_interface import CommandInterface


def test_app_unknown_then_valid_command(capfd, monkeypatch):
    """
    Test an unknown command followed by a valid command,
    ensuring the REPL actually continues and covers line 50-51.
    """
    # We'll enter one unknown command, then 'menu', then 'exit'
    inputs = iter([
        "bogus_command",  # triggers the unknown-branch with 'continue'
        "menu",           # valid command -> checks that the REPL truly continued
        "exit"
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from app import App
    App.start()

    out, err = capfd.readouterr()
    assert "Unknown command. Type 'menu' to see available commands," in out
    assert "Available commands:" in out
    assert "Exiting the interactive calculator..." in out
    # No errors
    assert err == ""




def test_command_interface_abstract_methods():
    """
    Test that calling the abstract property/method on a partial subclass
    actually hits the NotImplementedError lines, for coverage.
    """
    class PartialCommand(CommandInterface):
        # We'll implement ONLY one of the abstract methods, not both
        @property
        def name(self) -> str:
            # call super().name to hit the NotImplementedError
            return super().name

        def execute(self, args: list[str]) -> str:
            return super().execute(args)

    partial = PartialCommand()

    # The property 'name' calls super().name => NotImplementedError
    with pytest.raises(NotImplementedError):
        _ = partial.name

    # The method 'execute' calls super().execute => NotImplementedError
    with pytest.raises(NotImplementedError):
        partial.execute(["1", "2"])



def test_app_divide_by_zero(capfd, monkeypatch):
    """Test that 'divide 5 0' triggers the ZeroDivisionError branch in the REPL."""
    inputs = iter(["divide 5 0", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    from app import App
    App.start()
    out, err = capfd.readouterr()

    assert "Error: Cannot divide by zero." in out
    assert "Exiting the interactive calculator..." in out


def test_app_value_error(capfd, monkeypatch):
    """
    Test that 'add abc 2' triggers the ValueError branch in the REPL,
    printing 'Error: Invalid numeric input for add command.' or similar.
    """
    inputs = iter(["add abc 2", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    from app import App
    App.start()
    out, err = capfd.readouterr()

    assert "Error: Invalid numeric input" in out
    assert "Exiting the interactive calculator..." in out




def test_app_unexpected_error(capfd, monkeypatch):
    """
    Test that a general Exception in command execution is caught by 'except Exception'.
    We mock the plugin manager's get_command so it returns a command that raises a RuntimeError.
    """
    # We can mock the command class on the fly:
    class MockErrorCommand:
        def __init__(self):
            pass
        def execute(self, args):
            raise RuntimeError("Simulated unexpected error")
        @property
        def name(self):
            return "mockerror"

    # We also mock the PluginManager's get_command to return this class if the user types 'error'
    def mock_get_command(command_name):
        if command_name == "error":
            return MockErrorCommand
        return None

    # Provide user input: first "error 1 2" to trigger the exception, then "exit"
    inputs = iter(["error 1 2", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Patch the real plugin manager method
    with patch("app.commands.plugin_manager.PluginManager.get_command", side_effect=mock_get_command):
        from app import App
        App.start()
        out, err = capfd.readouterr()

        # We expect the "Unexpected error: Simulated unexpected error" message in stderr
        assert "Unexpected error: Simulated unexpected error" in err
        assert "Exiting the interactive calculator..." in out




def test_app_empty_input(capfd, monkeypatch):
    """
    Test that an empty input line is simply ignored and the REPL continues.
    We'll then type 'exit' to finish.
    """
    inputs = iter(['', 'exit'])  # first is empty line, then exit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from app import App
    App.start()
    out, err = capfd.readouterr()

    assert "Welcome to the Interactive Calculator. Type 'exit' to exit." in out
    assert "Exiting the interactive calculator..." in out
    # No error or unknown command message should appear for the empty line
    assert "Unknown command" not in out
    assert err == ""



def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    App.start()
    out, err = capfd.readouterr()

    # Check that the initial greeting is printed and the REPL exits gracefully
    assert "Welcome to the Interactive Calculator. Type 'exit' to exit." in out
    assert "Exiting the interactive calculator..." in out

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    # Simulate user entering an unknown command followed by 'exit'
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    App.start()
    out, err = capfd.readouterr()

    # Check that the REPL responds to an unknown command and then exits after 'exit' command
    assert "Welcome to the Interactive Calculator. Type 'exit' to exit." in out
    assert "Unknown command. Type 'menu' to see available commands, or 'exit' to quit." in out
    assert "Exiting the interactive calculator..." in out
