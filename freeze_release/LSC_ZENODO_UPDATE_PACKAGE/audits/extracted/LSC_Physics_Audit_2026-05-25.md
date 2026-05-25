**LSC FRAMEWORK**

**HOSTILE PHYSICS AUDIT**

*Pre-BEST-2 Freeze \| Independent Scientific Review*

Generated: 2026-05-25 \| Version reviewed: LSC 6.3.0 (Zenodo 20037838)

**AUDIT MANDATE:** This document provides a hostile but scientifically
fair physics audit of the LSC (Lepto-Scalar Coupling) neutrino
phenomenology framework. The auditor\'s role is to identify weak
assumptions, hidden inconsistencies, dimensional problems, physically
implausible structures, overclaims, undefined variables, unsupported
inference jumps, and places where detector effects are confused with
neutrino-sector physics. No new LSC theory is invented here.

**TREATMENT:** LSC is treated throughout as an **[unvalidated
phenomenological framework]{.underline}**, not established physics.

  ----------------- ----------------- ----------------- -----------------
  **CRITICAL**      **HIGH** May      **MEDIUM**        **LOW**
  Immediate         invalidate key    Statistical or    Documentation /
  exclusion risk or predictions       physical gap      provenance issue
  fundamental                                           
  incoherence                                           

  ----------------- ----------------- ----------------- -----------------

**1. EXECUTIVE AUDIT SUMMARY**

The LSC framework, as of version 6.3.0, presents a detector-response
tensor ansatz intended to model the Gallium/BEST neutrino anomaly
without claiming discovery. The framework has undergone significant
self-correction from its PBH-curvature origins (4.2) through to the
trace/traceless separation (6.3.0). The internal discipline of the 6.3.0
freeze protocol is genuine and commendable. However, the framework
carries several unresolved problems that range from immediately fatal
(CRITICAL) to statistically disqualifying (HIGH) to correctible
(MEDIUM/LOW).

The key overall diagnosis:

-   The framework is not falsified but is also not yet falsifiable in
    its current form.

-   The tensor degree of freedom significantly exceeds the available
    observational constraints.

-   The central physical mechanism (delta_G) has no derivable connection
    to any known physics at the required scale.

-   The Lorentz-violation implications of the D_ij tensor are entirely
    unaddressed and may constitute immediate experimental exclusion.

-   The statistical framework is formally incomplete without full
    covariance matrices.

  -------- --------------------------------------------- ------------------
  **\#**   **Finding**                                   **Severity**

  **1**    Effective Parameter delta_G Has No Physical   **CRITICAL**
           Derivation                                    

  **2**    Tensor A_ij Has 5 Free Parameters for 3       **CRITICAL**
           Observables --- Model is Underdetermined      

  **3**    Lorentz Violation in LSC 5.5 Lagrangian Is    **CRITICAL**
           Not Addressed                                 

  **4**    KATRIN Constraint Is Stated Without           **HIGH**
           Derivation                                    

  **5**    IceCube \'Analogy\' Is Physically Unmotivated **HIGH**

  **6**    Distinguishability from Detector Systematics  **HIGH**
           Is Not Established                            

  **7**    Sidereal Test Is Currently Unfalsifiable      **HIGH**

  **8**    Chi-Squared Without Full Covariance Matrix Is **HIGH**
           Statistically Invalid                         

  **9**    Cross-Section Scaling sigma \~ E\^2 Is        **MEDIUM**
           Incorrect Near Gallium Threshold              

  **10**   Trace/Traceless Separation Assumes Detector   **MEDIUM**
           Response Tensor Is Constant in Time           

  **11**   Leave-One-Out Instability Is Acknowledged but **MEDIUM**
           Not Resolved                                  

  **12**   The f0_a and fA_a Functions Are Undefined     **MEDIUM**

  **13**   LSC 4.2 PBH Curvature Language Residue in     **LOW**
           Later Versions                                

  **14**   Zenodo Record 19769179 Is Inaccessible ---    **LOW**
           Provenance Gap                                
  -------- --------------------------------------------- ------------------

**2. DETAILED FINDINGS**

+-----------------------------------------------------------------------+
| **FINDING 1: Effective Parameter delta_G Has No Physical Derivation   |
| \[CRITICAL\]**                                                        |
|                                                                       |
| ***QUOTED TEXT:** LSC 6.0 explicitly warns that natural solar-system  |
| gravitational effects are too small to directly explain percent-level |
| Gallium deficits, so delta_G is treated as an effective parameter.*   |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| The gravitational redshift from the Sun to Earth is approximately     |
| GM_sun/(R_sun \* c\^2) \~ 2 x 10\^-6, six orders of magnitude below   |
| the \~21% BEST deficit. The framework acknowledges this but retains   |
| delta_G as a free \'effective\' parameter without any physical        |
| mechanism to amplify it. This is mathematically equivalent to         |
| introducing a free normalization parameter with a curvature label.    |
| The physical interpretation is undefined. \'Effective\' parameters    |
| without a generating mechanism are phenomenological fudge factors.    |
| There is no field theory, no symmetry, and no dimensional argument    |
| supplied that would connect delta_G to any observable at the percent  |
| level. This is the central unresolved problem of the entire           |
| framework.                                                            |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Either (a) provide an explicit field-theoretic or geometrical         |
| mechanism that produces delta_G \~ 0.1-0.2 without conflict with      |
| solar system tests (where gravitational corrections are constrained   |
| to \< 10\^-7), or (b) rename delta_G as a pure normalization free     |
| parameter with no gravitational label and remove all curvature        |
| language from 6.0 onward. Option (b) makes the framework honest but   |
| trivial. Option (a) has not been attempted.                           |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 2: Tensor A_ij Has 5 Free Parameters for 3 Observables ---  |
| Model is Underdetermined \[CRITICAL\]**                               |
|                                                                       |
| ***QUOTED TEXT:** q_a(t,Omega) = n_i\^lab(t,Omega) A_a\^{ij}          |
| n_j\^lab(t,Omega) \... A_a\^{ij} = A_a\^{ji}, Tr(A_a) = 0*            |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| A symmetric traceless 3x3 real tensor has exactly 5 independent       |
| components. The primary observational target is BEST: three numbers   |
| (R_inner, R_outer, R_outer/R_inner --- only two of which are          |
| independent). Adding the scalar lambda0 and anisotropic coupling      |
| lambdaA, the model has at minimum 7 free parameters (5 tensor         |
| components + 2 couplings) for 2 independent observables from BEST,    |
| with GALLEX and SAGE contributing perhaps 2-4 more single-zone        |
| ratios. The model is severely underdetermined. Any structured         |
| residual pattern from BEST can be reproduced by appropriate choice of |
| A_ij without any predictive content. This is not a physically         |
| constrained model --- it is a curve-fitting template with post-hoc    |
| justification.                                                        |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Reduce the tensor to physically motivated components. If a preferred  |
| axis exists (e.g., galactic plane, ecliptic, specific direction), fix |
| the tensor orientation a priori and fit only the amplitude.           |
| Alternatively, perform a Bayesian model comparison with explicit      |
| penalty for parameter count (e.g., DIC, WAIC, or Bayesian evidence    |
| ratio). Show that the model improves over M1 (scalar normalization)   |
| by more than the AIC/BIC penalty for the additional degrees of        |
| freedom.                                                              |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 3: Lorentz Violation in LSC 5.5 Lagrangian Is Not Addressed |
| \[CRITICAL\]**                                                        |
|                                                                       |
| ***QUOTED TEXT:** L_tot = sqrt(-g) \[i psi-bar gamma\^mu nabla_mu     |
| psi - m_eff psi-bar psi - G_D psi-bar gamma\^mu D_mu_nu gamma\^nu     |
| psi\]*                                                                |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| The coupling term G_D psi-bar gamma\^mu D_mu_nu gamma\^nu psi, where  |
| D_mu_nu is a fixed background tensor (not a dynamical field),         |
| explicitly breaks local Lorentz invariance. This falls within the SME |
| (Standard Model Extension) framework of Lorentz-violation operators.  |
| For neutrinos at MeV energies, SME coefficients analogous to this     |
| term are constrained to \< 10\^-28 GeV from IceCube data on           |
| ultra-high-energy neutrinos (Abbasi et al. 2010, Phys.Rev.D           |
| 82:112003) and from atmospheric neutrino data. The 5.5 Lagrangian is  |
| not referenced against these bounds. Even if the 5.5 formalism is     |
| \'historical,\' it bleeds into 6.0/6.3.0 via the D_ij tensor which    |
| carries the same Lorentz-violating structure. This is not a minor     |
| formal issue --- it is a potential immediate experimental exclusion.  |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Map the D_ij anisotropy tensor explicitly onto the SME coefficient    |
| table (specifically the (a_L)\^mu and (c_L)\^mu_nu operators).        |
| Compute the SME coefficients implied by the LSC parameter region and  |
| compare against published bounds from IceCube, MINOS, T2K, and        |
| atmospheric neutrino experiments. If the required coefficients are    |
| excluded, the entire anisotropy sector must be abandoned.             |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 4: KATRIN Constraint Is Stated Without Derivation           |
| \[HIGH\]**                                                            |
|                                                                       |
| ***QUOTED TEXT:** \|delta_G + alpha_D Delta_D\|\_KATRIN \<\< 10\^-2*  |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| KATRIN measures neutrino mass through spectral endpoint distortions   |
| at sub-eV energies near the tritium endpoint (18.6 keV). The LSC      |
| energy-reconstruction shift (Delta E/E \~ 0.03-0.06) is stated to be  |
| constrained by KATRIN at the level \<\< 10\^-2, but no derivation is  |
| given. The constraint origin is unclear: KATRIN does not directly     |
| measure the absolute energy scale at the level relevant to MeV-scale  |
| gallium experiments. A 3-6% energy reconstruction shift at 750 keV    |
| (Cr-51 neutrino energy) does not trivially translate to KATRIN        |
| constraint at 18.6 keV without an explicit model of energy            |
| dependence. If the tensor D_ij is energy-independent, a 3-6% shift at |
| MeV scale would produce an enormous distortion of the KATRIN endpoint |
| --- already excluded by KATRIN data at \< 0.1 eV\^2/c\^4 precision.   |
| If D_ij is strongly energy-dependent (falling off as 1/E or faster),  |
| this must be specified and the energy dependence must be              |
| independently motivated.                                              |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Provide an explicit calculation of the KATRIN constraint: (1) specify |
| the energy dependence of f0_a(E,t) and fA_a(E,t), (2) compute the     |
| implied endpoint distortion in the KATRIN spectrum, (3) compare       |
| against KATRIN published limits. If the energy functions fall off     |
| fast enough to evade KATRIN, that functional form must be published   |
| as part of the frozen model spec before BEST-2 fitting.               |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 5: IceCube \'Analogy\' Is Physically Unmotivated \[HIGH\]** |
|                                                                       |
| ***QUOTED TEXT:** IceCube is relevant as a constraint/veto or         |
| detector anisotropy analogy, not direct gallium evidence.*            |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| IceCube operates at 100 GeV - 10 PeV, gallium experiments at \~0.75   |
| MeV. The energy ratio is \~10\^8 - 10\^13. Using IceCube as a         |
| \'detector anisotropy analogy\' for gallium detectors is physically   |
| unmotivated without specifying the energy scaling of the D_ij tensor. |
| If D_ij is energy-independent, IceCube limits on directional neutrino |
| flux asymmetry and on SME Lorentz-violation coefficients immediately  |
| rule out the LSC parameter range needed to fit the BEST deficit. If   |
| D_ij is strongly energy-dependent (suppressed at IceCube energies),   |
| the suppression mechanism must be specified. \'Analogy\' is not a     |
| scientific constraint. The document oscillates between calling        |
| IceCube a \'constraint/veto\' and an \'analogy\' --- these are        |
| contradictory uses.                                                   |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Decide: Is IceCube a constraint or not? If yes, compute the LSC       |
| prediction for IceCube directional flux asymmetry given the parameter |
| range required for BEST, and show it is consistent with IceCube       |
| published limits. If no, remove all IceCube references from the       |
| constraint section and state explicitly why the energy extrapolation  |
| is not valid.                                                         |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 6: Distinguishability from Detector Systematics Is Not      |
| Established \[HIGH\]**                                                |
|                                                                       |
| ***QUOTED TEXT:** LSC addresses the Gallium/BEST anomaly as a         |
| phenomenological question: can a propagation-plus-detector-response   |
| model structure source-experiment residuals better than null,         |
| normalization-only, cross-section/systematics, sterile-neutrino, or   |
| detector-systematics alternatives?*                                   |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| The LSC tensor epsilon_LSC(E,t,Omega) modifies the detector           |
| efficiency as a function of neutrino direction relative to the        |
| detector frame. This is formally identical to an unknown position-    |
| and direction-dependent detector efficiency systematic. BEST, GALLEX, |
| and SAGE all have reported systematic uncertainties in counter        |
| efficiencies, gallium extraction yields, and source geometry. The     |
| question \'does LSC fit better than detector-systematics baseline     |
| M4?\' cannot be answered without knowing what M4 assumes --- but M4   |
| is not defined in detail in the document. If M4 allows a general      |
| direction-dependent efficiency correction, it will trivially absorb   |
| all LSC signal. The LSC framework provides no physical criterion for  |
| separating \'neutrino-sector anisotropy\' from \'unknown detector     |
| directional systematic.\' This is the core unfalsifiability risk.     |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Define M4 (detector-systematics baseline) with explicit physical      |
| motivation: which specific systematics are included, at what level,   |
| and why the LSC tensor cannot be mimicked by any combination of known |
| or plausible systematics. This requires collaboration with the BEST   |
| experimental team to understand the actual detector geometry, counter |
| placement, and shielding anisotropy. Without this, LSC and            |
| detector-systematic are observationally equivalent.                   |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 7: Sidereal Test Is Currently Unfalsifiable \[HIGH\]**      |
|                                                                       |
| ***QUOTED TEXT:** Sidereal/orientation modulation is a discriminating |
| future test\... Required evidence: Time-stamped exposures,            |
| orientation metadata, environmental corrections.*                     |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| The document correctly identifies that the sidereal test requires     |
| timestamps and detector orientation metadata --- and then notes this  |
| data does not exist. A prediction that cannot be tested with          |
| available data is not a scientific prediction, it is a theoretical    |
| aspiration. Worse, the claim is classified as \'speculative\' with    |
| risk \'medium-high.\' The sidereal modulation signal depends on the   |
| same A_ij tensor that is underdetermined from BEST data alone (see    |
| Finding 2). An A_ij fit to BEST rate ratios is not sufficient to make |
| a unique sidereal prediction without specifying the tensor            |
| orientation in ICRS coordinates. If the tensor orientation is a free  |
| parameter, sidereal modulation is also a free prediction --- any      |
| modulation amplitude and phase can be accommodated post-hoc.          |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Fix the tensor orientation in ICRS coordinates a priori, based on an  |
| explicit physical hypothesis (e.g., galactic center direction, solar  |
| magnetic field direction, CMB dipole direction). Then compute the     |
| predicted sidereal modulation amplitude and phase for BEST geometry.  |
| Archive this as a frozen pre-BEST-2 prediction. If BEST-2 does not    |
| have orientation/timestamp data, state explicitly that this           |
| prediction cannot be tested and remove it from the falsifiability     |
| criteria.                                                             |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 8: Chi-Squared Without Full Covariance Matrix Is            |
| Statistically Invalid \[HIGH\]**                                      |
|                                                                       |
| ***QUOTED TEXT:** chi2(theta, eta) = \[R_obs - R_pred\]\^T C\^{-1}    |
| \[R_obs - R_pred\] + penalty(eta) \... Missing full extraction table, |
| counter efficiencies and covariance matrix.*                          |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| The statistical procedure requires the full covariance matrix C for   |
| BEST/GALLEX/SAGE rate ratios. The document explicitly acknowledges    |
| this matrix is unavailable. Without C, any chi-squared minimization   |
| uses an assumed (typically diagonal) error structure that ignores     |
| correlations between zones, between sources, and between systematic   |
| uncertainties. For BEST specifically, the inner and outer zone        |
| measurements are correlated through shared source geometry, germanium |
| extraction yield, and counting efficiency calibration. Using a        |
| diagonal covariance matrix will give incorrect best-fit parameters    |
| and invalid confidence intervals. Any published result based on this  |
| chi-squared is statistically unjustified.                             |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Do not publish any fit results using the available summary-level data |
| until the full covariance matrices are obtained from the experimental |
| collaborations. If the covariance matrices are not available, state   |
| explicitly that no statistically valid fit can be performed and that  |
| all current fits are exploratory order-of-magnitude estimates only.   |
| This is not optional for any arXiv submission.                        |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 9: Cross-Section Scaling sigma \~ E\^2 Is Incorrect Near    |
| Gallium Threshold \[MEDIUM\]**                                        |
|                                                                       |
| ***QUOTED TEXT:** sigma(E) \~ E\^2 \... sigma(E) propto E\^2*         |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| The gallium neutrino capture cross-section for 71Ga + nu_e -\> 71Ge + |
| e\^- does NOT scale as E\^2 at MeV energies. Near the threshold (E_th |
| = 233 keV), the cross-section rises sharply from zero, but at the     |
| 51Cr neutrino line energy (747 keV) and 37Ar neutrino line (814 keV), |
| the cross-section is determined by nuclear matrix elements,           |
| Gamow-Teller transitions to specific 71Ge excited states, and phase   |
| space. The E\^2 scaling is the naive allowed-spectrum approximation   |
| valid only when E \>\> E_threshold and transition form factors are    |
| constant. For the gallium system, the cross-section has been computed |
| by Bahcall (1997) and Haxton (1998) including the specific            |
| excited-state contributions. The LSC sensitivity estimate Delta_N/N   |
| \~ A_eff \* Delta_E/E (eq. 37) depends critically on d(ln sigma)/d(ln |
| E), which is NOT equal to 2 at 750 keV.                               |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Replace E\^2 scaling with the actual computed d(ln sigma)/d(ln E)     |
| from Bahcall 1997 / Haxton 1998 at the specific source energies.      |
| Recompute the LSC energy-response sensitivity. This may change the    |
| required delta_G and alpha_D by factors of 2-3. The Gamow-Teller      |
| matrix elements for transitions to excited states of 71Ge introduce   |
| additional energy dependence that could substantially change the      |
| sensitivity estimate.                                                 |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 10: Trace/Traceless Separation Assumes Detector Response    |
| Tensor Is Constant in Time \[MEDIUM\]**                               |
|                                                                       |
| ***QUOTED TEXT:** The anisotropic term must be evaluated in a fixed   |
| celestial frame and transformed to the lab frame for sidereal tests.* |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| The decomposition D_ij = D_ij\^iso + Delta_D_ij (eq. 49) assumes the  |
| tensor is static in the celestial (ICRS) frame and the time           |
| dependence enters only through Earth\'s rotation (the n_lab(t)        |
| transformation). This is only valid if the physical mechanism         |
| producing the anisotropy is static on the timescale of the            |
| experiments (weeks to months for source calibration campaigns). If    |
| the mechanism has any temporal variation (e.g., from solar wind,      |
| detector aging, or seasonal effects), the tensor is not separable in  |
| this way. More importantly, the three experiments (BEST, GALLEX,      |
| SAGE) took data at different epochs spanning \~30 years. Requiring a  |
| single static A_ij tensor to fit all three simultaneously is a strong |
| and unstated assumption that any anisotropy source is cosmological in |
| origin and completely stable over decades.                            |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| State explicitly that a static celestial-frame tensor is assumed over |
| the \~30-year baseline of gallium experiments. Quantify whether any   |
| known physical mechanism (solar activity cycles, detector drift)      |
| could produce a spurious time-varying apparent anisotropy. If         |
| temporal variation is possible, allow for epoch-dependent A_ij        |
| tensors and assess whether the fit degrades to unconstrained.         |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 11: Leave-One-Out Instability Is Acknowledged but Not       |
| Resolved \[MEDIUM\]**                                                 |
|                                                                       |
| ***QUOTED TEXT:** The strongest internal warning is that exact anchor |
| fits are insufficient; leave-one-out and cross-experiment validation  |
| are required\... the 6.2.1 package demonstrates exact anchor fits but |
| also leave-one-out instability.*                                      |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| Leave-one-out cross-validation instability means that the model       |
| parameters fitted to N-1 experiments do not predict the held-out      |
| experiment. This is a direct signal of overfitting. The 6.2.1 codex   |
| analysis identified this problem but the 6.3.0 freeze protocol does   |
| not resolve it --- it only mandates that it should be checked. The    |
| model cannot be presented as providing any predictive improvement     |
| over simpler baselines while leave-one-out instability persists. Any  |
| claim that LSC \'structures residuals better than alternatives\' is   |
| invalid until LOO stability is demonstrated.                          |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Perform and report the full leave-one-out analysis results now,       |
| before BEST-2. If LOO is unstable, reduce model complexity until      |
| stability is achieved, then re-freeze the simpler model. Do not       |
| submit to BEST-2 comparison with a model known to be LOO-unstable.    |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 12: The f0_a and fA_a Functions Are Undefined \[MEDIUM\]**  |
|                                                                       |
| ***QUOTED TEXT:** epsilon_LSC,a(E,t,Omega) = epsilon0_a(E,t,Omega) \* |
| \[1 + lambda0\*f0_a(E,t) + lambdaA\*q_a(t,Omega)\*fA_a(E,t)\]*        |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| The functions f0_a(E,t) and fA_a(E,t) appear in the core LSC 6.3.0    |
| equation (eq. 57) but are nowhere defined in the document. Their      |
| energy and time dependence is entirely unspecified. Without           |
| specifying these functions, the model is formally undefined ---       |
| lambda0 and lambdaA are meaningless without knowing what they         |
| multiply. The parameter count is also undefined: are f0 and fA        |
| parameterized families (adding more free parameters) or fixed known   |
| functions? This is not a minor omission; the entire predictive        |
| content of the model depends on these functions.                      |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Before any freeze, publish explicit functional forms for f0_a(E,t)    |
| and fA_a(E,t) with physical justification. These cannot be fitted     |
| from BEST data if they add free parameters --- they must be fixed a   |
| priori from physics (e.g., from the cross-section energy dependence,  |
| or from detector geometry). Freeze these functions as part of the     |
| pre-BEST-2 model specification.                                       |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 13: LSC 4.2 PBH Curvature Language Residue in Later         |
| Versions \[LOW\]**                                                    |
|                                                                       |
| ***QUOTED TEXT:** A PBH/curvature-centered framework using effective  |
| Hamiltonian and gravitationally coupled operator language\...         |
| historical/exploratory lineage; not the present Gallium core.*        |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| The curvature-coupled language from LSC 4.2 persists into LSC 6.0 via |
| H_grav = (E/c\^2)Phi(r) and the G(g_mu_nu, Phi(x)) propagation        |
| factor. While officially deprecated, equations 32-34 retain           |
| gravitational field labels that have no physical support at the       |
| percent level for solar system geometry. A reader of the 6.0 theory   |
| documents would encounter gravitational Hamiltonians and              |
| curved-spacetime propagation factors that are explicitly acknowledged |
| to be six orders of magnitude too small. This creates unnecessary     |
| confusion and potential for the historical material to be             |
| misinterpreted as current physical claims.                            |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| In all 6.0/6.3.0 documents, replace G(g_mu_nu, Phi(x)) with G_eff     |
| (dimensionless effective propagation factor, origin unspecified) and  |
| remove all gravitational field symbols from the expression. This is a |
| documentation fix, not a theory change, but it is necessary for       |
| intellectual honesty.                                                 |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **FINDING 14: Zenodo Record 19769179 Is Inaccessible --- Provenance   |
| Gap \[LOW\]**                                                         |
|                                                                       |
| ***QUOTED TEXT:** Note: 19769179 was provided as a Zenodo upload URL. |
| The public record API endpoint returned 404 during this               |
| reconstruction, so it is marked inaccessible.*                        |
|                                                                       |
| **ISSUE:**                                                            |
|                                                                       |
| A source cited in the inventory is permanently inaccessible via the   |
| public Zenodo API. For a framework intended for external review and   |
| BEST-2 comparison, all cited sources must be publicly verifiable. An  |
| inaccessible Zenodo record creates a provenance gap that cannot be    |
| resolved by reviewers.                                                |
|                                                                       |
| **RESOLUTION REQUIRED:**                                              |
|                                                                       |
| Verify whether record 19769179 was successfully published or is in    |
| private/draft state. If draft, either publish it or remove all        |
| references to it from the canonical source inventory. If it contained |
| theory content, reproduce that content in an accessible record.       |
+-----------------------------------------------------------------------+

**3. TOP 10 MOST DANGEROUS WEAKNESSES**

Ranked by threat to the framework\'s scientific validity:

  ---------- --------------------------- ----------------------- ------------------
  **Rank**   **Weakness**                **Why Dangerous**       **Severity**

  **1**      delta_G has no physical     Entire                  **CRITICAL**
             mechanism                   energy-reconstruction   
                                         sector is a free        
                                         normalization parameter 
                                         in disguise. No physics 
                                         separates it from       
                                         cross-section           
                                         normalization           
                                         uncertainty.            

  **2**      Lorentz-violation bounds    D_ij tensor may be      **CRITICAL**
             unaddressed                 immediately excluded by 
                                         IceCube SME limits,     
                                         eliminating the entire  
                                         anisotropy sector.      

  **3**      7 free parameters for 2-4   Model is unfalsifiable  **CRITICAL**
             observables                 as structured: any      
                                         residual pattern can be 
                                         fitted. No predictive   
                                         power.                  

  **4**      Leave-one-out instability   Known overfitting       **HIGH**
             unresolved                  signal. Model cannot    
                                         outperform baselines if 
                                         LOO is unstable.        

  **5**      No full covariance matrix   All chi-squared fits    **HIGH**
                                         are statistically       
                                         unjustified. No         
                                         publishable result can  
                                         emerge from current     
                                         data.                   

  **6**      KATRIN constraint not       The                     **HIGH**
             derived                     energy-reconstruction   
                                         shift required by LSC   
                                         may already be excluded 
                                         by KATRIN endpoint      
                                         measurements.           

  **7**      f0_a and fA_a are undefined Core equation (57) is   **HIGH**
                                         formally incomplete.    
                                         Model specification is  
                                         not frozen.             

  **8**      Sidereal prediction is      Tensor orientation is   **HIGH**
             unfalsifiable now           free; sidereal phase    
                                         and amplitude are       
                                         post-hoc. Data to test  
                                         it does not exist.      

  **9**      sigma \~ E\^2 is wrong at   Sensitivity estimates   **MEDIUM**
             750 keV                     are quantitatively      
                                         incorrect. Required     
                                         delta_G and alpha_D may 
                                         be wrong by factor 2-3. 

  **10**     Indistinguishable from      No physical criterion   **HIGH**
             detector systematic         separates LSC           
                                         anisotropy from unknown 
                                         direction-dependent     
                                         efficiency. M4 is       
                                         undefined.              
  ---------- --------------------------- ----------------------- ------------------

**4. WHAT PARTS ARE SALVAGEABLE**

**4A. Genuinely Sound Elements**

-   **The freeze protocol discipline (6.3.0). Requiring pre-registered
    model specs, comparison baselines M0-M6, and archived negative
    outcomes is methodologically correct. This should be retained and
    strengthened.**

-   **The acknowledgment that LSC is unvalidated phenomenology, not
    confirmed physics. This epistemic honesty is necessary and must not
    be weakened in any future version.**

-   **The leave-one-out validation requirement. The internal warning
    against anchor-fit overclaiming is the most scientifically honest
    element of the entire framework. It must be executed, not merely
    stated.**

-   **The trace/traceless decomposition as a structural principle.
    Separating scalar normalization shifts from directional anisotropy
    is physically well-motivated, assuming the anisotropy is pre-defined
    rather than fitted.**

-   **The comparison baseline structure (M0-M6). Requiring LSC to
    outperform sterile-neutrino and detector-systematics baselines by an
    explicit model-comparison metric is correct scientific practice.**

**4B. Conditionally Salvageable**

-   The D_ij detector response tensor --- IF the Lorentz-violation
    bounds are computed and the tensor is found to be compatible with
    SME limits. IF the tensor is reduced to 1-2 physically motivated
    free parameters rather than 5.

-   The sidereal test prediction --- IF the tensor orientation is fixed
    a priori in ICRS coordinates from an explicit physical hypothesis
    before any BEST-2 data is seen.

-   The energy-reconstruction sector --- IF delta_G is renamed as a pure
    effective normalization parameter with no gravitational label, and
    IF the cross-section sensitivity is recomputed from Bahcall/Haxton
    nuclear matrix elements.

**5. WHAT SHOULD BE FROZEN BEFORE BEST-2**

This is a minimal required freeze checklist. Fitting BEST-2 data before
these are completed invalidates the comparison.

  --------- ------------------------------------------------ ------------------
  **\#**    **Required Freeze Action**                       **Priority**

  **F1**    Publish explicit functional forms for f0_a(E,t)  **BLOCKING**
            and fA_a(E,t) with physical justification. No    
            fitting allowed until these are fixed.           

  **F2**    Reduce A_ij to ≤2 free parameters by fixing      **BLOCKING**
            tensor orientation from a pre-stated physical    
            hypothesis (specify the preferred direction).    

  **F3**    Compute SME Lorentz-violation coefficients       **BLOCKING**
            implied by the D_ij tensor and compare against   
            published IceCube, MINOS, T2K bounds.            

  **F4**    Replace sigma \~ E\^2 with actual d(ln           **BLOCKING**
            sigma)/d(ln E) from Bahcall 1997 / Haxton 1998   
            at 51Cr and 37Ar energies.                       

  **F5**    Perform and publish the leave-one-out            **BLOCKING**
            validation. If LOO is unstable, reduce model     
            complexity until it stabilizes. Frozen model     
            must be LOO-stable.                              

  **F6**    Derive the KATRIN energy-response constraint     **BLOCKING**
            from first principles given the chosen f0(E)     
            functional form.                                 

  **F7**    Define M4 (detector-systematics baseline) with   **BLOCKING**
            explicit physical content --- list which         
            detector effects are included and at what level. 

  **F8**    State explicitly that the covariance matrix C is **BLOCKING**
            incomplete and that all current fits are         
            order-of-magnitude exploratory only. No          
            statistical claims based on diagonal-error       
            chi-squared.                                     

  **F9**    Archive the pre-BEST-2 frozen model prediction   **REQUIRED**
            for BEST-2 zone ratios with uncertainty ranges   
            derived from LOO-stable parameter bounds.        

  **F10**   Fix the ICRS tensor orientation and compute the  **REQUIRED**
            predicted sidereal modulation amplitude and      
            phase for BEST geometry as a pre-registered      
            prediction.                                      
  --------- ------------------------------------------------ ------------------

**6. WHAT SHOULD BE REMOVED OR DOWNGRADED**

**6A. Remove Immediately**

-   All gravitational/curvature labels on delta_G. The gravitational
    contribution from solar system geometry is 10\^-6, not
    percent-level. The curvature framing is physically false and
    misleading.

-   The LSC 5.5 Lagrangian (eq. 31) from any document presented as
    current theory. It is formally Lorentz-violating and the bounds have
    not been checked. If retained for historical lineage only, label
    explicitly as \'EXCLUDED FROM CURRENT CORE --- LORENTZ VIOLATION
    UNCHECKED.\'

-   The claim that \'IceCube is relevant as constraint/veto\' without a
    derived calculation. Either compute the constraint or remove the
    IceCube constraint claim.

-   E\^2 cross-section scaling from all sensitivity estimates. It is
    numerically wrong for the gallium system.

**6B. Downgrade to \'Speculative / Unvalidated\'**

-   All claims about sidereal modulation. These are unfalsifiable
    without orientation metadata and an a priori fixed tensor
    orientation.

-   All figures and estimates derived from chi-squared without full
    covariance. These are exploratory illustrations, not statistical
    results.

-   The claim that the anomaly \'cannot be explained by standard
    oscillation\' as a statement implicitly supporting LSC. This
    requires a full Bayesian model comparison that has not been done.

**7. IS THE FRAMEWORK SCIENTIFICALLY PUBLISHABLE?**

The direct answer is: NOT IN CURRENT FORM. The conditional answer is:
possibly, after specific repairs, as a narrowly scoped working paper.

**7A. Current Disqualifiers for Publication**

-   Equations with undefined functions (f0_a, fA_a) cannot appear in a
    published paper.

-   A model known to be leave-one-out unstable cannot be presented as
    providing predictive improvement over baselines.

-   Statistical fits using incomplete covariance matrices must be
    labeled as preliminary and non-statistical throughout.

-   Lorentz-violation implications of D_ij must be addressed before any
    anisotropy claims can appear in print.

-   The 7-parameter model fitted to 2-4 observables must include
    explicit AIC/BIC/Bayesian evidence ratios against simpler models.

**7B. What a Publishable Version Would Look Like**

A legitimate conservative working paper could be structured as follows:

-   Title: \'A Detector-Response Tensor Template for Gallium Neutrino
    Source Experiments: Motivation, Formalism, and Pre-BEST-2
    Predictions\'

-   Claims: The paper claims only (1) the formalism is internally
    consistent, (2) it is distinguishable from sterile-neutrino models
    in specific observables (specify which), and (3) it makes one
    pre-registered prediction for BEST-2 zone ratios.

-   The cross-section scaling must use Bahcall/Haxton nuclear matrix
    elements.

-   The SME analysis must be included as a section, showing either
    compatibility or identifying the required energy-dependence of f(E)
    to evade bounds.

-   The covariance matrix limitation must be stated prominently in the
    abstract.

-   LOO validation must be completed and reported.

-   Model comparison against M0-M4 must use BIC or Bayesian evidence,
    not raw chi-squared.

**8. FINAL VERDICT**

+-----------------------------------------------------------------------+
| **VERDICT: UNREADY FOR BEST-2 COMPARISON IN CURRENT FORM**            |
|                                                                       |
| The LSC 6.3.0 framework has genuine intellectual value as a           |
| systematic attempt to parameterize detector-response contributions to |
| the Gallium anomaly. The freeze protocol and epistemic discipline of  |
| 6.3.0 are significantly better than earlier versions. However:        |
|                                                                       |
| -   Three CRITICAL findings (delta_G unphysical mechanism,            |
|     Lorentz-violation unaddressed, model underdetermined) mean the    |
|     framework is not yet scientifically coherent.                     |
|                                                                       |
| -   Four HIGH findings (KATRIN constraint uncomputed, covariance      |
|     matrix absent, f0/fA undefined, sidereal unfalsifiable) mean the  |
|     framework is not yet statistically valid.                         |
|                                                                       |
| -   The framework risks becoming an unfalsifiable flexible template   |
|     if the tensor degree of freedom is not reduced and the physical   |
|     origin of the anisotropy is not specified a priori.               |
|                                                                       |
| -   The framework is not falsified. It remains a legitimate           |
|     phenomenological direction IF the 8 BLOCKING items in Section 5   |
|     are resolved before any BEST-2 data is touched.                   |
|                                                                       |
| **Recommendation: Complete F1 through F8 (blocking freeze items).     |
| Resubmit for audit. Do not fit BEST-2 data until those items are      |
| publicly archived.**                                                  |
+-----------------------------------------------------------------------+

*Audit generated 2026-05-25 \| Claude physics criticism role per LSC
6.3.0 Freeze Statement \| No new LSC theory introduced*
