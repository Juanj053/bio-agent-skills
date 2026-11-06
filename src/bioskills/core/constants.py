"""
Physical, chemical, and biological constants for bioengineering calculations.
"""

from typing import Dict

# Standard amino acid 1-letter codes
AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")

# Monoisotopic & Average Molecular Weights (Da) of amino acid residues in peptides
# (accounting for condensation: H2O removed per peptide bond)
WATER_MW_AVERAGE = 18.01528
WATER_MW_MONOISOTOPIC = 18.010565

RESIDUE_MW_AVERAGE: Dict[str, float] = {
    'A': 71.0788,
    'R': 156.1875,
    'N': 114.1038,
    'D': 115.0886,
    'C': 103.1388,
    'E': 129.1155,
    'Q': 128.1307,
    'G': 57.0519,
    'H': 137.1411,
    'I': 113.1594,
    'L': 113.1594,
    'K': 128.1741,
    'M': 131.1926,
    'F': 147.1766,
    'P': 97.1167,
    'S': 87.0782,
    'T': 101.1051,
    'W': 186.2132,
    'Y': 163.1760,
    'V': 99.1326,
}

RESIDUE_MW_MONO: Dict[str, float] = {
    'A': 71.037114,
    'R': 156.101111,
    'N': 114.042927,
    'D': 115.026943,
    'C': 103.009184,
    'E': 129.042593,
    'Q': 128.058578,
    'G': 57.021464,
    'H': 137.058912,
    'I': 113.084064,
    'L': 113.084064,
    'K': 128.094963,
    'M': 131.040485,
    'F': 147.068414,
    'P': 97.052764,
    'S': 87.032028,
    'T': 101.047678,
    'W': 186.079313,
    'Y': 163.063329,
    'V': 99.068414,
}

# Kyte-Doolittle Hydropathy Index
KYTE_DOOLITTLE: Dict[str, float] = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
    'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
    'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'E': -3.5,
    'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5
}

# Eisenberg Consensus Hydrophobic Scale (normalized hydrophobic moment)
EISENBERG: Dict[str, float] = {
    'I': 0.73, 'F': 0.61, 'V': 0.54, 'L': 0.53, 'W': 0.37,
    'M': 0.26, 'A': 0.25, 'G': 0.16, 'C': 0.04, 'Y': 0.02,
    'P': -0.07, 'T': -0.18, 'S': -0.26, 'H': -0.40, 'E': -0.62,
    'N': -0.64, 'Q': -0.69, 'D': -0.72, 'K': -1.10, 'R': -1.76
}

# Multiple pKa scales for multi-protic isoelectric point determination
PKA_SCALES: Dict[str, Dict[str, float]] = {
    "lehninger": {
        "N_term": 9.69, "C_term": 2.34,
        "C": 8.33, "D": 3.86, "E": 4.25,
        "H": 6.00, "K": 10.50, "R": 12.48, "Y": 10.07
    },
    "emboss": {
        "N_term": 8.6, "C_term": 3.6,
        "C": 8.5, "D": 3.9, "E": 4.1,
        "H": 6.5, "K": 10.8, "R": 12.5, "Y": 10.1
    },
    "rodwell": {
        "N_term": 8.0, "C_term": 3.1,
        "C": 8.33, "D": 3.68, "E": 4.25,
        "H": 6.0, "K": 11.5, "R": 11.5, "Y": 10.07
    },
    "grimsley": {
        "N_term": 7.7, "C_term": 3.3,
        "C": 6.8, "D": 3.5, "E": 4.2,
        "H": 6.6, "K": 10.5, "R": 12.0, "Y": 10.3
    }
}

# Guruprasad Instability Matrix weights (selected critical pairs for stability evaluation)
DI_PEPTIDE_INSTABILITY_DEFAULTS = {
    ('W', 'K'): 1.0, ('M', 'W'): 1.0, ('W', 'W'): 1.0, ('E', 'E'): -14.03,
    ('Q', 'Q'): 20.26, ('K', 'K'): 1.0, ('C', 'C'): 1.0, ('P', 'P'): 20.26
}

# Universal Gas Constant R
GAS_CONSTANT_R = 8.314462618  # J / (mol * K)

# Standard Dissolved Oxygen Henry's constant in water at 25-30°C (Benson-Krause model)
# Saturated DO at 30°C, 1 atm air = 7.54 mg/L = 0.00754 g/L = 0.2356 mmol/L
C_STAR_DO_30C_1ATM = 0.00754  # g/L
