import numpy as np

class NeutrinoParameters:
    def __init__(self, dm_squared, theta_12, g_fermi):
        self.dm_squared = dm_squared
        self.theta_12 = theta_12
        self.g_fermi = g_fermi

class PBHParameters:
    def __init__(self, mass_spectrum, density_profile, min_mass, max_mass):
        self.mass_spectrum = mass_spectrum
        self.density_profile = density_profile
        self.min_mass = min_mass
        self.max_mass = max_mass

class SimulationParameters:
    def __init__(self, energy_range, distance_range, num_points):
        self.energy_range = energy_range
        self.distance_range = distance_range
        self.num_points = num_points
        self.output_plot_dir = "plots/"
        self.output_data_dir = "data/"

def load_config(config_path):
    # This is a placeholder. In a real scenario, you would parse a YAML file.
    # For now, we'll use hardcoded values based on the config.yaml provided.
    
    neutrino_params = NeutrinoParameters(
        dm_squared=2.5e-3, # eV^2
        theta_12=0.58,     # radians (approx 33.82 degrees)
        g_fermi=1.1663787e-5 # GeV^-2
    )

    pbh_params = PBHParameters(
        mass_spectrum='power_law',
        density_profile='nfw',
        min_mass=1e15,
        max_mass=1e18
    )

    sim_params = SimulationParameters(
        energy_range=[1, 100], # GeV
        distance_range=[1, 1000], # km
        num_points=1000
    )

    return neutrino_params, pbh_params, sim_params
