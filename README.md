# Treasure Labyrinth Game

A console-based text adventure game written in pure Python. Explore the ancient maze, solve riddles, avoid hidden traps, and find the legendary treasure.

## Project Overview

This project is a modular text quest developed to practice Python fundamentals, Git workflow, and package management with Poetry. The game features a functional programming approach (no classes), separating game logic, state management, and data.

### Key Features
* **Exploration:** Navigate through interconnected rooms like the Library, Armory, and Trap Room.
* **Inventory System:** Collect items (`take`) and use them (`use`) to interact with the environment.
* **Puzzles:** Solve logic riddles to unlock paths and chests.
* **Random Events:** A custom pseudo-random number generator triggers dynamic events (finding coins, getting scared, or triggering traps) based on player steps.
* **Clean Code:** The project follows PEP8 standards and is checked with the **Ruff** linter.

## Gameplay Demo

Watch the full walkthrough below:

[![asciicast](https://asciinema.org/a/AsTCSvQx1Bomz6Eg.svg)](https://asciinema.org/a/AsTCSvQx1Bomz6Eg)

## Installation & Setup

The project uses [Poetry](https://python-poetry.org/) for dependency management.

**Prerequisites:**
* Python 3.10+
* Poetry
* Make (optional, for running shortcuts)

**Installation:**

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    make install
    # or manually: poetry install
    ```

##How to Play

To start the game, run the following command in your terminal:

```bash
make project
# or manually: poetry run project