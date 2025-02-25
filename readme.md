# Interactive Command-Line Calculator with Plugin Architecture

This project demonstrates a **plugin-based** command pattern architecture in Python, featuring a REPL (Read-Eval-Print Loop), robust error handling, and **100% test coverage** with `pytest`.

---

## 📌 Table of Contents

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

## 🔍 Overview

This calculator runs continuously in a **REPL**, enabling you to type commands such as `add`, `subtract`, `multiply`, `divide`, and `menu`. Each command is implemented as a **plugin** in the `app/commands/` folder. New commands can be easily added by dropping in a new file that implements the **command interface**.

### 🎯 Goals

- Provide a **clean plugin architecture** (via Python’s `pkgutil` and reflection).  
- Handle **errors** gracefully: invalid arguments, invalid numeric input, division by zero, unknown commands, etc.  
- Achieve **100% coverage** for all code, including REPL logic and plugin commands.  

---

## ⭐ Key Features

### 🔹 **Continuous REPL**
- Type commands at the `>>>` prompt.  
- Type `exit` to quit.

### 🔹 **Basic Arithmetic Commands**
- `add <x> <y>` → Outputs `x + y = result`
- `subtract <x> <y>` → Outputs `x - y = result`
- `multiply <x> <y>` → Outputs `x * y = result`
- `divide <x> <y>` → Outputs `x / y = result`
- Zero-division triggers a specific error message.

### 🔹 **Menu Command**
- `menu` → Lists all available commands dynamically discovered via the **PluginManager**.

### 🔹 **Plugin Architecture**
- Each command is a self-contained `.py` file in `app/commands/`.
- **PluginManager** automatically discovers and registers them, no need to modify the main application.

### 🔹 **Robust Error Handling**
- **Usage errors** (wrong number of arguments) → `ValueError`
- **Invalid numeric input** → `ValueError`
- **Divide by zero** → `ZeroDivisionError`
- **Unknown command** → `Unknown command. Type 'menu' to see available commands, or 'exit' to quit.`
- **Unexpected errors** → Caught and printed to `stderr`.

### 🔹 **100% Test Coverage**
- **Unit tests** for each command.
- **Integration tests** for the REPL (via `monkeypatch`).
- Coverage measured by `pytest-cov`.

---

## 📂 Project Structure

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

## ⚙️ Installation

1. **Clone** the repository:
   ```bash
   git clone <repository_url>
   cd calc_design_patterns
   ```

2. **Create & activate** a virtual environment:
   ```bash
   python -m venv homework5
   source homework5/bin/activate  # Mac/Linux
   homework5\Scripts\activate    # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

1. **Run** the calculator:
   ```bash
   python main.py
   ```
2. **Sample Session**:
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

## 🔌 Plugin Architecture

- **PluginManager** (`plugin_manager.py`) scans the `app/commands` folder to discover classes that implement `CommandInterface`.
- **Adding a new command**:
  ```python
  from app.commands.command_interface import CommandInterface

  class MyCoolCommand(CommandInterface):
      @property
      def name(self) -> str:
          return "mycool"

      def execute(self, args: list[str]) -> str:
          return "You ran mycool!"
  ```
  - **Done!** The REPL will now recognize `mycool` automatically.

---

## ✅ Testing

1. **Run all tests**:
   ```bash
   pytest
   ```
2. **Check coverage**:
   ```bash
   pytest --cov=app --cov-report=term-missing
   ```
3. **Expected Output**:
   ```
   Name                                Stmts   Miss  Cover
   -------------------------------------------------------
   app/app.py                           32      0   100%
   app/commands/add_command.py          15      0   100%
   app/commands/multiply_command.py     15      0   100%
   app/commands/plugin_manager.py       23      0   100%
   -------------------------------------------------------
   TOTAL                               140      0   100%
   ```

---

## 🤝 Contributing

1. **Fork** this repository.  
2. Create a **feature branch**.  
3. Add or update commands, fix bugs, or improve tests.  
4. Ensure tests and linter checks pass:
   ```bash
   pytest --cov=app --cov-report=term-missing
   pylint app tests
   ```
5. Submit a **pull request**.

---
