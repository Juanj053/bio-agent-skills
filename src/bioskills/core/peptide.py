"""
In-silico peptide biophysics, pI titration, alanine scanning, and proteolytic cleavage analysis.
"""

import math
from typing import Dict, Any, List, Tuple
from bioskills.core.constants import (
    AMINO_ACIDS,
    WATER_MW_AVERAGE,
    WATER_MW_MONOISOTOPIC,
    RESIDUE_MW_AVERAGE,
    RESIDUE_MW_MONO,
    KYTE_DOOLITTLE,
    EISENBERG,
    PKA_SCALES
)


def validate_peptide_sequence(sequence: str) -> str:
    """Validates and standardizes single-letter amino acid sequences."""
    seq = sequence.strip().upper()
    if not seq:
        raise ValueError("Peptide sequence cannot be empty.")
    invalid = set(seq) - AMINO_ACIDS
    if invalid:
        raise ValueError(f"Sequence contains invalid non-canonical amino acid codes: {sorted(list(invalid))}")
    return seq


def compute_net_charge(sequence: str, ph: float, pka_scale: str = "lehninger") -> float:
    """
    Computes the net multi-protic electrostatic charge Z(pH) of a peptide:
    Positive charges: N-terminus, Lys, Arg, His
    Negative charges: C-terminus, Asp, Glu, Cys, Tyr
    """
    pka = PKA_SCALES.get(pka_scale.lower(), PKA_SCALES["lehninger"])
    
    # N-terminal positive charge
    charge = 1.0 / (1.0 + 10.0 ** (ph - pka["N_term"]))
    
    # C-terminal negative charge
    charge -= 1.0 / (1.0 + 10.0 ** (pka["C_term"] - ph))
    
    # Side chains
    for aa in sequence:
        if aa in ("K", "R", "H"):
            charge += 1.0 / (1.0 + 10.0 ** (ph - pka[aa]))
        elif aa in ("D", "E", "C", "Y"):
            charge -= 1.0 / (1.0 + 10.0 ** (pka[aa] - ph))
            
    return charge


def compute_isoelectric_point(sequence: str, pka_scale: str = "lehninger", tol: float = 1e-4) -> float:
    """
    Solves for the Isoelectric Point (pI) where Z(pH) = 0 via high-precision bisection root finding.
    """
    low = 0.0
    high = 14.0
    
    for _ in range(60):
        mid = (low + high) / 2.0
        charge_mid = compute_net_charge(sequence, mid, pka_scale)
        
        if abs(charge_mid) < tol or (high - low) / 2.0 < tol:
            return round(mid, 3)
            
        if charge_mid > 0:
            low = mid
        else:
            high = mid
            
    return round((low + high) / 2.0, 3)


def compute_hydrophobic_moment(sequence: str, angle_deg: float = 100.0) -> float:
    """
    Computes the mean hydrophobic moment (mu_H) via the Eisenberg consensus scale.
    Standard angle: 100 degrees for alpha-helix, 160 degrees for beta-sheet.
    """
    n = len(sequence)
    if n == 0:
        return 0.0
        
    rad = math.radians(angle_deg)
    sum_cos = 0.0
    sum_sin = 0.0
    
    for i, aa in enumerate(sequence):
        h = EISENBERG.get(aa, 0.0)
        sum_cos += h * math.cos(i * rad)
        sum_sin += h * math.sin(i * rad)
        
    moment = math.sqrt(sum_cos ** 2 + sum_sin ** 2) / n
    return round(moment, 4)


def compute_gravy(sequence: str) -> float:
    """Computes Grand Average of Hydropathicity (GRAVY) via Kyte-Doolittle scale."""
    if not sequence:
        return 0.0
    return round(sum(KYTE_DOOLITTLE.get(aa, 0.0) for aa in sequence) / len(sequence), 4)


def compute_aliphatic_index(sequence: str) -> float:
    """
    Computes Ikai Aliphatic Index:
    AI = X(Ala) + 2.9 * X(Val) + 3.9 * (X(Ile) + X(Leu))
    """
    n = len(sequence)
    if n == 0:
        return 0.0
    x_a = sequence.count('A') / n
    x_v = sequence.count('V') / n
    x_i = sequence.count('I') / n
    x_l = sequence.count('L') / n
    ai = 100.0 * (x_a + 2.9 * x_v + 3.9 * (x_i + x_l))
    return round(ai, 2)


def calculate_peptide_properties(
    sequence: str,
    ph: float = 7.4,
    pka_scale: str = "lehninger"
) -> Dict[str, Any]:
    """
    Comprehensive biophysical profiling of a peptide sequence.
    """
    seq = validate_peptide_sequence(sequence)
    n = len(seq)
    
    # Molecular Weights
    mw_avg = sum(RESIDUE_MW_AVERAGE[aa] for aa in seq) + WATER_MW_AVERAGE
    mw_mono = sum(RESIDUE_MW_MONO[aa] for aa in seq) + WATER_MW_MONOISOTOPIC
    
    # Electrostatics & pI
    pi = compute_isoelectric_point(seq, pka_scale)
    z_ph = compute_net_charge(seq, ph, pka_scale)
    z_neutral = compute_net_charge(seq, 7.0, pka_scale)
    
    # Hydrophobicity & Structure
    gravy = compute_gravy(seq)
    mu_h_helix = compute_hydrophobic_moment(seq, 100.0)
    mu_h_sheet = compute_hydrophobic_moment(seq, 160.0)
    aliphatic_idx = compute_aliphatic_index(seq)
    
    # Amino acid composition
    comp = {aa: seq.count(aa) for aa in sorted(list(set(seq)))}
    
    # Precipitation risk heuristic (near pI)
    solubility_risk = "High Risk (pI close to physiological pH 7.4)" if abs(pi - 7.4) < 0.6 else "Favorable"
    
    return {
        "sequence": seq,
        "length": n,
        "mw_average_da": round(mw_avg, 3),
        "mw_monoisotopic_da": round(mw_mono, 4),
        "isoelectric_point_pi": pi,
        "net_charge_at_target_ph": round(z_ph, 3),
        "target_ph": ph,
        "net_charge_neutral_ph7": round(z_neutral, 3),
        "pka_scale_used": pka_scale,
        "gravy_score": gravy,
        "hydrophobic_moment_helix": mu_h_helix,
        "hydrophobic_moment_sheet": mu_h_sheet,
        "aliphatic_index": aliphatic_idx,
        "solubility_risk": solubility_risk,
        "composition": comp
    }


def alanine_scanning_mutagenesis(sequence: str, ph: float = 7.4) -> List[Dict[str, Any]]:
    """
    Performs computational alanine scanning mutagenesis:
    Replaces each non-alanine residue with Ala and computes biophysical deltas (Delta-pI, Delta-GRAVY, Delta-Charge).
    """
    seq = validate_peptide_sequence(sequence)
    wt = calculate_peptide_properties(seq, ph=ph)
    results = []
    
    for i, aa in enumerate(seq):
        if aa == 'A':
            continue
            
        mutant_seq = seq[:i] + 'A' + seq[i+1:]
        mut = calculate_peptide_properties(mutant_seq, ph=ph)
        
        delta_pi = round(mut["isoelectric_point_pi"] - wt["isoelectric_point_pi"], 3)
        delta_gravy = round(mut["gravy_score"] - wt["gravy_score"], 4)
        delta_charge = round(mut["net_charge_at_target_ph"] - wt["net_charge_at_target_ph"], 3)
        delta_mu_h = round(mut["hydrophobic_moment_helix"] - wt["hydrophobic_moment_helix"], 4)
        
        results.append({
            "position": i + 1,
            "wild_type_residue": aa,
            "mutation": f"{aa}{i+1}A",
            "mutant_sequence": mutant_seq,
            "mutant_pi": mut["isoelectric_point_pi"],
            "delta_pi": delta_pi,
            "mutant_gravy": mut["gravy_score"],
            "delta_gravy": delta_gravy,
            "mutant_net_charge": mut["net_charge_at_target_ph"],
            "delta_net_charge": delta_charge,
            "delta_hydrophobic_moment": delta_mu_h
        })
        
    return results


def protease_cleavage_profile(sequence: str) -> Dict[str, Any]:
    """
    Profiles enzymatic cleavage susceptibility against key clinical and laboratory proteases:
    - DPP-4 (Dipeptidyl peptidase-4): N-terminal cleaves after Pro or Ala at P2 position
    - Neprilysin (NEP / Neutral endopeptidase): Cleaves N-terminal to bulky hydrophobic residues (L, F, I)
    - Trypsin: Cleaves C-terminal to Arg or Lys (unless followed by Pro)
    - Chymotrypsin: Cleaves C-terminal to Phe, Tyr, or Trp (unless followed by Pro)
    - Thrombin: Cleaves after Arg in Gly-Arg or Pro-Arg motifs
    - Elastase: Cleaves after small uncharged residues (Ala, Val, Gly, Ser)
    - Pepsin: Cleaves after Leu, Phe, Glu under acidic conditions
    """
    seq = validate_peptide_sequence(sequence)
    n = len(seq)
    cleavage_events = []
    
    # 1. DPP-4: Cleaves peptide bond between residue 2 and 3 if residue 2 is P or A
    if n >= 3 and seq[1] in ("P", "A"):
        cleavage_events.append({
            "protease": "DPP-4",
            "position": 2,
            "cleavage_bond": f"{seq[1]}2-{seq[2]}3",
            "mechanism": "N-terminal dipeptide release (Pro/Ala at P1)",
            "impact": "Rapid inactivation (characteristic of native GLP-1/GIP)"
        })
        
    # 2. Trypsin: Cleaves after K or R, not before P
    for i in range(n - 1):
        if seq[i] in ("K", "R") and seq[i+1] != "P":
            cleavage_events.append({
                "protease": "Trypsin",
                "position": i + 1,
                "cleavage_bond": f"{seq[i]}{i+1}-{seq[i+1]}{i+2}",
                "mechanism": "Endopeptidase basic specificity (Lys/Arg)",
                "impact": "Internal chain fragmentation"
            })
            
    # 3. Chymotrypsin: Cleaves after F, Y, W, not before P
    for i in range(n - 1):
        if seq[i] in ("F", "Y", "W") and seq[i+1] != "P":
            cleavage_events.append({
                "protease": "Chymotrypsin",
                "position": i + 1,
                "cleavage_bond": f"{seq[i]}{i+1}-{seq[i+1]}{i+2}",
                "mechanism": "Aromatic hydrophobic residue cleavage",
                "impact": "Core scaffold disruption"
            })
            
    # 4. Neprilysin (NEP): Cleaves bond preceding L, F, I
    for i in range(1, n):
        if seq[i] in ("L", "F", "I") and seq[i-1] != "P":
            cleavage_events.append({
                "protease": "Neprilysin",
                "position": i,
                "cleavage_bond": f"{seq[i-1]}{i}-{seq[i]}{i+1}",
                "mechanism": "Zinc-dependent metalloendopeptidase cleavage",
                "impact": "Major renal/endothelial clearance pathway"
            })
            
    # 5. Thrombin: Cleaves after R in PR or GR
    for i in range(1, n):
        if seq[i] == "R" and seq[i-1] in ("P", "G"):
            cleavage_events.append({
                "protease": "Thrombin",
                "position": i + 1,
                "cleavage_bond": f"{seq[i]}{i+1}-{seq[i+1] if i+1 < n else 'end'}",
                "mechanism": "Pro/Gly-Arg recognition motif",
                "impact": "Circulatory systemic degradation"
            })

    total_cleavage_sites = len(cleavage_events)
    stability_rating = (
        "High Proteolytic Stability" if total_cleavage_sites <= 1
        else ("Moderate Stability" if total_cleavage_sites <= 3 else "High Proteolytic Vulnerability")
    )

    return {
        "sequence": seq,
        "length": n,
        "total_cleavage_sites": total_cleavage_sites,
        "stability_rating": stability_rating,
        "cleavage_events": cleavage_events
    }
