# Interactive Command-Line Calculator with Plugin Architecture

This project demonstrates a **plugin-based** command pattern architecture in Python, featuring a REPL (Read-Eval-Print Loop), robust error handling, and 100% test coverage with **pytest**.

---

## Table of Contents

1. [Overview](#overview)  
2. [Key Features](#key-features)  
3. [Project Structure](#project-structure)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Plugin Architecture](#plugin-architecture)  
7. [Testing](#testing)  
8. [Contributing](#contributing)  
9. [License](#license)

---

## Overview

This calculator runs continuously in a REPL, enabling you to type commands such as `add`, `subtract`, `multiply`, `divide`, and `menu`. Each command is implemented as a **plugin** in the `app/commands/` folder. New commands can be easily added by dropping in a new file that implements the **command interface**.

### Goals:

- Provide a **clean plugin architecture** (via Python’s `pkgutil` and reflection).
- Handle **errors** gracefully: invalid arguments, invalid numeric input, division by zero, unknown commands, etc.
- Achieve **100% coverage** for all code, including REPL logic and plugin commands.

---

## Key Features

1. **Continuous REPL**:  
   - Type commands at the `>>>` prompt.  
   - Type `exit` to quit.

2. **Basic Arithmetic Commands**:  
   - `add <x> <y>` → outputs `x + y = result`  
   - `subtract <x> <y>` → outputs `x - y = result`  
   - `multiply <x> <y>` → outputs `x * y = result`  
   - `divide <x> <y>` → outputs `x / y = result`  
   - Zero-division triggers a specific error message.

3. **Menu Command**:  
   - `menu` → lists all available commands dynamically discovered via the **PluginManager**.

4. **Plugin Architecture**:  
   - Each command is a self-contained `.py` file in `app/commands/`.
   - **PluginManager** automatically discovers and registers them, no need to modify the main application.

5. **Robust Error Handling**:  
   - Usage errors (wrong number of arguments) → `ValueError`.  
   - Invalid numeric input → `ValueError`.  
   - Divide by zero → `ZeroDivisionError`.  
   - Unknown command → “Unknown command. Type 'menu' to see available commands, or 'exit' to quit.”  
   - Unexpected errors → Caught and printed to `stderr`.

6. **100% Test Coverage**:  
   - **Unit tests** for each command.  
   - **Integration tests** for the REPL (via monkeypatching user input).  
   - Coverage measured by `pytest-cov`.

---

## Project Structure

```
calc_design_patterns/
├── .github/
│   └── workflows/
│       └── python-app.yml        # GitHub Actions CI
├── app/
│   ├── __init__.py               # Exports the App
│   ├── app.py                    # REPL code
│   └── commands/
│       ├── __init__.py
│       ├── add_command.py
│       ├── subtract_command.py
│       ├── multiply_command.py
│       ├── divide_command.py
│       ├── menu_command.py
│       ├── command_interface.py  # Abstract base for commands
│       └── plugin_manager.py     # Auto-discovers commands
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_app.py               # Integration tests for the REPL
│   └── test_commands.py          # Unit tests for each command
├── .coveragerc                   # Coverage config
├── .gitignore
├── .pylintrc                     # Pylint config
├── main.py                       # Entry point (calls App.start())
├── pytest.ini                    # Pytest config
├── readme.md                     # (This file)
└── requirements.txt              # Dependencies
```

---

## Installation

1. **Clone** or download the repository:
   ```bash
   git clone https://github.com/AbhishekDuddupudi/homework5
   cd homework5
   ```

2. **Create and activate** a virtual environment (optional but recommended):
   ```bash
   python -m venv homework5
   source homework5/bin/activate
   ```

3. **Install** the required packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run** the calculator:
   ```bash
   python main.py
   ```
2. You’ll see:
   ```
   Welcome to the Interactive Calculator. Type 'exit' to exit.
   >>>
   ```
3. **Try out** commands:
   - `add 5 3`  
   - `subtract 9 4`  
   - `multiply 4 5`  
   - `divide 20 4`  
   - `menu`  
   - `exit`

4. **Sample Session**:
   ```
   >>> add 5 3
   5.0 + 3.0 = 8.0
   >>> divide 5 0
   Error: Cannot divide by zero.
   >>> add abc 2
   Error: Invalid numeric input for add command.
   >>> menu
   Available commands: add, divide, menu, multiply, subtract
   >>> exit
   Exiting the interactive calculator...
   ```

---

## Plugin Architecture

- **PluginManager** (`plugin_manager.py`) scans the `app/commands` folder to discover classes that implement `CommandInterface`.
- Each command is a class with:
  - A `name` property  
  - An `execute(args: list[str]) -> str` method  
- **Adding a new command**:
  1. Create a new file in `app/commands/`, e.g. `mycool_command.py`.
  2. Implement `CommandInterface`:
     ```python
     from app.commands.command_interface import CommandInterface

     class MyCoolCommand(CommandInterface):
         @property
         def name(self) -> str:
             return "mycool"

         def execute(self, args: list[str]) -> str:
             # Your logic
             return "You ran mycool!"
     ```
  3. **Done!** The REPL will now recognize `mycool` automatically.

---

## Testing

1. Run all tests with:
   ```bash
   pytest
   ```
2. Check **coverage** with:
   ```bash
   pytest --cov=app --cov-report=term-missing
   ```

### Test Results

```

tests/test_app.py::test_app_unknown_then_valid_command PASSED                                 [  4%]
tests/test_app.py::test_command_interface_abstract_methods PASSED                             [  8%]
tests/test_app.py::test_app_divide_by_zero PASSED                                             [ 13%]
tests/test_app.py::test_app_value_error PASSED                                                [ 17%]
tests/test_app.py::test_app_unexpected_error PASSED                                           [ 21%]
tests/test_app.py::test_app_empty_input PASSED                                                [ 26%]
tests/test_app.py::test_app_start_exit_command PASSED                                         [ 30%]
tests/test_app.py::test_app_start_unknown_command PASSED                                      [ 34%]
tests/test_commands.py::test_add_command_success PASSED                                       [ 39%]
tests/test_commands.py::test_add_command_invalid_args_count PASSED                            [ 43%]
tests/test_commands.py::test_add_command_invalid_numeric PASSED                               [ 47%]
tests/test_commands.py::test_subtract_command_success PASSED                                  [ 52%]
tests/test_commands.py::test_subtract_command_invalid_args_count PASSED                       [ 56%]
tests/test_commands.py::test_subtract_command_invalid_numeric PASSED                          [ 60%]
tests/test_commands.py::test_multiply_command_success PASSED                                  [ 65%]
tests/test_commands.py::test_multiply_command_invalid_args_count PASSED                       [ 69%]
tests/test_commands.py::test_multiply_command_invalid_numeric PASSED                          [ 73%]
tests/test_commands.py::test_divide_command_success PASSED                                    [ 78%]
tests/test_commands.py::test_divide_command_invalid_args_count PASSED                         [ 82%]
tests/test_commands.py::test_divide_command_invalid_numeric PASSED                            [ 86%]
tests/test_commands.py::test_divide_command_zero_division PASSED                              [ 91%]
tests/test_commands.py::test_menu_command_success PASSED                                      [ 95%]
tests/test_commands.py::test_menu_command_with_args PASSED                                    [100%]

======================================== 23 passed in 0.06s ======================================



Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
app/__init__.py                         2      0   100%
app/app.py                             32      0   100%
app/commands/__init__.py                0      0   100%
app/commands/add_command.py            15      0   100%
app/commands/command_interface.py       9      0   100%
app/commands/divide_command.py         17      0   100%
app/commands/menu_command.py           12      0   100%
app/commands/multiply_command.py       15      0   100%
app/commands/plugin_manager.py         23      0   100%
app/commands/subtract_command.py       15      0   100%
-----------------------------------------------------------------
TOTAL                                 140      0   100%


======================================== 23 passed in 0.08s =========================================

```

---

## Contributing

1. **Fork** this repository.  
2. Create a **feature branch**.  
3. Add or update commands, fix bugs, or improve tests.  
4. **Ensure** tests and linter checks pass:
   ```bash
   pytest --cov=app --cov-report=term-missing
   pylint app tests
   ```
5. Submit a **pull request**.

### Code Style

- This project uses **pylint**.