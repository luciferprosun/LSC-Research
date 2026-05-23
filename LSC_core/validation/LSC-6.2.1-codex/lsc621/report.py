from __future__ import annotations

from textwrap import dedent

from .model import AnalysisResult


def tex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = text
    for key, value in replacements.items():
        out = out.replace(key, value)
    return out


def format_float(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def render_markdown(result: AnalysisResult) -> str:
    lines: list[str] = []
    lines.append("# LSC 6.2.1 Codex Analysis")
    lines.append("")
    lines.append("Working continuation on the gallium source data package.")
    lines.append("")
    lines.append("## Selected Fit")
    lines.append("")
    lines.append("| coefficient | value |")
    lines.append("| --- | ---: |")
    for name, value in zip(result.coefficient_names, result.coefficients, strict=True):
        lines.append(f"| {name} | {value:.8f} |")
    lines.append(f"| condition number | {result.condition_number:.3f} |")
    lines.append("")
    lines.append("## Anchor Predictions")
    lines.append("")
    lines.append("| name | observed R | predicted R | residual |")
    lines.append("| --- | ---: | ---: | ---: |")
    for row in result.anchor_rows:
        lines.append(
            f"| {row.name} | {row.observed_r:.6f} | {row.predicted_r:.6f} | {row.residual:+.6f} |"
        )
    lines.append("")
    lines.append("## Validation Predictions")
    lines.append("")
    lines.append("| name | observed R | predicted R | residual |")
    lines.append("| --- | ---: | ---: | ---: |")
    for row in result.validation_rows:
        lines.append(
            f"| {row.name} | {row.observed_r:.6f} | {row.predicted_r:.6f} | {row.residual:+.6f} |"
        )
    lines.append("")
    lines.append("## Leave-One-Out")
    lines.append("")
    lines.append("| omitted | predicted R | observed R | residual |")
    lines.append("| --- | ---: | ---: | ---: |")
    for row in result.loo_rows:
        lines.append(
            f"| {row.name} | {row.predicted_r:.6f} | {row.observed_r:.6f} | {row.residual:+.6f} |"
        )
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append(
        f"- mean source cross section, 51Cr: {result.source_mean_51cr_cm2:.6e} cm^2"
    )
    lines.append(
        f"- mean source cross section, 37Ar: {result.source_mean_37ar_cm2:.6e} cm^2"
    )
    lines.append("- the anchor fit is exact by construction, so leave-one-out is the real stability check")
    lines.append("- GALLEX source-by-source split remains a useful nuisance test")
    return "\n".join(lines) + "\n"


def render_tex(result: AnalysisResult) -> str:
    coeff_lines = []
    for name, value in zip(result.coefficient_names, result.coefficients, strict=True):
        coeff_lines.append(f"{tex_escape(name)} & {value:.8f} \\\\")
    anchor_lines = []
    for row in result.anchor_rows:
        anchor_lines.append(
            f"{tex_escape(row.name)} & {row.observed_r:.6f} & {row.predicted_r:.6f} & {row.residual:+.6f} \\\\"
        )
    validation_lines = []
    for row in result.validation_rows:
        validation_lines.append(
            f"{tex_escape(row.name)} & {row.observed_r:.6f} & {row.predicted_r:.6f} & {row.residual:+.6f} \\\\"
        )
    loo_lines = []
    for row in result.loo_rows:
        loo_lines.append(
            f"{tex_escape(row.name)} & {row.observed_r:.6f} & {row.predicted_r:.6f} & {row.residual:+.6f} \\\\"
        )

    return dedent(
        rf"""
        \documentclass[11pt]{{article}}
        \usepackage[margin=1in]{{geometry}}
        \usepackage{{booktabs}}
        \usepackage{{longtable}}
        \usepackage{{array}}
        \usepackage{{amsmath,amssymb}}
        \usepackage[hidelinks]{{hyperref}}
        \usepackage{{microtype}}
        \setlength{{\parskip}}{{0.6em}}
        \setlength{{\parindent}}{{0pt}}

        \begin{{document}}
        \title{{LSC 6.2.1 Codex Analysis}}
        \author{{Open working package}}
        \date{{\today}}
        \maketitle

        \section*{{Scope}}
        This report is an exploratory fit to the BEST, GALLEX and SAGE gallium source data.
        It is not a claim of confirmed new physics. The aim is to test whether a compact
        phenomenological ansatz can reproduce the main source-calibration ratios while
        keeping the calibration trail readable.

        \section*{{Data Anchors}}
        The anchor set uses five independent constraints:
        BEST inner, BEST outer, GALLEX combined reanalysis, SAGE $^{51}$Cr and SAGE $^{37}$Ar.
        BEST ratio and the GALLEX Cr1/Cr2 split are kept as diagnostics.

        \section*{{Model}}
        The fit is performed in linearized form:
        \[
        -\ln R = \beta_L L^{-1}_{{\mathrm eff}} + \beta_S A_{{\mathrm shape}} +
        \beta_\sigma \, \sigma_{{\mathrm norm}} + \beta_Z Z_{{\mathrm BEST}} + \beta_0.
        \]
        Here $L_{{\mathrm eff}}$ is a geometry proxy, $A_{{\mathrm shape}}$ is a second-moment
        anisotropy proxy, $\sigma_{{\mathrm norm}}$ is the mean source-line cross section in
        units of $10^{{-45}}\mathrm{{cm}}^2$, and $Z_{{\mathrm BEST}}$ splits the BEST inner and
        outer zones.

        \subsection*{{Geometry Proxy}}
        For this first-pass package:
        \[
        L_{{\mathrm eff}} =
        \begin{{cases}}
        4R/3 & \text{{sphere}} \\
        (R + H/2)/2 & \text{{cylindrical or tank geometry}}
        \end{{cases}}
        \]
        \[
        A_{{\mathrm shape}} = \frac{{\left| \langle z^2 \rangle - \langle x^2 \rangle \right|}}
        {{\langle z^2 \rangle + 2 \langle x^2 \rangle}},
        \quad
        \langle x^2 \rangle = R^2/4,\quad \langle z^2 \rangle = H^2/12.
        \]

        \section*{{Fitted Coefficients}}
        \begin{{tabular}}{{lr}}
        \toprule
        coefficient & value \\
        \midrule
        {''.join(coeff_lines)}
        \bottomrule
        \end{{tabular}}

        \section*{{Anchor Predictions}}
        \begin{{longtable}}{{lrrr}}
        \toprule
        case & observed & predicted & residual \\
        \midrule
        \endfirsthead
        \toprule
        case & observed & predicted & residual \\
        \midrule
        \endhead
        {''.join(anchor_lines)}
        \bottomrule
        \end{{longtable}}

        \section*{{Validation Predictions}}
        \begin{{longtable}}{{lrrr}}
        \toprule
        case & observed & predicted & residual \\
        \midrule
        \endfirsthead
        \toprule
        case & observed & predicted & residual \\
        \midrule
        \endhead
        {''.join(validation_lines)}
        \bottomrule
        \end{{longtable}}

        \section*{{Leave-One-Out Stability}}
        \begin{{longtable}}{{lrrr}}
        \toprule
        omitted case & observed & predicted & residual \\
        \midrule
        \endfirsthead
        \toprule
        omitted case & observed & predicted & residual \\
        \midrule
        \endhead
        {''.join(loo_lines)}
        \bottomrule
        \end{{longtable}}

        \section*{{Interpretation}}
        The exact anchor fit means the main question is not whether the algebra can absorb the
        anchors. It is whether the same coefficients survive perturbation. The leave-one-out run
        shows that the package is still sensitive to the selected anchor set, especially around
        GALLEX. That is useful: it tells us where the next 6.2.1 iteration needs extra nuisance
        structure or additional event-level data.

        \section*{{Source Notes}}
        \begin{{itemize}}
        \item BEST: \href{{https://doi.org/10.1103/PhysRevLett.128.232501}}{{Phys. Rev. Lett. 128, 232501 (2022)}}
        \item GALLEX final and reanalysis: \href{{https://doi.org/10.1016/S0370-2693(97)01562-1}}{{Phys. Lett. B 420, 114-126 (1998)}} and \href{{https://doi.org/10.1016/j.physletb.2010.01.030}}{{Phys. Lett. B 685, 47-54 (2010)}}
        \item SAGE Cr-51: \href{{https://doi.org/10.1103/PhysRevC.59.2246}}{{Phys. Rev. C 59, 2246 (1999)}}
        \item SAGE Ar-37: \href{{https://doi.org/10.1103/PhysRevC.73.045805}}{{Phys. Rev. C 73, 045805 (2006)}}
        \item Gallium source cross sections: \href{{https://doi.org/10.1103/PhysRevC.56.3391}}{{Phys. Rev. C 56, 3391 (1997)}}
        \end{{itemize}}

        \end{{document}}
        """
    ).lstrip()
