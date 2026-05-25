from __future__ import annotations

import csv
import json
import shutil
import subprocess
from pathlib import Path

from lsc621.data import DATASET_PATH, build_observations, load_dataset
from lsc621.model import run_analysis
from lsc621.report import render_markdown, render_tex


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "out"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def compile_pdf(tex_path: Path) -> None:
    pdflatex = shutil.which("pdflatex")
    if pdflatex is None:
        raise RuntimeError("pdflatex is not available in this environment")
    for _ in range(2):
        subprocess.run(
            [
                pdflatex,
                "-interaction=nonstopmode",
                "-halt-on-error",
                tex_path.name,
            ],
            cwd=tex_path.parent,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset(DATASET_PATH)
    observations = build_observations(dataset)
    result = run_analysis(observations)

    (OUT_DIR / "analysis.json").write_text(
        json.dumps(result.to_json(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    write_csv(
        OUT_DIR / "observations.csv",
        [
            {
                "name": obs.name,
                "experiment": obs.experiment,
                "source": obs.source,
                "observed_r": f"{obs.observed_r:.6f}",
                "feature_length_inv": f"{obs.feature[0]:.8f}",
                "feature_shape": f"{obs.feature[1]:.8f}",
                "feature_source_norm": f"{obs.feature[2]:.8f}",
                "feature_zone_split": f"{obs.feature[3]:.8f}",
                "anchor": str(obs.anchor),
                "citation": obs.citation,
                "notes": obs.notes,
            }
            for obs in observations
        ],
    )

    write_csv(
        OUT_DIR / "predictions.csv",
        [
            {
                "name": row.name,
                "kind": row.kind,
                "observed_r": f"{row.observed_r:.6f}",
                "predicted_r": f"{row.predicted_r:.6f}",
                "residual": f"{row.residual:+.6f}",
                "pull": "" if row.pull is None else f"{row.pull:+.6f}",
            }
            for row in result.anchor_rows + result.validation_rows
        ],
    )

    write_csv(
        OUT_DIR / "loo.csv",
        [
            {
                "omitted": row.name,
                "observed_r": f"{row.observed_r:.6f}",
                "predicted_r": f"{row.predicted_r:.6f}",
                "residual": f"{row.residual:+.6f}",
                "pull": "" if row.pull is None else f"{row.pull:+.6f}",
            }
            for row in result.loo_rows
        ],
    )

    markdown = render_markdown(result)
    (OUT_DIR / "report.md").write_text(markdown, encoding="utf-8")

    tex = render_tex(result)
    tex_path = OUT_DIR / "lsc_6_2_1_codex_report.tex"
    tex_path.write_text(tex, encoding="utf-8")
    compile_pdf(tex_path)

    print(f"wrote {OUT_DIR / 'analysis.json'}")
    print(f"wrote {OUT_DIR / 'report.md'}")
    print(f"wrote {tex_path}")
    print(f"wrote {tex_path.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()

