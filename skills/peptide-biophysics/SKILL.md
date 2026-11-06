---
name: peptide-biophysics
description: In-silico peptide biophysics, multi-protic isoelectric point (pI) bisection, net charge titration, alanine scanning mutagenesis, and MEROPS enzymatic cleavage profiling.
---

# In-Silico Peptide Biophysics & ADMET Agent Skill

Use this skill when you need to analyze, screen, or engineer therapeutic peptides, bioactive sequences, or recombinant proteins:
1. Exact monoisotopic and average molecular weights ($M_W$).
2. Multi-protic isoelectric point ($pI$) solved by numerical bisection across Henderson-Hasselbalch equilibria.
3. Net electrostatic charge titration $\mathcal{Z}(pH)$ at physiological ($pH = 7.4$) or custom target pH.
4. Grand Average of Hydropathicity (GRAVY via Kyte-Doolittle) and Eisenberg hydrophobic moments ($\mu_H$) at $\alpha$-helical ($100^\circ$) and $\beta$-sheet ($160^\circ$) periodicity.
5. In-silico Alanine Scanning Mutagenesis: computes $\Delta pI$, $\Delta \text{GRAVY}$, $\Delta \mu_H$, and $\Delta \mathcal{Z}$.
6. Proteolytic stability profiling against major human physiological endopeptidases (DPP-4, Neprilysin, Trypsin, Chymotrypsin, Thrombin).

## CLI Invocation

### 1. Peptide Biophysical Analysis
```bash
# Analyze Semaglutide backbone (or GLP-1, BPC-157, etc.)
bioskills peptide analyze --seq "HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG" --ph 7.4 --scale lehninger --json

# Analyze short bioactive peptide (e.g. GHK or Epitalon)
bioskills peptide analyze --seq "GHK" --ph 7.4 --json
```

### 2. Alanine Scanning Mutagenesis
```bash
# Evaluate residue contribution to hydrophobicity, pI, and charge
bioskills peptide scan --seq "GEPGP" --ph 7.4 --json
```

### 3. Proteolytic Cleavage Profiling (MEROPS)
```bash
# Scan sequence for DPP-4, Neprilysin, and Trypsin cleavage sites
bioskills peptide cleave --seq "HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG" --json
```

## Mathematical Formulations
- **Multi-protic Charge Balance**:
  $$\mathcal{Z}(pH) = \frac{1}{1 + 10^{pH - pKa(N)}} + \sum_{\text{basic}} \frac{1}{1 + 10^{pH - pKa_i}} - \frac{1}{1 + 10^{pKa(C) - pH}} - \sum_{\text{acidic}} \frac{1}{1 + 10^{pKa_i - pH}}$$
- **Hydrophobic Moment**:
  $$\mu_H = \frac{1}{N} \sqrt{\left(\sum_{i=1}^N h_i \cos(i\delta)\right)^2 + \left(\sum_{i=1}^N h_i \sin(i\delta)\right)^2}$$
