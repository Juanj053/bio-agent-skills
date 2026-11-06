---
name: stoichiometry-audit
description: Macroscopic elemental carbon balance recovery, degree of reduction per C-mole, and cellular maintenance energy audit (Pirt model) for fermentation processes.
---

# Stoichiometry & Carbon Balance Auditor Agent Skill

Use this skill when auditing biomanufacturing runs, fermentation batches, or cell culture yields:
1. Carbon Recovery Fraction ($C_{\text{recovery}} = \frac{C_{\text{biomass}} + C_{\text{product}} + C_{\text{CO2}}}{C_{\text{substrate}}}$).
2. Carbon incorporation efficiency into target recombinant products vs. cell biomass.
3. Degree of Reduction ($\gamma$) and available electron balances for carbon substrates, metabolites, and host dry cell weight.
4. Pirt equation cellular maintenance auditing to distinguish growth-associated energy demand from basal cell maintenance ($m_S$).

## CLI Invocation

### 1. Macroscopic Carbon Balance Recovery
```bash
# Evaluate carbon balance for a batch run (S0=35g/L, Sf=1.2g/L, X0=0.8g/L, Xf=11.5g/L, P0=0, Pf=3.2g/L)
bioskills stoichiometry balance --s0 35.0 --sf 1.2 --x0 0.8 --xf 11.5 --p0 0.0 --pf 3.2 --json
```

### 2. Degree of Reduction & Electron Balance
```bash
# Calculate gamma for glucose (C6 H12 O6)
bioskills stoichiometry reduction -C 6 -H 12 -O 6 --json

# Calculate gamma for glycerol (C3 H8 O3)
bioskills stoichiometry reduction -C 3 -H 8 -O 3 --json

# Calculate gamma for microbial biomass (CH1.8 O0.5 N0.2)
bioskills stoichiometry reduction -C 1 -H 2 -O 1 -N 0 --json
```

### 3. Pirt Maintenance Energy Audit
```bash
# Determine Pirt ms and fraction of carbon diverted to non-growth maintenance
bioskills stoichiometry pirt --mu 0.28 --yxs 0.42 --max-yield 0.51 --json
```

## Mathematical Formulations
- **Elemental Degree of Reduction ($\gamma$)**:
  $$\gamma = \frac{4C + H - 2O - 3N + 5P + 6S}{C}$$
- **Pirt Substrate Maintenance Model**:
  $$\frac{1}{Y_{X/S}^{\text{obs}}} = \frac{1}{Y_{X/S}^{\max}} + \frac{m_S}{\mu}$$
