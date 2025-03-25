from src.simulation import Simulation

if __name__ == "__main__":

    simulation = Simulation()
    print("T_"+simulation.__class__.__name__+"_steps")
    # Run the game simulation
    simulation.run()
