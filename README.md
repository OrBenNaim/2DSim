# Game of Life Simulation

## Description
- This project simulates Conway's Game of Life, a cellular automaton devised by mathematician John Conway. The simulation follows the game rules where cells on a grid evolve based on their neighbors. The project uses Python with pygame for visualization.

**Details*:* 
1. A branch called “Sprint-5,” extending the previous branch.
2. Implement data collection within the simulation to track relevant statistics—implement these as alerts.
3. Generate a line plot depicting the number of live organisms of each type over time during the simulation.
4. Generate a line plot depicting the number of Herbivore reproductions throughout the simulation.
5. Implement a timeline summarizing interesting “events” (like reproductions, animal consumption, or any other appropriate events).
6. Use appropriate visualization libraries (e.g., Matplotlib) to generate the plots.
7. Ensure the statistics and plots are generated after the simulation run and are saved to files.


## Features
- **Grid Visualization**: Displays a grid of cells that can be toggled between alive and dead.
- **Simulation Control**: Start, stop, and pause the simulation.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/OrBenNaim/2DSim.git
    cd 2DSim
    ```
2. Install dependencies:
    ```bash
        pip install numpy
    ```
   ```bash
        pip install pygame
   ```
   ```bash
        pip install pandas 
   ```
   ```bash
        pip install matplotlib
   ```

## Usage
1. Run the simulation:
    ```bash
        python main.py
    ```

2. **Controls**:
   - Space: Pause/Resume simulation.
   - Enter: Start the simulation.
   - Esc: Stop the simulation. The program will immediately generate all graphs after pressing 'Esc' key.

## Assignment Description
   **Link**: 
   - [Assignment Description](https://docs.google.com/document/d/1Vb_wEcch_1Ntv1C488CBxmVf1OdBdoUKBJg3sgdhtcU/edit?tab=t.0#heading=h.sa3348ax0681)