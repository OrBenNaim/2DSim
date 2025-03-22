from src.simulation import Simulation


if __name__ == "__main__":
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    CELL_SIZE = 6

    simulation = Simulation(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)

    # Run the game simulation
    simulation.run()
