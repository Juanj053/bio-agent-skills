---
name: bioprocess-kinetics
description: Rigorous microbial and mammalian growth kinetics, substrate inhibition (Monod and Haldane), mass transfer (kla, OTR), and fluid hydrodynamics for bioreactors.
---

# Bioprocess Kinetics & Hydrodynamics Agent Skill

Use this skill when you need to calculate:
1. Specific growth rates under classical uninhibited Monod kinetics, Haldane substrate inhibition, or Contois high-cell-density crowding models.
2. Net cell proliferation and biomass doubling time ($t_d = \frac{\ln 2}{\mu - k_d}$).
3. Optimal substrate concentrations ($S_{\text{opt}} = \sqrt{K_S \cdot K_I}$) and peak attainable specific growth rates under substrate toxicity.
4. Product synthesis rates via the Luedeking-Piret equation separating growth-associated ($\alpha$) from non-growth-associated ($\beta$) synthesis.
5. Bioreactor fluid hydrodynamics: Impeller Reynolds number ($Re$), tip speed ($v_{\text{tip}}$), gassed/ungassed power draw ($P_0, P_g$), volumetric power density ($P/V$ in $\text{kW/m}^3$), and oxygen mass transfer coefficient ($k_L a$).

## CLI Invocation

### 1. Growth Kinetics Evaluation
```bash
# Classical Monod
bioskills bioprocess kinetics --mu-max 0.35 --substrate 15.0 --ks 2.0 --kd 0.012 --json

# Substrate Inhibition (Haldane / Andrews Model)
bioskills bioprocess kinetics --mu-max 0.40 --substrate 35.0 --ks 1.5 --ki 45.0 --kd 0.015 --json

# High Cell Density Fermentation (Contois Model)
bioskills bioprocess kinetics --mu-max 0.45 --substrate 25.0 --ks 1.0 --biomass 45.0 --ks-x 0.65 --json
```

### 2. Product Formation Kinetics (Luedeking-Piret)
```bash
# Calculate specific product rate qP and volumetric productivity dP/dt
bioskills bioprocess luedeking --mu 0.35 --biomass 15.0 --alpha 0.18 --beta 0.008 --json
```

### 3. Hydrodynamics & Oxygen Transfer Rate (OTR)
```bash
# Standard 20 L Stirred Tank with Rushton Impellers
bioskills bioprocess hydrodynamics --type str_rushton --vol 20.0 --rpm 450 --vvm 1.2 --json

# 500 L Pilot Reactor with Marine Propellers
bioskills bioprocess hydrodynamics --type str_marine --vol 500.0 --rpm 220 --vvm 0.8 --json
```

## Mathematical Formulations
- **Monod Growth**:
  $$\mu = \mu_{\max} \frac{S}{K_S + S}$$
- **Haldane Substrate Inhibition**:
  $$\mu = \mu_{\max} \frac{S}{K_S + S + \frac{S^2}{K_I}}$$
- **Contois Cell-Density Inhibition**:
  $$\mu = \mu_{\max} \frac{S}{K_{SX} \cdot X + S}$$
- **Luedeking-Piret Product Formation**:
  $$q_P = \alpha \mu + \beta, \quad \frac{dP}{dt} = \alpha \frac{dX}{dt} + \beta X$$
- **Impeller Reynolds Number**:
  $$Re = \frac{\rho \cdot N \cdot D_i^2}{\mu}$$
- **Volumetric Mass Transfer ($k_L a$ via Van't Riet)**:
  $$k_L a = 0.026 \left(\frac{P_g}{V}\right)^{0.4} (v_s)^{0.5} \times 3600 \quad [\text{h}^{-1}]$$
