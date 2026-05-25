# Ayoayo
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-powered-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![pytest](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)

This project is a digital version of the traditional Nigerian board game Ayoayo, featuring a visual board and two-player online gameplay.

## Database
Completed games are stored in `game_results.db` with winner, scores, and timestamp. Use SQLite tools to view results.

## Running

1. Install the dependencies (e.g. `uv sync`)
2. Source the venv (`source .venv/bin/activate`)
3. Run the game using `python src/main.py`

## Testing

* Lint using `pylint src tests`
* Run tests using `pytest`
* Run tests with coverage: `pytest --cov=src --cov-report=term-missing tests/`

## Repository Structure
```
.
├── img
├── src
│   ├── bot
│   └── game_logic
└── tests
    ├── bot
    └── game_logic
```
