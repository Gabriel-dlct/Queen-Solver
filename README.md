# Queen Solver 🎮👑

A challenging puzzle game where players must strategically place queens on a chessboard following specific rules:
- One queen per column
- One queen per row
- One queen per color
- Queens cannot touch each other (not even diagonally)

## About this Project

This automated solver (v2.0) solves the Queens game **directly on your screen**, in about a second:

1. **Launch** – `button.py` opens a small window with a *"Lancer le solver"* button.
2. **Capture** – clicking it runs `main.py`, which takes a screenshot of your main monitor.
3. **Detect** – the board is located in the screenshot, its size (N×N) is detected, and the color of every cell is read.
4. **Solve** – cells are grouped into color regions and a backtracking algorithm finds the queen placement.
5. **Click** – the mouse automatically double-clicks each solution cell, so the puzzle is completed instantly.

The time spent on each step is printed in the terminal.

## Quick Setup ⚡

> **Requirements**: Linux with an **X11** session (clicks are sent through `python-xlib`, Wayland is not supported) and Python ≥ 3.13.

### Using `uv`

1. Create the virtual environment and install dependencies:
```bash
uv sync
```

2. Launch the solver window (from the project root):
```bash
uv run src/button.py
```

### Without `uv`

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Launch the solver window (from the project root):
```bash
python src/button.py
```

### Usage

1. Open the Queens puzzle on your **main monitor**, with the whole board visible.
2. Click **"Lancer le solver"**.
3. Don't touch the mouse: the queens are placed automatically.

## Project Structure

- `src/button.py`: Small Tkinter window with a button that launches the solver
- `src/main.py`: Full pipeline: screenshot → detection → solving → clicking
- `src/detector.py`: Finds the board in the screenshot, detects its size and reads cell colors (OpenCV)
- `src/solver/objects.py`: `Game` class: loads the board from colors, solves it by backtracking, can also generate random puzzles and display them
- `src/clicker.py`: Sends the mouse clicks on the solution cells (Xlib)
- `src/test.py`: Debug script: detects the board and displays it without clicking
