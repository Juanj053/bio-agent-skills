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
5. In-vitro Instability Index (Guruprasad et al., 1990) with DIWV dipeptide statistical weights (threshold: $II < 40$ stable vs $II \ge 40$ unstable).
6. Boman Interaction Index (Boman, 2003) estimating protein-binding and receptor affinity.
7. In-silico Alanine Scanning Mutagenesis: computes $\Delta pI$, $\Delta \text{GRAVY}$, $\Delta \mu_H$, and $\Delta \mathcal{Z}$.
8. Proteolytic stability profiling against major human physiological endopeptidases (DPP-4, Neprilysin, Trypsin, Chymotrypsin, Thrombin).

## CLI Invocation

### 1. Peptide Biophysical Analysis
```bash
# Analyze Semaglutide backbone with Bjellqvist or Lehninger scale
bioskills peptide analyze --seq "HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG" --ph 7.4 --scale bjellqvist --json

# Analyze short bioactive peptide (e.g. GHK or Epitalon)
bioskills peptide analyze --seq "GHK" --ph 7.4 --json
```

### 2. In-Vitro Stability & Boman Interaction Index
```bash
# Predict in-vitro stability and receptor binding potential
bioskills peptide stability --seq "QWGRRCCGWGPGRRYCVRWC" --json
```

### 3. Alanine Scanning Mutagenesis
```bash
# Evaluate residue contribution to hydrophobicity, pI, and charge
bioskills peptide scan --seq "GEPGP" --ph 7.4 --json
```

### 4. Proteolytic Cleavage Profiling (MEROPS)
```bash
# Scan sequence for DPP-4, Neprilysin, and Trypsin cleavage sites
bioskills peptide cleave --seq "HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG" --json
```

## Mathematical Formulations
- **Instability Index (Guruprasad et al., 1990)**:
  $$II = \frac{10}{L} \sum_{i=1}^{L-1} \text{DIWV}(x_i, x_{i+1})$$
- **Boman Interaction Index (Boman, 2003)**:
  $$\text{Boman} = \frac{1}{L} \sum_{i=1}^L \Delta G_{\text{transfer}}(x_i)$$
- **Multi-protic Charge Balance**:
  $$\mathcal{Z}(pH) = \frac{1}{1 + 10^{pH - pKa(N)}} + \sum_{\text{basic}} \frac{1}{1 + 10^{pH - pKa_i}} - \frac{1}{1 + 10^{pKa(C) - pH}} - \sum_{\text{acidic}} \frac{1}{1 + 10^{pKa_i - pH}}$$
- **Hydrophobic Moment**:
  $$\mu_H = \frac{1}{N} \sqrt{\left(\sum_{i=1}^N h_i \cos(i\delta)\right)^2 + \left(\sum_{i=1}^N h_i \sin(i\delta)\right)^2}$$
