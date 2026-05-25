import numpy as np
import matplotlib.pyplot as plt

class Analysis:
    def __init__(self, solver):
        self.solver = solver

    def calculate_oscillation_probability(self, solution, flavor_index=0):
        # Assuming solution is a 2-component vector for 2-flavor oscillations
        # Probability of remaining in the initial flavor (e.g., electron neutrino)
        return np.abs(solution[:, flavor_index])**2

    def plot_probability(self, r_points, probabilities, energy, output_dir="."):
        plt.figure(figsize=(10, 6))
        plt.plot(r_points, probabilities)
        plt.xlabel("Distance (km)")
        plt.ylabel("Survival Probability")
        plt.title(f"Neutrino Survival Probability at E = {energy} GeV")
        plt.grid(True)
        plt.savefig(f"{output_dir}/survival_probability_E{energy}.png")
        plt.close()

    def run_analysis(self, initial_state, energy, distance_range, output_dir="."):
        r_points, solution = self.solver.solve_evolution(initial_state, energy, distance_range)
        probabilities = self.calculate_oscillation_probability(solution)
        self.plot_probability(r_points, probabilities, energy, output_dir)
        print(f"Analysis complete for E={energy} GeV. Plot saved to {output_dir}/survival_probability_E{energy}.png")
