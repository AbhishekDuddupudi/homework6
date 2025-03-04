import pytest
from app.commands.add_command import AddCommand
from app.commands.subtract_command import SubtractCommand
from app.commands.multiply_command import MultiplyCommand
from app.commands.divide_command import DivideCommand
from app.commands.menu_command import MenuCommand
from app.commands.plugin_manager import PluginManager

def test_add_command_success():
    cmd = AddCommand()
    assert cmd.name == "add"
    result = cmd.execute(["3", "4"])
    assert result == "3.0 + 4.0 = 7.0"

def test_add_command_invalid_args_count():
    cmd = AddCommand()
    with pytest.raises(ValueError) as exc:
        cmd.execute(["5"])
    assert "Invalid number of arguments" in str(exc.value)

def test_add_command_invalid_numeric():
    cmd = AddCommand()
    with pytest.raises(ValueError) as exc:
        cmd.execute(["abc", "2"])
    assert "Invalid numeric input" in str(exc.value)

def test_subtract_command_success():
    cmd = SubtractCommand()
    assert cmd.name == "subtract"
    result = cmd.execute(["9", "4"])
    assert result == "9.0 - 4.0 = 5.0"

def test_subtract_command_invalid_args_count():
    cmd = SubtractCommand()
    with pytest.raises(ValueError):
        cmd.execute(["7"])  # only one arg

def test_subtract_command_invalid_numeric():
    cmd = SubtractCommand()
    with pytest.raises(ValueError):
        cmd.execute(["foo", "bar"])

def test_multiply_command_success():
    cmd = MultiplyCommand()
    assert cmd.name == "multiply"
    result = cmd.execute(["3", "4"])
    assert result == "3.0 * 4.0 = 12.0"

def test_multiply_command_invalid_args_count():
    cmd = MultiplyCommand()
    with pytest.raises(ValueError):
        cmd.execute(["7"])

def test_multiply_command_invalid_numeric():
    cmd = MultiplyCommand()
    with pytest.raises(ValueError):
        cmd.execute(["foo", "bar"])

def test_divide_command_success():
    cmd = DivideCommand()
    assert cmd.name == "divide"
    result = cmd.execute(["20", "4"])
    assert result == "20.0 / 4.0 = 5.0"

def test_divide_command_invalid_args_count():
    cmd = DivideCommand()
    with pytest.raises(ValueError):
        cmd.execute(["20"])

def test_divide_command_invalid_numeric():
    cmd = DivideCommand()
    with pytest.raises(ValueError):
        cmd.execute(["abc", "4"])

def test_divide_command_zero_division():
    cmd = DivideCommand()
    with pytest.raises(ZeroDivisionError):
        cmd.execute(["5", "0"])

def test_menu_command_success(monkeypatch):
    """
    Test that the menu command returns available commands.
    We'll monkeypatch the plugin manager so it returns a known set of commands.
    """
    # Possibly patch PluginManager to avoid scanning the actual filesystem
    original_init = PluginManager.__init__
    
    def mock_init(self):
        self._commands = {
            "add": AddCommand,
            "subtract": SubtractCommand,
            "menu": MenuCommand
        }

    monkeypatch.setattr(PluginManager, "__init__", mock_init)

    cmd = MenuCommand()
    result = cmd.execute([])
    # The commands are "add", "subtract", "menu" (sorted: add, menu, subtract)
    assert "add, menu, subtract" in result

    # revert PluginManager.__init__ so other tests aren't affected
    monkeypatch.setattr(PluginManager, "__init__", original_init)

def test_menu_command_with_args():
    cmd = MenuCommand()
    with pytest.raises(ValueError):
        cmd.execute(["extra_arg"])
