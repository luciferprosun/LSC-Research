import json
from pathlib import Path

import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "code"

    # SI constants
    G = 6.67430e-11
    c = 299_792_458.0
    m_sun = 1.98847e30

    # Model and oscillation parameters
    alpha_lsc = 1.0e-3
    source_mass = 10.0 * m_sun
    energy_ev = 1.0e15
    energy_pev = energy_ev / 1.0e15
    e_scale_ev = 1.0
    delta_m2_ev2 = 2.5e-3
    theta = np.deg2rad(33.0)
    v_matter_ev = 1.0e-13

    schwarzschild_radius = 2.0 * G * source_mass / c**2
    radius = np.geomspace(3.0 * schwarzschild_radius, 1.0e4 * schwarzschild_radius, 600)

    compactness = G * source_mass / (radius * c**2)
    v_lsc_ev = alpha_lsc * compactness * energy_pev * e_scale_ev
    resonance_left_ev2 = delta_m2_ev2 * np.cos(2.0 * theta)
    resonance_right_ev2 = 2.0 * energy_ev * (v_matter_ev + v_lsc_ev)

    output = {
        "parameters": {
            "alpha_lsc": alpha_lsc,
            "source_mass_solar": 10.0,
            "energy_ev": energy_ev,
            "energy_pev": energy_pev,
            "e_scale_ev": e_scale_ev,
            "delta_m2_ev2": delta_m2_ev2,
            "theta_deg": 33.0,
            "v_matter_ev": v_matter_ev,
            "schwarzschild_radius_m": schwarzschild_radius,
        },
        "radius_m": radius.tolist(),
        "v_lsc_ev": v_lsc_ev.tolist(),
        "resonance_left_ev2": float(resonance_left_ev2),
        "resonance_right_ev2": resonance_right_ev2.tolist(),
    }

    with (data_dir / "simulation_output.json").open("w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)


if __name__ == "__main__":
    main()
