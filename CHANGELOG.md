# Changelog

All notable changes to the `bio-agent-skills` package and CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-11-06

### Added
- **Guruprasad Instability Index (`bioskills.core.peptide`)**:
  - Embedded the complete $20 \times 20$ Dipeptide Instability Weight Value (DIWV) matrix ($399$ statistical pairs from Guruprasad et al., 1990).
  - Analytical prediction of *in vitro* peptide stability ($II < 40$ classified as stable; $II \ge 40$ as unstable).
  - New CLI subcommand: `bioskills peptide stability --seq <SEQ> [--json]`.
- **Boman Interaction Index (`bioskills.core.peptide`)**:
  - Implementation of Boman (2003) protein-binding and receptor interaction index based on free energies of transfer.
  - Automated classification: high receptor interaction (> 2.48 kcal/mol) vs. selective antimicrobial profile (< 2.01 kcal/mol).
- **Bjellqvist pKa Scale (`bioskills.core.constants`)**:
  - Added ExPASy ProtParam standard Bjellqvist pKa scale (`bjellqvist`) to `PKA_SCALES`.
- **Contois High-Cell-Density Kinetics (`bioskills.core.bioprocess`)**:
  - Growth inhibition modeling driven by biomass concentration / steric crowding ($\mu = \mu_{\max} \frac{S}{K_{SX} X + S}$).
  - Supported in CLI via `--biomass` and `--ks-x`.
- **Luedeking-Piret Product Formation Kinetics (`bioskills.core.bioprocess`)**:
  - Mathematical decoupling of growth-associated ($\alpha$) vs. non-growth-associated ($\beta$) metabolite synthesis ($q_P = \alpha \mu + \beta$).
  - Automated classification: Type I (Primary metabolites), Type II (Secondary/antibiotics), and Type III (Mixed).
  - New CLI subcommand: `bioskills bioprocess luedeking --mu <MU> --biomass <X> [--alpha <A>] [--beta <B>] [--json]`.
- **Academic Inspiration & Citations**:
  - Formal academic references section in `README.md` and `CITATION.cff` acknowledging the seminal open-source architectures of `peptides.py` (Larralde et al., EMBL) and `modlAMP` (Müller et al., ETH Zürich).

---

## [1.0.0] - 2026-11-06

### Added
- **Core Molecular Biophysics (`bioskills.core.peptide`)**:
  - Exact molecular weight calculation (average isotopic and monoisotopic).
  - Multi-protic Henderson-Hasselbalch isoelectric point (pI) via numerical bisection ($f(\text{pH}) = 0$).
  - Net electrical charge $\mathcal{Z}(\text{pH})$ titration curve across 4 validated pKa scales (`lehninger`, `emboss`, `rodwell`, `grimsley`).
  - Kyte-Doolittle Grand Average of Hydropathicity (GRAVY).
  - Eisenberg hydrophobic moment ($\mu_H$) for $\alpha$-helix ($100^\circ$) and $\beta$-sheet ($160^\circ$).
  - Ikai aliphatic index for thermal stability profiling.
  - Complete *in-silico* alanine scanning mutagenesis ($\Delta\Delta G$ heuristics and hydropathy differential).
  - MEROPS protease cleavage site mapper (DPP-4, Neprilysin, Trypsin, Chymotrypsin, Thrombin).

- **Bioprocess Kinetics & Scale-Up (`bioskills.core.bioprocess`)**:
  - Unstructured Monod kinetics ($\mu = \mu_{\max} \frac{S}{K_S + S} - k_d$).
  - Haldane/Andrews substrate inhibition kinetics ($\mu = \mu_{\max} \frac{S}{K_S + S + S^2 / K_I}$) with analytical derivation of optimum substrate concentration $S_{\text{opt}} = \sqrt{K_S K_I}$.
  - Doubling time ($t_d = \frac{\ln 2}{\mu}$).
  - Bioreactor hydrodynamics: Reynolds number ($Re$), impeller tip speed ($v_{\text{tip}} = \pi N D_i$), ungassed power ($P_0 = N_p \rho N^3 D_i^5$), gassed power ($P_g$ via Michel & Miller), volumetric power density ($P/V$), and maximum oxygen transfer rate ($OTR_{\max}$).
  - Multi-criteria scale-up translation between bench, pilot, and industrial bioreactors under constant power-per-volume ($P/V$), constant tip speed ($v_{\text{tip}}$), or constant mass transfer ($k_L a$).

- **Stoichiometry & Energy Auditing (`bioskills.core.stoichiometry`)**:
  - Macroscopic carbon balance recovery ($R_C = \frac{C_{\text{out}}}{C_{\text{in}}} \times 100\%$) and elemental C-mole accounting.
  - Elemental degree of reduction ($\gamma = \frac{4C + H - 2O - 3N + 5P + 6S}{C}$) per C-mole formula.
  - Pirt cellular maintenance energy model ($m_S = \mu \left( \frac{1}{Y_{\text{obs}}} - \frac{1}{Y_{\max}} \right)$) separating biomass synthesis from endogenous cellular maintenance.

- **Dimensional Unit Conversions (`bioskills.core.units`)**:
  - Dissolved oxygen saturation, concentration (mg/L), and partial pressure ($kPa$) via Benson-Krause formulation.
  - Optical density ($OD_{600}$) to Dry Cell Weight ($\text{DCW}$) with species-specific calibrators (*E. coli*, *S. cerevisiae*, *P. pastoris*, *CHO*).
  - Bioreactor aeration conversions: volumetric flow ($vvm \leftrightarrow L/\min \leftrightarrow m^3/h$) and superficial gas velocity ($v_s$).

- **Standardized AI Agent Skills (`skills/*/SKILL.md`)**:
  - Standardized agent skill definitions for autonomous AI agents (Google Antigravity, Claude Code, Cursor, CrewAI) with `--json` schema guarantees to eliminate numerical hallucinations in scientific calculations.
  - Bundled skill export command: `bioskills skills export --dest <DIR>`.

- **Test Suite & CI**:
  - 20 comprehensive unit tests with `pytest` testing analytical limits, edge cases, and CLI outputs.
  - GitHub Actions CI workflow for Python 3.10, 3.11, and 3.12 matrices.
