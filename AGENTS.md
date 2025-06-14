# Instructions for Codex Agents

This repository hosts a small Flet based chat client that talks to a KoboldCPP server.
All application code lives inside the `src/` directory. Backend modules contain
logic and data handling while UI components live under `frontend/`.

## Coding Conventions
- Use 4 spaces per indentation level.
- Keep imports alphabetically sorted within each section.
- Provide type hints and descriptive docstrings for new functions.
- Backend and frontend code should remain separated as in the current structure.

## Setup
- Python 3.11 or newer is required.
- Install dependencies with:
  ```bash
  pip install -e .[dev]
  ```
  The `[dev]` extra installs testing requirements.
- Run the application with `flet run` once dependencies are installed.

## Testing
- Tests are located in the `tests/` directory and use **pytest**.
- Execute the tests with:
  ```bash
  python -m pytest
  ```
- Tests must not read or write the real `settings.json` or `diary_entries.json`.
  Use `tmp_path` or other temporary locations when working with those files.
- All code changes should be covered by unit tests when feasible.

## Pull Requests
- Ensure the test suite passes before committing.
- Include concise commit messages and avoid large unrelated changes.

## Documentation
Offline Flet documentation resides in `docs/flet-docs`.
Place any Langchain-related docs under `docs/langchain-docs`.
Update the Flet docs whenever the `flet` dependency version changes.
