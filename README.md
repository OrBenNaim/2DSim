
# Game of Life Simulation

## Description
This project simulates Conway's Game of Life, a cellular automaton devised by mathematician John Conway. The simulation follows the game rules where cells on a grid evolve based on their neighbors. The project uses Python with `pygame` for visualization.

## Features
- **Grid Visualization**: Displays a grid of cells that can be toggled between alive and dead.
- **Simulation Control**: Start, stop, and pause the simulation.
- **Random Patterns**: Generate random initial patterns.
- **File Loading**: Load predefined patterns from text files.
- **Interactive**: Click on cells to toggle their state.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/OrBenNaim/2DSim.git
    cd 2DSim
    ```

2. Install dependencies:
    ```bash
    pip install pygame numpy
    ```

## Usage

1. Run the simulation:
    ```bash
    python main.py
    ```

2. **Controls**:
    - `Space`: Pause/Resume simulation.
    - `Enter`: Start the simulation.
    - `R`: Generate a random pattern.
    - `C`: Clear the grid.
    - `L`: Load a predefined pattern from a file.
    - Left-click on cells to toggle their state.

## File Structure
- **main.py**: Entry point of the simulation, handles user input and events.
- **simulation.py**: Manages the game logic and updates the grid.
- **grid.py**: Defines the grid, cell toggling, and pattern handling.


