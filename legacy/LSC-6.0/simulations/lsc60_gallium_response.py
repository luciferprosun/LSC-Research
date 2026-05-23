#!/usr/bin/env python3
"""Toy LSC 6.0 Gallium-response simulation.

This script is deliberately simple. It does not claim to fit BEST data.
It visualizes how a small propagation term plus an anisotropic detector term
can map into an event-rate deficit under an effective amplification factor.

It uses only the Python standard library so that the repository can run on a
fresh machine without installing scientific packages.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


TARGET_R_BEST = 0.79


def detector_anisotropy(theta: float, amplitude: float) -> float:
    """Quadrupole-like angular detector response with zero-ish sky average."""
    return amplitude * 0.5 * (3.0 * math.cos(theta) ** 2 - 1.0)


def event_ratio(delta_g: float, delta_detector: float, amplification: float) -> float:
    """Linearized event-rate response."""
    delta_e_over_e = delta_g + delta_detector
    return 1.0 - amplification * delta_e_over_e


def svg_polyline(points: list[tuple[float, float]], color: str) -> str:
    encoded = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{encoded}" fill="none" stroke="{color}" stroke-width="3"/>'


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    theta_values = [math.radians(deg) for deg in range(0, 181)]
    amplification = 3.5

    scenarios = [
        ("detector 3%, propagation 3%", 0.03, 0.03),
        ("detector 4%, propagation 2.5%", 0.025, 0.04),
        ("detector 6%, propagation 1.5%", 0.015, 0.06),
    ]

    rows: list[dict[str, str]] = []
    series: list[tuple[str, str, list[tuple[float, float]]]] = []
    colors = ["#00aaff", "#ff2bd6", "#00aa66"]

    y_min = 0.65
    y_max = 1.10
    width = 920
    height = 560
    left = 70
    right = 30
    top = 35
    bottom = 65
    plot_w = width - left - right
    plot_h = height - top - bottom

    def map_x(degrees: float) -> float:
        return left + plot_w * degrees / 180.0

    def map_y(ratio: float) -> float:
        return top + plot_h * (y_max - ratio) / (y_max - y_min)

    for color, (label, delta_g, amp_d) in zip(colors, scenarios):
        points = []
        for theta in theta_values:
            degrees = math.degrees(theta)
            delta_d = detector_anisotropy(theta, amp_d)
            ratio = event_ratio(delta_g, delta_d, amplification)
            rows.append(
                {
                    "scenario": label,
                    "theta_degrees": f"{degrees:.1f}",
                    "delta_g": f"{delta_g:.5f}",
                    "detector_amplitude": f"{amp_d:.5f}",
                    "delta_detector": f"{delta_d:.5f}",
                    "rate_ratio": f"{ratio:.5f}",
                }
            )
            points.append((map_x(degrees), map_y(ratio)))
        series.append((label, color, points))

    csv_path = out_dir / "lsc60_gallium_response.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    target_y = map_y(TARGET_R_BEST)
    axis = [
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#333" stroke-width="1"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#333" stroke-width="1"/>',
        f'<line x1="{left}" y1="{target_y:.2f}" x2="{left + plot_w}" y2="{target_y:.2f}" stroke="#111" stroke-width="1.5" stroke-dasharray="7 5"/>',
    ]

    polylines = [svg_polyline(points, color) for _, color, points in series]
    legend_items = []
    for idx, (label, color, _) in enumerate(series):
        y = 70 + idx * 24
        legend_items.append(f'<rect x="625" y="{y - 10}" width="18" height="4" fill="{color}"/>')
        legend_items.append(f'<text x="650" y="{y}" font-size="14" fill="#111">{label}</text>')
    legend_items.append('<line x1="625" y1="142" x2="643" y2="142" stroke="#111" stroke-width="1.5" stroke-dasharray="7 5"/>')
    legend_items.append('<text x="650" y="146" font-size="14" fill="#111">BEST-scale R ~ 0.79</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{width / 2}" y="24" text-anchor="middle" font-size="20" font-family="Arial, sans-serif">LSC 6.0 toy propagation + anisotropic detector response</text>
  {''.join(axis)}
  {''.join(polylines)}
  {''.join(legend_items)}
  <text x="{width / 2}" y="{height - 18}" text-anchor="middle" font-size="15" font-family="Arial, sans-serif">Arrival / detector angle theta [degrees]</text>
  <text x="20" y="{height / 2}" transform="rotate(-90 20 {height / 2})" text-anchor="middle" font-size="15" font-family="Arial, sans-serif">Toy observed rate ratio R</text>
  <text x="{left - 10}" y="{map_y(1.0):.2f}" text-anchor="end" font-size="12">1.00</text>
  <text x="{left - 10}" y="{map_y(0.79):.2f}" text-anchor="end" font-size="12">0.79</text>
  <text x="{left - 10}" y="{map_y(0.70):.2f}" text-anchor="end" font-size="12">0.70</text>
</svg>
'''

    svg_path = out_dir / "lsc60_gallium_response.svg"
    svg_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {csv_path}")
    print(f"Wrote {svg_path}")


if __name__ == "__main__":
    main()
