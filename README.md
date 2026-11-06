# <p align="center">bio-agent-skills</p>
<p align="center">
  <strong>Rigorous Bioengineering & In-Silico Molecular Agent Skills Suite (CLI & Agent Specs)</strong><br>
  <em>Deterministic Computational Tools for AI Agents (Antigravity, Claude Code, Cursor, CrewAI) & Biotech Researchers</em><br>
  Developed by <a href="https://www.linkedin.com/in/juanj-alva">Ing. Juan José Álvarez Morales</a> • <strong>Elevate Biotech</strong>
</p>

<p align="center">
  <a href="https://github.com/Juanj053/bio-agent-skills/actions"><img src="https://img.shields.io/badge/CI-passing-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white" alt="CI"></a>
  <a href="https://www.linkedin.com/in/juanj-alva"><img src="https://img.shields.io/badge/LinkedIn-Juan%20Jos%C3%A9%20%C3%81lvarez-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"></a>
  <img src="https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Agent%20Standard-SKILL.md%20Ready-blueviolet?style=for-the-badge" alt="Agent Skill">
</p>

---

## 🧬 Executive Overview: Why Bioengineering Needs Deterministic Agent Skills

Large Language Models (LLMs) and autonomous AI coding agents (such as Google Antigravity, Claude Code, Cursor, Codex, and CrewAI) are transforming scientific research. However, when asked to calculate **bioprocess scale-up parameters, multi-protic isoelectric points, mass transfer coefficients ($k_L a$), or macroscopic carbon balances**, generic LLMs frequently:
1. **Hallucinate arithmetic and exponents** in non-linear kinetic equations (e.g., Andrews/Haldane substrate inhibition).
2. **Violate conservation laws**, generating impossible biomass yields or unphysical carbon recoveries.
3. **Use oversimplified pKa heuristics**, causing errors in peptide charge curves ($\mathcal{Z}(pH)$) and solubility predictions.

**`bio-agent-skills`** solves this by providing a **dual-purpose scientific architecture**:
1. **A High-Performance Terminal CLI (`bioskills`)**: Pure Python tool with zero bloat, producing human-readable tables or machine-readable `--json` for automated pipelines.
2. **Standardized AI Agent Skills (`skills/*/SKILL.md`)**: Plug-and-play skill bundles that AI agents can discover, read, and invoke to execute deterministic bioengineering calculations without hallucinations.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        BIO-AGENT-SKILLS UNIFIED ARCHITECTURE                           │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
        ┌───────────────────────────────────┼───────────────────────────────────┐
        ▼                                   ▼                                   ▼
[ IN-SILICO PEPTIDES ]              [ BIOPROCESS & SCALE ]              [ STOICHIOMETRY & AUDIT ]
• Multi-protic pI Bisection         • Monod & Haldane Kinetics          • Macroscopic Carbon Recovery
• Net Charge Z(pH) Titration        • Hydrodynamics: Re, v_tip, P/V     • Degree of Reduction (gamma)
• Alanine Scanning Mutagenesis      • Mass Transfer: kla (Van't Riet)   • Pirt Maintenance Energy (mS)
• MEROPS Protease Stability         • Scale-Up Translation              • DO / Aeration / OD600 Units
        │                                   │                                   │
        └───────────────────────────────────┼───────────────────────────────────┘
                                            ▼
                      ┌───────────────────────────────────────────┐
                      │    CLI ENGINE: bioskills  (--json / UI)   │
                      └─────────────────────┬─────────────────────┘
                                            ▼
                 Compatible with: Antigravity • Claude Code • Cursor • CrewAI
```

---

## 📦 Bundled Agent Skills

| Skill Folder | Domain & Scope | Mathematical Engine | CLI Commands |
| :--- | :--- | :--- | :--- |
| [**`skills/peptide-biophysics`**](skills/peptide-biophysics/SKILL.md) | In-silico peptide screening & biophysics | Bisection $pI$, Henderson-Hasselbalch, Kyte-Doolittle GRAVY, Eisenberg $\mu_H$, MEROPS proteolysis | `bioskills peptide analyze`<br>`bioskills peptide scan`<br>`bioskills peptide cleave` |
| [**`skills/bioprocess`**](skills/bioprocess/SKILL.md) | Growth kinetics & reactor hydrodynamics | Monod, Haldane substrate inhibition, Van't Riet $k_L a$, Reynolds $Re$, tip speed $v_{\text{tip}}$ | `bioskills bioprocess kinetics`<br>`bioskills bioprocess hydrodynamics` |
| [**`skills/bioreactor-scaleup`**](skills/bioreactor-scaleup/SKILL.md) | Scale-up translation across vessel volumes | Constant $P/V$, constant $v_{\text{tip}}$, constant $k_L a$, mixing time ratio $\theta_{m2}/\theta_{m1}$ | `bioskills bioprocess scaleup` |
| [**`skills/stoichiometry-audit`**](skills/stoichiometry-audit/SKILL.md) | Elemental balances & maintenance audits | Degree of reduction ($\gamma$), carbon balance recovery, Pirt maintenance energy equation | `bioskills stoichiometry balance`<br>`bioskills stoichiometry reduction`<br>`bioskills stoichiometry pirt` |

---

## 🚀 Quick Start & Installation

### Option A: Direct Execution via `uvx` (No Installation Required)
```bash
# Run any skill command directly via uvx
uvx --from git+https://github.com/Juanj053/bio-agent-skills.git bioskills peptide analyze --seq "GHK"
```

### Option B: Local Installation with `uv` or `pip`
```bash
# Clone the repository
git clone https://github.com/Juanj053/bio-agent-skills.git
cd bio-agent-skills

# Install in editable mode
uv pip install -e ".[dev]"

# Run test suite
pytest -v tests/
```

---

## 💻 CLI Usage & Examples

### 1. Peptide Biophysical Profiling
```bash
# Analyze Semaglutide peptide backbone
bioskills peptide analyze --seq "HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG" --ph 7.4 --scale lehninger
```
*Output:*
```text
================================================================================
🧬 BIOSKILLS CLI | Rigorous Bioengineering & In-Silico Molecular Skills
================================================================================
[🔬 PEPTIDE BIOPHYSICAL PROFILING]
--------------------------------------------------------------------------------
  Sequence                                : HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG
  Length                                  : 31
  Mw Average Da                           : 3379.711
  Isoelectric Point Pi                    : 5.234
  Net Charge At Target Ph                 : -1.025
  Gravy Score                             : -0.1903
  Hydrophobic Moment Helix                : 0.3421
  Aliphatic Index                         : 72.58
  Solubility Risk                         : Favorable
================================================================================
```

### 2. In-Silico Alanine Scanning Mutagenesis
```bash
# Evaluate residue contribution to pI, charge, and hydropathicity
bioskills peptide scan --seq "GEPGP" --ph 7.4 --json
```

### 3. Proteolytic Cleavage Profiling (MEROPS Proteases)
```bash
# Check cleavage susceptibility against DPP-4, Neprilysin, Trypsin, Chymotrypsin
bioskills peptide cleave --seq "HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG"
```

### 4. Bioprocess Growth Kinetics (Monod & Haldane Substrate Inhibition)
```bash
# Haldane substrate inhibition (mu_max=0.40, S=35g/L, Ks=1.5g/L, Ki=45g/L)
bioskills bioprocess kinetics --mu-max 0.40 --substrate 35.0 --ks 1.5 --ki 45.0 --kd 0.012
```

### 5. Bioreactor Hydrodynamics & Oxygen Transfer Rate (OTR)
```bash
# 20 L stirred tank with dual Rushton impellers at 450 RPM, 1.2 vvm
bioskills bioprocess hydrodynamics --type str_rushton --vol 20.0 --rpm 450 --vvm 1.2
```

### 6. Bioreactor Scale-Up Translation
```bash
# Translate from 20 L bench scale to 500 L pilot scale under constant power per volume (P/V)
bioskills bioprocess scaleup --source-vol 20.0 --target-vol 500.0 --rpm 450 --vvm 1.2 --criterion power_volume
```

### 7. Macroscopic Carbon Balance Recovery
```bash
# Verify stoichiometric carbon recovery across a fermentation batch
bioskills stoichiometry balance --s0 35.0 --sf 0.0 --x0 0.8 --xf 11.5 --p0 0.0 --pf 3.2
```

### 8. Elemental Degree of Reduction ($\gamma$)
```bash
# Glucose (C6 H12 O6) -> gamma = 4.00
bioskills stoichiometry reduction -C 6 -H 12 -O 6

# Glycerol (C3 H8 O3) -> gamma = 4.67
bioskills stoichiometry reduction -C 3 -H 8 -O 3
```

---

## 🤖 Exporting Skills to AI Coding Agents

You can export the standardized `SKILL.md` files directly into your AI assistant workspace:

```bash
# Export to Google Antigravity custom skills directory
bioskills skills export --dest ~/.gemini/skills/

# Export to Claude Code / Claude Desktop directory
bioskills skills export --dest ~/.claude/skills/

# Export to current workspace
bioskills skills export --dest ./skills/
```

Once exported, your AI agent can automatically execute `bioskills` CLI commands to answer complex scientific prompts with complete mathematical fidelity.

---

## 📂 Repository Structure

```
bio-agent-skills/
├── .github/workflows/
│   └── ci.yml                   # Automated matrix tests across Python 3.10, 3.11, 3.12
├── skills/                      # Standardized AI Agent Skill packs
│   ├── bioprocess/
│   │   └── SKILL.md             # Growth kinetics & hydrodynamics skill spec
│   ├── peptide-biophysics/
│   │   └── SKILL.md             # In-silico peptide biophysics & ADMET spec
│   ├── bioreactor-scaleup/
│   │   └── SKILL.md             # Bioreactor scale-up translation spec
│   └── stoichiometry-audit/
│       └── SKILL.md             # Carbon balance & Pirt maintenance spec
├── src/bioskills/
│   ├── __init__.py              # Package init & version metadata
│   ├── cli.py                   # High-performance CLI tool
│   └── core/
│       ├── constants.py         # Validated biophysical constants & pKa tables
│       ├── peptide.py           # pI bisection, charge titration, alanine scan, proteolysis
│       ├── bioprocess.py        # Monod/Haldane kinetics, hydrodynamics, kla, scale-up
│       ├── stoichiometry.py     # Carbon balance, degree of reduction, Pirt audit
│       └── units.py             # DO, OD600/DCW, and aeration unit interconversions
├── tests/
│   ├── test_peptide.py          # Unit tests for peptide biophysics
│   ├── test_bioprocess.py       # Unit tests for kinetics and hydrodynamics
│   ├── test_stoichiometry.py    # Unit tests for carbon balances
│   ├── test_units.py            # Unit tests for unit conversions
│   └── test_cli.py              # Unit tests for CLI commands and JSON export
├── pyproject.toml               # Modern PEP 517/621 packaging (Hatchling)
├── CITATION.cff                 # Academic citation metadata
├── LICENSE                      # MIT License
└── README.md                    # Documentation & user guide
```

---

## 📜 Citation

If you utilize this skills suite or CLI tool in your academic research, industrial biomanufacturing scale-up protocols, or agentic AI workflows, please cite:

```bibtex
@software{alvarez_morales_2026_bio_agent_skills,
  author       = {Álvarez Morales, Juan José},
  title        = {bio-agent-skills: Rigorous Bioengineering & In-Silico Molecular Agent Skills Suite},
  month        = nov,
  year         = 2026,
  publisher    = {GitHub},
  version      = {1.0.0},
  url          = {https://github.com/Juanj053/bio-agent-skills}
}
```

---

## 👨‍🔬 Author & Collaborations

**Ing. Juan José Álvarez Morales**  
*Biotechnology Engineer (Universidad Técnica de Ambato)*  
*Founder & Chief Bioengineer at Elevate Biotech • Research Lead at Agromanper*  
Ambato, Ecuador 🇪🇨  

- **LinkedIn:** [linkedin.com/in/juanj-alva](https://www.linkedin.com/in/juanj-alva)  
- **Email:** [jjalvarezm77@gmail.com](mailto:jjalvarezm77@gmail.com)  
- **GitHub:** [@Juanj053](https://github.com/Juanj053)  
- **Research Collaboration:** Open for international academic consortia, grant proposals (CYTED, NIH/Fogarty), and AI-driven biotechnology partnerships.
