# LSC arXiv workspace build log

Generated three arXiv-safe source packages:

- LSC 4.2
- LSC 5.0
- LSC 6.2

Workspace:

- /home/l/Desktop/LSC_ARXIV_WORKSPACE

Source material used:

- Local archive: /home/l/Desktop/prace dark neutrino 
- LSC 4.2 Zenodo PDF: _CLEAN_ORGANIZED/02_LSC_4_2/LSC_4_2_ULTRA_FULL_ZENODO.pdf
- LSC 5.0 local Markdown source: _CLEAN_ORGANIZED/03_LSC_5_0/LSC5.0_full.md
- LSC 6.0 Zenodo release PDF and public links, used as the conservative base for LSC 6.2
- Prism/dispersion report material, used only as an analogy for the LSC 6.2 wording
- Local figures copied from the organized archive and renamed without spaces

Corrections and arXiv compatibility changes:

- Created mandatory main.tex for every package.
- Used only stable arXiv-compatible packages: amsmath, amssymb, graphicx, hyperref.
- Rewrote equations manually into simple LaTeX equation/align environments.
- Avoided custom classes, external file references, exotic packages, and filenames with spaces.
- Added conservative wording where the source material was incomplete or partly speculative.
- Added direct public references to the LSC GitHub/Zenodo materials inside the bibliography.
- LSC 6.2 is an arXiv-safe synthesis draft based on LSC 6.0 plus the prism/dispersion extension, not a verbatim recovered source document.

Compilation test:

- LSC_4_2_arxiv/main.tex: pdflatex completed successfully; PDF generated.
- LSC_5_0_arxiv/main.tex: pdflatex completed successfully; PDF generated.
- LSC_6_2_arxiv/main.tex: pdflatex completed successfully; PDF generated.

Final ZIP policy:

- ZIP files contain only main.tex and figures/.
- Auxiliary LaTeX files, local build PDFs, logs, and notes are kept in the workspace but excluded from upload ZIPs.

Upgrade after Gemini theoretical review:

- LSC 4.2:
  - Replaced the evolution parameter with an affine parameter lambda.
  - Added local-energy definition E_loc(r)=E_infty/sqrt(|g_tt(r)|).
  - Added covariant phase integral with sqrt(g_rr/|g_tt|).
  - Added flat-space limit check.
  - Added a conservative note that spin-connection terms are neglected for radial Schwarzschild propagation.
  - Renamed the output section to Phenomenological Implications and added a minimal Delta m_eff^2 example.

- LSC 5.0:
  - Removed any implication that ordinary terrestrial Schwarzschild redshift explains the anomaly.
  - Reframed the model as an effective energy-reconstruction ansatz.
  - Added E_eff(x)=E_rec G(x).
  - Added the phase integral Phi_ij=int Delta m^2/(2 E_eff) dx.
  - Added a constant-correction example and Delta m_eff^2 approximation.
  - Added Required Magnitude of Effective Potential, including the note that standard GR is too small at roughly 10^-10.

- LSC 6.2:
  - Changed the primary framing from prism analogy to detector-frame tensor anisotropy.
  - Defined D_ij=delta(n_i n_j - delta_ij/3).
  - Added E_rec(p_hat)=E_true(1+D_ij p_hat^i p_hat^j).
  - Added IceCube-style anisotropy/systematics wording, including crystal-orientation fabric context.
  - Added a chi-square mapping for binned energy-angular-time data.
  - Kept prism/dispersion language only as a secondary visualization analogy.

Post-upgrade compilation:

- LSC_4_2_arxiv/main.tex: pdflatex completed successfully after upgrade.
- LSC_5_0_arxiv/main.tex: pdflatex completed successfully after upgrade.
- LSC_6_2_arxiv/main.tex: pdflatex completed successfully after upgrade.

Additional LSC 6.2 mathematical correction:

- Split propagation and detector reconstruction into separate equations:
  E_true(x)=E_infty G(g_mu_nu,Phi(x)) and
  E_rec=E_true(1+alpha_D D_ij p_hat^i p_hat^j).
- Replaced the former direct phase-index expression with the standard oscillation phase integral:
  Delta Phi_ij = int_0^L Delta m_ij^2/(2 E_eff(x)) dx.
- Defined E_eff(x)=E_true(x)[1+delta_G(x)+alpha_D D_ij p_hat^i p_hat^j].
- Added the explicit contraction D_ij p_hat^i p_hat^j =
  delta[(p_hat dot n)^2 - 1/3].
- Updated Delta m_eff notation to Delta m_{ij,eff}^2 and epsilon_D=D_kl p_hat^k p_hat^l.
- Removed direct optical/prism interpretation language and kept only a conservative effective phase-correction interpretation.
- Added sigma_k^2=sigma_stat,k^2+sigma_sys,k^2 to the chi-square model.
- Added representative illustration value delta ~ 0.05.
- Added the abstract sentence that the work provides a testable phenomenological ansatz and does not claim a fundamental origin.
- Rebuilt LSC_6_2_arxiv.zip and verified that the ZIP compiles after extraction.

LSC 6.2 pre-arXiv lock:

- Updated title to "A Phenomenological Framework for Neutrino Propagation and Detector-Frame Tensor Anisotropy".
- Removed double counting of propagation in E_eff by using E_eff(x)=E_true(x)[1+alpha_D D_ij p_hat^i p_hat^j].
- Added the standard-framework recovery limit D_ij -> 0 and delta_G -> 0.
- Verified required figures exist with no spaces in filenames.
- Rebuilt LSC_6_2_arxiv.zip with only main.tex and figures/, then verified compilation after extraction.
