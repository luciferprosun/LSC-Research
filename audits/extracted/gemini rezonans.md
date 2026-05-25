\[5/25/26 9:18 AM\] Lukaszzz: \<!DOCTYPE html\>

\<html lang=\"en\"\>

\<head\>

\<meta charset=\"UTF-8\"\>

\<title\>LSC Public Data & Constraint Reconnaissance\</title\>

\<style\>

\@page {

size: A4;

margin: 20mm 15mm 25mm 15mm;

\@top-right {

content: \"LSC Reconnaissance Report\";

font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif;

font-size: 8pt;

color: #64748b;

}

\@bottom-left {

content: \"CONFIDENTIAL // PRE-BEST-2 SCIENTIFIC EVALUATION\";

font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif;

font-size: 8pt;

color: #64748b;

}

\@bottom-right {

content: \"Page \" counter(page) \" of \" counter(pages);

font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif;

font-size: 8pt;

color: #64748b;

}

}

body {

font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif;

color: #1e293b;

line-height: 1.5;

font-size: 10pt;

margin: 0;

padding: 0;

background-color: #ffffff;

}

.header-banner {

background-color: #0f172a;

color: #ffffff;

padding: 6mm;

margin-bottom: 6mm;

border-radius: 4px;

}

h1 {

font-size: 18pt;

margin: 0 0 2mm 0;

text-transform: uppercase;

letter-spacing: 0.5px;

}

.subtitle {

font-size: 11pt;

color: #94a3b8;

margin: 0;

font-style: italic;

}

h2 {

font-size: 13pt;

color: #0f172a;

margin-top: 6mm;

margin-bottom: 3mm;

border-left: 4px solid #3b82f6;

padding-left: 3mm;

page-break-after: avoid;

}

h3 {

font-size: 11pt;

color: #1e293b;

margin-top: 4mm;

margin-bottom: 2mm;

page-break-after: avoid;

}

p {

margin-top: 0;

margin-bottom: 3mm;

text-align: justify;

}

table {

width: 100%;

border-collapse: collapse;

margin-top: 3mm;

margin-bottom: 5mm;

page-break-inside: auto;

}

tr {

page-break-inside: avoid;

page-break-after: auto;

}

th {

background-color: #0f172a;

color: #ffffff;

font-weight: bold;

text-align: left;

padding: 2mm;

font-size: 9pt;

border: 1px solid #0f172a;

}

td {

padding: 2mm;

font-size: 8.5pt;

border: 1px solid #e2e8f0;

vertical-align: top;

}

tr:nth-child(even) td {

background-color: #f8fafc;

}

ul, ol {

margin-top: 0;

margin-bottom: 3mm;

padding-left: 5mm;

}

li {

margin-bottom: 1mm;

text-align: justify;

}

.page-break {

page-break-before: always;

}

.highlight-box {

background-color: #eff6ff;

border-left: 4px solid #2563eb;

padding: 3mm;

margin-bottom: 4mm;

font-size: 9.5pt;

page-break-inside: avoid;

}

.alert-box {

background-color: #fef2f2;

border-left: 4px solid #dc2626;

padding: 3mm;

margin-bottom: 4mm;

font-size: 9.5pt;

page-break-inside: avoid;

}

\</style\>

\</head\>

\<body\>

\<div class=\"header-banner\"\>

\<h1\>LSC Public Data & Constraint Reconnaissance\</h1\>

\<div class=\"subtitle\"\>Final Pre-BEST-2 Freeze Readiness
Assessment\</div\>

\</div\>

\[5/25/26 9:18 AM\] Lukaszzz: \<h2\>Executive Summary\</h2\>

\<p\>

This report constitutes a final, unprotective, and rigorous data
reconnaissance for the LSC (Liquid Scintillator Core) framework prior to
the BEST-2 experimental phase. Operating under the strict assumption
that LSC is an unvalidated phenomenological framework, this audit maps
all publicly available datasets, evaluates their sufficiency for
likelihood-level analysis, identifies critical missing metadata, and
maps external physics constraints (solar, KATRIN, IceCube).

\</p\>

\<p\>

The central finding is that while the public domain offers sufficient
data to establish the absolute deficit scale (trace), the framework
remains fundamentally underconstrained regarding its directional and
time-dependent parameters (traceless tensor components) due to the
proprietary nature of extraction-level covariance and sidereal
timestamps.

\</p\>

\<h2\>A. Map of Publicly Available Datasets and Resources\</h2\>

\<table\>

\<thead\>

\<tr\>

\<th style=\"width: 15%;\"\>Resource\</th\>

\<th style=\"width: 25%;\"\>Source / Link\</th\>

\<th style=\"width: 35%;\"\>Contents & Machine Readability\</th\>

\<th style=\"width: 15%;\"\>Sufficient?\</th\>

\<th style=\"width: 10%;\"\>Class\</th\>

\</tr\>

\</thead\>

\<tbody\>

\<tr\>

\<td\>\<b\>BEST (2022)\</b\>\</td\>

\<td\>PRL 128, 232501 (2022)\<br\>arXiv:2112.14599\</td\>

\<td\>Inner/Outer zone rates (20
extractions).\<br\>\<i\>Machine-readable:\</i\> No (PDF tables).\</td\>

\<td\>\<b\>No.\</b\> Lacks full covariance matrix.\</td\>

\<td\>\<b\>ESSENTIAL\</b\>\</td\>

\</tr\>

\<tr\>

\<td\>\<b\>GALLEX\</b\>\</td\>

\<td\>PRD 80, 082001 (2009)\</td\>

\<td\>Historical Cr-51 source calibration
rates.\<br\>\<i\>Machine-readable:\</i\> No.\</td\>

\<td\>\<b\>No.\</b\> No timestamp event logs.\</td\>

\<td\>\<b\>IMPORTANT\</b\>\</td\>

\</tr\>

\<tr\>

\<td\>\<b\>SAGE\</b\>\</td\>

\<td\>PRC 80, 015807 (2009)\</td\>

\<td\>Cr-51 and Ar-37 calibration
extractions.\<br\>\<i\>Machine-readable:\</i\> No.\</td\>

\<td\>\<b\>No.\</b\> Summary statistics only.\</td\>

\<td\>\<b\>IMPORTANT\</b\>\</td\>

\</tr\>

\<tr\>

\<td\>\<b\>KATRIN\</b\>\</td\>

\<td\>Nature Phys 18, 160 (2022)\</td\>

\<td\>Sub-eV neutrino mass limits.\<br\>\<i\>Machine-readable:\</i\> Yes
(Data releases).\</td\>

\<td\>\<b\>Yes.\</b\> Bounds eV-scale steriles.\</td\>

\<td\>\<b\>IMPORTANT\</b\>\</td\>

\</tr\>

\<tr\>

\<td\>\<b\>IceCube\</b\>\</td\>

\<td\>Nature Phys 14, 961 (2018)\</td\>

\<td\>Lorentz Violation / SME tensor
limits.\<br\>\<i\>Machine-readable:\</i\> Yes (Data releases).\</td\>

\<td\>\<b\>Yes.\</b\> Constrains high-energy anisotropy.\</td\>

\<td\>\<b\>OPTIONAL\</b\>\</td\>

\</tr\>

\<tr\>

\<td\>\<b\>Solar Neutrinos\</b\>\</td\>

\<td\>Borexino: Nature 562 (2018)\</td\>

\<td\>pp, Be-7, B-8 flux survival
probabilities.\<br\>\<i\>Machine-readable:\</i\> Yes (Borexino
portal).\</td\>

\<td\>\<b\>Yes.\</b\> Bounds total disappearance.\</td\>

\<td\>\<b\>ESSENTIAL\</b\>\</td\>

\</tr\>

\<tr\>

\<td\>\<b\>Cross-Section\</b\>\</td\>

\<td\>PLB 795, 542 (2019)\</td\>

\<td\>Gallium cross-section
uncertainties.\<br\>\<i\>Machine-readable:\</i\> No.\</td\>

\<td\>\<b\>No.\</b\> Theory limits remain debated.\</td\>

\<td\>\<b\>ESSENTIAL\</b\>\</td\>

\</tr\>

\<tr\>

\<td\>\<b\>Covariance\</b\>\</td\>

\<td\>N/A (Baksan collaboration)\</td\>

\<td\>Correlated systematics across BEST
zones.\<br\>\<i\>Machine-readable:\</i\> N/A.\</td\>

\<td\>\<b\>N/A.\</b\>\</td\>

\<td\>\<b\>UNAVAILABLE\</b\>\</td\>

\</tr\>

\</tbody\>

\</table\>

\[5/25/26 9:18 AM\] Lukaszzz: \<h2\>B. Missing Information & Validation
Blockers\</h2\>

\<div class=\"alert-box\"\>

\<b\>Fundamental Underconstraint:\</b\> The LSC framework introduces a
detector-frame tensor (D_ij) allowing for directional and
orientation-dependent variation. The public data is
\<b\>insufficient\</b\> to constrain this.

\</div\>

\<ul\>

\<li\>\<b\>Missing Covariance:\</b\> The lack of a public, fully
correlated systematic covariance matrix for the BEST inner/outer zones
prevents rigorous \$\\chi\^2\$ testing. Treating the zones as having
diagonal independent errors artificially inflates the statistical
significance of any fit.\</li\>

\<li\>\<b\>Missing Timestamps & Sidereal Data:\</b\> To fit the
traceless (directional) parameters of the LSC framework, precise
time-stamped event data for extraction runs must be mapped to celestial
coordinates (ICRS). This metadata is completely absent from public
archives.\</li\>

\<li\>\<b\>Private Access Requirement:\</b\> Public data alone is
entirely insufficient for full likelihood-level validation. Falsifying
or proving the orientation-dependent parameters of LSC requires direct
collaboration access to proprietary Baksan hardware logs and extraction
chronologies.\</li\>

\</ul\>

\<h2\>C. BEST-2 Resolution Capability\</h2\>

\<p\>

\<b\>Can BEST-2 realistically resolve the ambiguity?\</b\>\<br\>

Partially. BEST-2 aims to refine measurements, potentially altering
target geometries or baseline distances. If BEST-2 identifies a clear
oscillation-like wave (distance-dependent), it strongly supports the
standard sterile-neutrino hypothesis. If the deficit remains uniformly
isotropic across new geometries, it supports either a normalization
error (cross-section) or the isotropic trace parameter of LSC.

\</p\>

\<p\>

However, \<b\>detector/systematics degeneracy will remain\</b\> unless
BEST-2 specifically publishes continuous, time-resolved extraction data
mapped to celestial coordinates. Without this, an LSC tensor fit is
indistinguishable from localized chemical inefficiencies or transient
noise.

\</p\>

\<div class=\"page-break\"\>\</div\>

\<h2\>D. Requisite Packages & Constraint Maps\</h2\>

\<h3\>1. Minimum Required Dataset Package\</h3\>

\<ul\>

\<li\>Official extraction rates for BEST, SAGE, and GALLEX (Publicly
available).\</li\>

\<li\>Gallium cross-section theoretical bounds (Bahcall/Kostensalo)
(Publicly available).\</li\>

\<li\>Exact spatial coordinates of all target chamber zones relative to
the Earth\'s rotational axis (Private/Limited).\</li\>

\</ul\>

\<h3\>2. Critical Missing Information List (The Blockers)\</h3\>

\<ul\>

\<li\>Run-by-run fully correlated covariance matrices for BEST.\</li\>

\<li\>Absolute UTC timestamps for the initiation and conclusion of each
chemical extraction.\</li\>

\<li\>Counter-level efficiencies and dead-time hardware logs.\</li\>

\</ul\>

\<h3\>3. External Constraint Map\</h3\>

\<ul\>

\<li\>\<b\>Solar/Atmospheric Consistency:\</b\> Limits maximum isotropic
disappearance. Constrains LSC\'s \$ lpha_D\$ to avoid violating Borexino
limits.\</li\>

\<li\>\<b\>KATRIN:\</b\> Prevents the framework from assuming heavy
sterile masses beyond \$\\sim 0.8\$ eV as a baseline comparator.\</li\>

\<li\>\<b\>Standard-Model Extension (SME) Limits:\</b\> IceCube searches
place stringent limits on Lorentz-violating tensor fields. If LSC
assumes a cosmological background tensor, it must conform to IceCube\'s
SME bounds (\$\< 10\^{-24}\$).\</li\>

\</ul\>

\<h3\>4. Pre-BEST-2 Freeze Readiness Assessment\</h3\>

\<p\>

The framework is mathematically mature enough to be frozen, but it is
\<b\>experimentally unready\</b\> for true falsification due to the
public data vacuum. It must be frozen as a \"conditional template\"
awaiting private data, rather than an immediately testable hypothesis.

\</p\>

\[5/25/26 9:18 AM\] Lukaszzz: \<h2\>E. Final Decision\</h2\>

\<div class=\"highlight-box\"\>

\<b\>RECOMMENDATION: FREEZE WITH DOWNGRADED CLAIMS\</b\>\<br\>

Based on the severe lack of public covariance and orientation metadata,
the LSC framework should be \<b\>FROZEN\</b\> in its current
mathematical state (v6.3.0), but its operational status must be strictly
limited.

\<br\>\<br\>

It cannot be presented as a fully verifiable theory using only public
data. The freeze must explicitly state that the tensor (directional)
components of LSC are currently untestable and that the framework serves
solely as a preregistered mathematical pipeline, completely dependent on
future collaboration with the BEST-2 team for sidereal and hardware
metadata.

\</div\>

\</body\>

\</html\>
