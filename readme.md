```markdown
# HW6: Production Readiness – DevOps, Environment Variables, and Logging

**Table of Contents**

1. [Overview](#overview)  
2. [Key Features](#key-features)  
3. [Project Structure](#project-structure)  
4. [Setup & Installation](#setup--installation)  
5. [Environment Variables](#environment-variables)  
6. [Logging Configuration](#logging-configuration)  
7. [Usage](#usage)  
8. [Testing & Coverage](#testing--coverage)  
9. [GitHub Actions (CI)](#github-actions-ci)  
10. [Adding New Commands](#adding-new-commands)  
11. [License](#license)

---

## Overview

This project **enhances** our previous calculator application (from HW5) by adding:

- **GitHub Actions** for automated testing (CI/CD fundamentals),
- **Environment Variables** (via a local `.env`),  
- **Logging** to record detailed application events and errors.

The calculator is an **interactive command-line** (REPL) tool that supports multiple operations (add, subtract, multiply, divide, etc.) via a **plugin-based command** architecture.

---

## Key Features

1. **Continuous Integration**  
   - GitHub Actions runs tests automatically on each push or pull request to the `main` branch.

2. **Environment Variables**  
   - A `.env` file (excluded from Git) is used to set configuration like `ENV_NAME`, `LOG_LEVEL`, etc.

3. **Advanced Logging**  
   - Logs events at different levels: `INFO`, `WARNING`, `ERROR`, and `EXCEPTION`.  
   - we can optionally provide a `logging.conf` file to customize logging handlers or formatters.

4. **Plugin Architecture**  
   - Command classes (e.g. `AddCommand`, `SubtractCommand`) are automatically discovered.  
   - Easily drop in new command files without modifying core REPL logic.

5. **High Test Coverage**  
   - Thorough test suite for each command and for the REPL loop.  
   - Typically near 100% coverage locally and on GitHub Actions.

---

## Project Structure

A sample directory layout:

```
homework6/
├── .github/
│   └── workflows/
│       └── python-app.yml         # GitHub Actions CI
├── app/
│   ├── __init__.py
│   ├── app.py                     # REPL logic, environment variable usage, logging calls
│   └── commands/
│       ├── __init__.py
│       ├── add_command.py
│       ├── subtract_command.py
│       ├── multiply_command.py
│       ├── divide_command.py
│       ├── menu_command.py
│       └── plugin_manager.py      # Discovers all commands
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_app.py                # Tests the REPL (integration)
│   └── test_commands.py           # Tests individual command plugins
├── .env               # Local environment variables (excluded by .gitignore)
├── logging.conf       # Optional custom logging config
├── .coveragerc
├── .gitignore
├── main.py            # Entry point, loads env vars, configures logging, calls App.start()
├── pytest.ini
├── readme.md          # This file
└── requirements.txt
```

---

## Setup & Installation

1. **Clone** or download this repository:
   ```bash
   git clone https://github.com/AbhishekDuddupudi/homework6
   cd homework6
   ```

2. **(Optional) Create and activate** a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   # or
   venv\Scripts\activate     # For Windows
   ```

3. **Install dependencies**:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Environment Variables

We use the `.env` file to configure environment-specific values without committing secrets. Make sure the `.gitignore` is like this:
```
.env
```
so that it does **not** get committed to source control.

**Example `.env`:**
```bash
ENV_NAME="local-development"
LOG_LEVEL="INFO"
```

When we run `main.py`, the application reads `.env` using [python-dotenv](https://pypi.org/project/python-dotenv/), setting environment variables such as:
- `ENV_NAME` (used to identify dev, staging, prod, etc.)
- `LOG_LEVEL` (sets default logging level, e.g. `DEBUG`, `INFO`, `WARNING`)

---

## Logging Configuration

1. The app checks for a file named `logging.conf`.
2. If `logging.conf` **exists**, we load advanced logging settings, possibly sending logs to console + file.
3. If no `logging.conf` is found, it falls back to `logging.basicConfig()` with a basic formatter.

**Typical Logging Levels**:
- **INFO**: Normal operations, e.g. “User typed `add 2 3`.”
- **WARNING**: Unknown or invalid command usage.
- **ERROR**: Recoverable issues like `ValueError` in a command.
- **EXCEPTION**: Unexpected errors (stack traces) for debugging.



---

## Usage

1. **Run the app**:
   ```bash
   python main.py
   ```
2. You should see:
   ```
   Welcome to the Interactive Calculator. Type 'exit' to exit.
   >>>
   ```
3. **Type commands** like:
   - `add 5 3` → prints `5.0 + 3.0 = 8.0`
   - `subtract 9 4` → prints `9.0 - 4.0 = 5.0`
   - `multiply 4 5` → prints `4.0 * 5.0 = 20.0`
   - `divide 20 4` → prints `20.0 / 4.0 = 5.0`
   - `menu` → lists available commands
   - `exit` → quits


---

## Testing & Coverage

### Running Tests Locally

- **All tests**:
  ```bash
  pytest
  ```
- **Tests with coverage**:
  ```bash
  pytest --cov=app --cov-report=term-missing
  ```
  You should see a summary like:
  ```
  ---------- coverage: platform ..., python ... ----------
  Name                                Stmts   Miss  Cover
  -------------------------------------------------------
  app/app.py                          ...     0     100%
  app/commands/add_command.py         ...     0     100%
  ...
  TOTAL                               ...     0     100%
  ```



## GitHub Actions (CI)

We use the `.github/workflows/python-app.yml` file to run tests automatically on each push or pull request to the `main` branch. Here’s the typical pipeline:

1. **Check out** code.  
2. **Set up Python** 3.10 (or your chosen version).  
3. **Install** dependencies from `requirements.txt`.  
4. **Run** `pytest --cov=app --cov-report=term-missing`.  
5. The **workflow passes** if tests pass, otherwise fails.

To view logs:
- Go to your repository on GitHub,
- Click the **Actions** tab,
- Select the latest run under “Python application”.


---

## License

This project is published under the [MIT License](https://opensource.org/licenses/MIT), which permits reuse and modifications for any purpose provided that original copyright notices and permissions are retained.


```