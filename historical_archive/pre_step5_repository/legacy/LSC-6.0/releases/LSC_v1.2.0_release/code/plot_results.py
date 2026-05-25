import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    figures_dir = root / "figures"
    data_path = root / "code" / "simulation_output.json"

    with data_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    radius = np.array(data["radius_m"])
    v_lsc = np.array(data["v_lsc_ev"])
    resonance_right = np.array(data["resonance_right_ev2"])
    resonance_left = data["resonance_left_ev2"]
    rs = data["parameters"]["schwarzschild_radius_m"]

    x = radius / rs

    plt.figure(figsize=(7.0, 4.8))
    plt.loglog(x, v_lsc, color="#1f5f8b", linewidth=2.2)
    plt.xlabel(r"$r/r_s$")
    plt.ylabel(r"$V_{\rm LSC}$ [eV]")
    plt.title("Effective LSC potential vs radius")
    plt.grid(True, which="both", alpha=0.25)
    plt.tight_layout()
    plt.savefig(figures_dir / "lsc_potential.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.0, 4.8))
    plt.loglog(x, resonance_right, color="#9b3d2e", linewidth=2.2, label=r"$2E(V_{\rm matter}+V_{\rm LSC})$")
    plt.axhline(resonance_left, color="#222222", linestyle="--", linewidth=1.8, label=r"$\Delta m^2\cos(2\theta)$")
    plt.xlabel(r"$r/r_s$")
    plt.ylabel(r"resonance scale [eV$^2$]")
    plt.title("Resonance-condition diagnostic")
    plt.grid(True, which="both", alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "resonance_plot.png", dpi=180)
    plt.close()


if __name__ == "__main__":
    main()
