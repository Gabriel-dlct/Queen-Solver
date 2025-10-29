# Queen Solver 🎮👑

A challenging puzzle game where players must strategically place queens on a chessboard following specific rules:
- One queen per column
- One queen per row 
- One queen per color
- Queens cannot attack each other

## About this Project

This automated solver (v1.0) can:
- Generate random queen puzzle configurations
- Automatically solve the puzzle by calculating correct queen placements
- Execute the solution by simulating clicks on the game board
- Output two visualizations using Matplotlib:
    - The first visualization shows the generated board configuration.
    - The second visualization displays the board with the solution.
    ## Quick Setup ⚡

    This project supports both `uv` package manager and manual setup for dependency management.

    ### Using `uv`

    1. Create and activate the virtual environment:
    ```bash
    uv init
    uv sync
    ```

    2. Run the solver:
    ```bash
    uv run main.py <size>
    ```

    > **Note**: The board size parameter must be:
    > - Minimum: 4 (smaller boards have no valid solutions)
    > - Recommended maximum: 20 (larger sizes may require significant computation time)

    ### Without `uv`

    If you prefer not to use the `uv` package manager, you can set up the project manually:

    1. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

    2. Run the solver:
    ```bash
    python main.py <size>
    ```

    > **Note**: The board size parameter must be:
    > - Minimum: 4 (smaller boards have no valid solutions)
    > - Recommended maximum: 20 (larger sizes may require significant computation time)

## Project Structure

- `main.py`: Execute the script
- `objects.py`: Create the classes to create and solve the game
- `visualizations.py`: Generate and display the visualizations of the board configurations and solutions


## Future of the Project

The objective is to develop a script that can directly solve the queen puzzle and automatically click on the correct squares to complete it instantly. The next steps involve creating a detection script, a transformation script to integrate with the current solver, and a final script to perform the clicks in the appropriate locations.
