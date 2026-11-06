---
name: bioreactor-scaleup
description: Bioprocess scale-up translation between bench, pilot, and industrial bioreactors under constant power-per-volume, constant tip speed, or constant mass transfer.
---

# Bioreactor Scale-Up Translation Agent Skill

Use this skill when scaling fermentation and cell culture bioprocesses from laboratory bench scale (e.g., 2 L - 20 L) to pilot plant (50 L - 500 L) or industrial production (1,000 L - 50,000 L):
1. **Constant Power Density ($P/V = \text{const}$)**: Standard for aerobic microbial fermentations where oxygen transfer must be maintained.
2. **Constant Impeller Tip Speed ($v_{\text{tip}} = \text{const}$)**: Crucial for shear-sensitive biological hosts (mammalian CHO cells, plant suspension cultures, filamentous fungi).
3. **Constant Volumetric Mass Transfer ($k_L a = \text{const}$)**: Calibrated translation ensuring cellular oxygen uptake ($OUR$) is fully satisfied by reactor gas-liquid transfer ($OTR$).
4. **Estimated Mixing Time Increase ($\theta_{m2}/\theta_{m1}$)**: Identifies risks of pH, substrate, or dissolved oxygen gradient formation at large scale.

## CLI Invocation

### 1. Scale-Up Under Constant Power per Volume ($P/V$)
```bash
# Scale up from 20 L bench reactor (450 RPM, 1.2 vvm) to 500 L pilot reactor
bioskills bioprocess scaleup --source-vol 20.0 --target-vol 500.0 --rpm 450 --vvm 1.2 --criterion power_volume --json
```

### 2. Scale-Up Under Constant Tip Speed ($v_{\text{tip}}$ - Shear Limitation)
```bash
# Scale up mammalian cell culture to prevent hydrodynamic cell lysis
bioskills bioprocess scaleup --source-vol 10.0 --target-vol 200.0 --rpm 180 --vvm 0.2 --criterion tip_speed --json
```

### 3. Scale-Up Under Constant Mass Transfer ($k_L a$)
```bash
# Scale up maintaining identical volumetric O2 transfer capability
bioskills bioprocess scaleup --source-vol 20.0 --target-vol 2000.0 --rpm 450 --vvm 1.0 --criterion kla --json
```

## Scale-Up Relations
- **Constant Power per Volume ($P/V$)**:
  $$N_2 = N_1 \left(\frac{V_1}{V_2}\right)^{2/9}$$
- **Constant Impeller Tip Speed ($v_{\text{tip}}$)**:
  $$N_2 = N_1 \left(\frac{V_1}{V_2}\right)^{1/3}$$
- **Mixing Time Ratio**:
  $$\frac{\theta_{m2}}{\theta_{m1}} = \left(\frac{N_1}{N_2}\right) \left(\frac{D_2}{D_1}\right)^2$$
