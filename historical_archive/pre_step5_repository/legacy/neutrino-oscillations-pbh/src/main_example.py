import numpy as np
from params import load_config
from lscc4_neutrino import NeutrinoOscillationSolver
from analysis import Analysis
import os

def main():
    # Load configuration
    neutrino_params, pbh_params, sim_params = load_config("config.yaml")

    # Create output directories if they don't exist
    os.makedirs(sim_params.output_plot_dir, exist_ok=True)
    os.makedirs(sim_params.output_data_dir, exist_ok=True)

    # Initialize solver and analysis
    solver = NeutrinoOscillationSolver(neutrino_params, pbh_params)
    analysis = Analysis(solver)

    # Define initial state (e.g., pure electron neutrino)
    initial_state = np.array([1+0j, 0+0j]) # For 2-flavor, electron neutrino

    # Run analysis for a specific energy
    energy_to_analyze = 10 # GeV
    analysis.run_analysis(initial_state, energy_to_analyze, sim_params.distance_range, sim_params.output_plot_dir)

    print("Main example execution complete.")

if __name__ == "__main__":
    main()
